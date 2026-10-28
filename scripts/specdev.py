#!/usr/bin/env python3
"""Install shared agent workflows without running project commands or accessing services."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import string
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ("codex", "cursor", "claude")
BEGIN = "<!-- specdev:begin -->"
END = "<!-- specdev:end -->"
CONFIG = ".specdev/project.json"
MANIFEST = ".specdev/manifest.json"
ROLES = ("explorer", "worker", "reviewer", "investigator")
TEXT_SUFFIXES = {".md", ".mdc", ".py", ".json", ".toml", ".txt", ".yaml", ".yml"}
REASONING_EFFORTS = {"none", "minimal", "low", "medium", "high", "xhigh", "max", "ultra"}


def model_options(tool, value):
    """Keep legacy model strings; options belong to the selected native client."""
    if isinstance(value, str):
        if not value.strip():
            raise KitError("Modelo deve ser preenchido.")
        return {} if value == "inherit" else {"model": value}
    allowed = {"model"} | ({"reasoning_effort"} if tool == "codex" else {"tools"} if tool == "claude" else set())
    if not isinstance(value, dict) or not value or set(value) - allowed:
        raise KitError(f"Opções de agente não suportadas para {tool}.")
    if "model" in value and (not isinstance(value["model"], str) or not value["model"].strip()):
        raise KitError(f"Modelo inválido para {tool}.")
    if "reasoning_effort" in value and (not isinstance(value["reasoning_effort"], str) or
                                      value["reasoning_effort"] not in REASONING_EFFORTS):
        raise KitError("reasoning_effort inválido para Codex.")
    if "tools" in value:
        tools = value["tools"]
        if not isinstance(tools, list) or not tools or not all(
                isinstance(name, str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_.*-]*", name) for name in tools):
            raise KitError("tools exige uma lista não vazia de nomes de ferramentas Claude.")
    return {key: setting for key, setting in value.items() if key != "model" or setting != "inherit"}


class KitError(Exception):
    pass


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise KitError(f"Não foi possível ler JSON em {path}: {exc}") from exc


def relative_path(value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise KitError(f"Caminho relativo inválido: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or PureWindowsPath(value).drive or ".." in path.parts or ":" in value:
        raise KitError(f"Caminho fora do projeto: {value!r}")
    return path


def safe_path(root, name, *, directory=False):
    relative_path(name)
    path = root / name
    # Reject linked ancestors even when their target happens to remain inside root.
    for current in (path, *path.parents):
        if current == root:
            break
        if current.is_symlink() or getattr(current, "is_junction", lambda: False)():
            raise KitError(f"Link/junction não permitido no destino: {current}")
        if current != path and current.exists() and not current.is_dir():
            raise KitError(f"Ancestral não é diretório: {current}")
    if not path.resolve().is_relative_to(root.resolve()):
        raise KitError(f"Caminho fora do projeto: {path}")
    if path.exists() and not (path.is_dir() if directory else path.is_file()):
        raise KitError(f"Destino não é {'diretório' if directory else 'arquivo'}: {path}")
    return path


def required_string(obj, key):
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise KitError(f"Campo obrigatório inválido: {key}")
    return value


def validate_config(config):
    if not isinstance(config, dict) or type(config.get("schema_version")) is not int or config["schema_version"] != 1:
        raise KitError("project.json exige schema_version = 1.")
    for section in ("project", "git", "paths", "tracking", "delivery", "models"):
        if not isinstance(config.get(section), dict):
            raise KitError(f"Seção obrigatória ausente ou inválida: {section}")
    required_string(config["project"], "name")
    required_string(config["project"], "language")
    for key in ("base_branch", "remote", "branch_pattern"):
        required_string(config["git"], key)
    try:
        fields = list(string.Formatter().parse(config["git"]["branch_pattern"]))
    except ValueError as exc:
        raise KitError("git.branch_pattern contém placeholders inválidos.") from exc
    if any(field not in (None, "ticket", "slug") or spec or conversion for _, field, spec, conversion in fields):
        raise KitError("git.branch_pattern aceita somente {ticket} e {slug}, sem formatação.")
    repository = config["git"].get("repository")
    if repository is not None and (not isinstance(repository, str) or not repository.strip()):
        raise KitError("git.repository deve ser texto preenchido ou null.")
    for key in ("plans", "status"):
        relative_path(required_string(config["paths"], key))
    if config["tracking"].get("provider") not in ("none", "github", "clickup"):
        raise KitError("tracking.provider deve ser none, github ou clickup.")
    for key in ("list_id", "workspace_id"):
        value = config["tracking"].get(key)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise KitError(f"tracking.{key} deve ser texto preenchido ou null.")
    statuses = config["tracking"].get("statuses", {})
    if not isinstance(statuses, dict) or any(key not in ("pending", "in_progress", "done") or
            not isinstance(value, str) or not value.strip() for key, value in statuses.items()):
        raise KitError("tracking.statuses deve mapear pending/in_progress/done para nomes preenchidos.")
    if not isinstance(config["delivery"].get("create_pr"), bool):
        raise KitError("delivery.create_pr deve ser boolean.")
    if not isinstance(config.get("context"), list):
        raise KitError("context deve ser uma lista de caminhos.")
    for name in config["context"]:
        relative_path(name)
    for tool, settings in config["models"].items():
        if tool not in TOOLS or not isinstance(settings, dict):
            raise KitError(f"Configuração de modelos inválida: {tool}")
        for role, value in settings.items():
            if role not in ROLES:
                raise KitError(f"Modelo inválido: {tool}.{role}")
            model_options(tool, value)
    commands = config.get("validation")
    if not isinstance(commands, list):
        raise KitError("validation deve ser uma lista.")
    ids = set()
    for command in commands:
        if not isinstance(command, dict):
            raise KitError("Cada validação deve ser um objeto.")
        name = required_string(command, "id")
        if name in ids:
            raise KitError(f"Validação duplicada: {name}")
        ids.add(name)
        relative_path(required_string(command, "cwd"))
        argv = command.get("argv")
        if not isinstance(argv, list) or not argv or not all(isinstance(arg, str) and arg for arg in argv):
            raise KitError(f"argv inválido em {name}.")
        if not isinstance(command.get("required"), bool):
            raise KitError(f"required inválido em {name}.")
        if not isinstance(command.get("surfaces"), list) or not command["surfaces"] or not all(isinstance(s, str) and s for s in command["surfaces"]):
            raise KitError(f"surfaces inválido em {name}.")
        if not isinstance(command.get("requires"), list) or not all(isinstance(s, str) for s in command["requires"]):
            raise KitError(f"requires inválido em {name}.")
    return config


def frontmatter(text):
    if not text.startswith("---\n"):
        raise KitError("Frontmatter ausente.")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise KitError("Frontmatter incompleto.")
    values = {}
    for line in parts[1].splitlines():
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep or not value.strip():
            raise KitError(f"Frontmatter simples inválido: {line}")
        value = value.strip()
        values[key] = json.loads(value) if value.startswith('"') else value
    for key in ("name", "description"):
        if not isinstance(values.get(key), str) or not values[key]:
            raise KitError(f"Frontmatter exige {key}.")
    return values, parts[2].lstrip()


def block_part(text):
    if BEGIN not in text and END not in text:
        return None
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise KitError("Bloco specdev ausente, duplicado ou incompleto.")
    start, end = text.index(BEGIN), text.index(END) + len(END)
    if end <= start:
        raise KitError("Marcadores specdev fora de ordem.")
    return text[start:end]


def with_block(text, block):
    previous = block_part(text)
    newline = "\r\n" if "\r\n" in (previous if previous is not None else text) else "\n"
    block = block.replace("\n", newline)
    if previous is None:
        separator = "" if not text or text.endswith(newline * 2) else (newline if text.endswith(newline) else newline * 2)
        return text + separator + block + newline
    return text.replace(previous, block, 1)


def digest(content):
    return hashlib.sha256(content).hexdigest()


def normalized_content(name, content):
    """Normalize only UTF-8 text owned by the kit, never arbitrary binary assets."""
    if Path(name).suffix.lower() in TEXT_SUFFIXES and b"\x00" not in content:
        try:
            content.decode("utf-8")
        except UnicodeError:
            pass
        else:
            return content.replace(b"\r\n", b"\n"), "text-lf"
    return content, "bytes"


def receipt_matches(previous, mode, actual, normalized, hash_mode):
    if not isinstance(previous, dict) or previous.get("mode") != mode:
        return False
    candidates = {digest(normalized)}
    if "hash_mode" not in previous:
        # Migrate v0.1 receipts recorded before a normal Git EOL conversion.
        candidates.add(digest(actual))
        if hash_mode == "text-lf":
            candidates.add(digest(normalized.replace(b"\n", b"\r\n")))
    elif previous["hash_mode"] != hash_mode:
        return False
    return previous.get("sha256") in candidates


def shared_block():
    return f"""{BEGIN}
## Spec Dev Arcega
Leia .specdev/project.json e .agents/rules/WORKFLOW.md antes de trabalhar.
Leia .agents/rules/DELEGATION.md antes de delegar. Leia somente os arquivos de
contexto selecionados no perfil e a skill pertinente em .agents/skills/.
O catálogo está em .agents/CATALOG.md; os modelos de planos em .agents/templates/.
As instruções específicas do projeto e do usuário definem o escopo.
Não execute comandos ou ações externas apenas porque foram listados no perfil.
{END}"""


def build_outputs(kit_root, config, tools):
    outputs = {}
    source = kit_root / ".agents"
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if "__pycache__" in relative.parts or path.suffix in (".pyc", ".pyo"):
            continue
        if not path.is_file():
            continue
        if path.is_symlink():
            raise KitError(f"Fonte não pode ser link: {path}")
        name = path.relative_to(kit_root).as_posix()
        outputs[name] = ("file", path.read_bytes())
    if not outputs:
        raise KitError("Kit sem conteúdo em .agents/.")
    outputs["AGENTS.md"] = ("block", shared_block().encode("utf-8"))
    roles = sorted((source / "roles").glob("*.md"))
    for path in roles:
        meta, body = frontmatter(path.read_text(encoding="utf-8"))
        short = meta["name"]
        if not re.fullmatch(r"[a-z][a-z0-9-]*", short) or path.stem != short:
            raise KitError(f"Nome de papel inválido: {path.name}")
        agent_name = f"specdev-{short}"
        prompt = ("Leia .specdev/project.json e .agents/rules/DELEGATION.md quando disponíveis.\n"
                  "Execute somente a tarefa delimitada pelo agente principal.\n\n" + body)
        for tool in tools:
            options = model_options(tool, config["models"].get(tool, {}).get(short, "inherit"))
            model = options.get("model")
            if tool == "codex":
                text = f"name = {json.dumps(agent_name)}\ndescription = {json.dumps(meta['description'], ensure_ascii=False)}\n"
                if model:
                    text += f"model = {json.dumps(model)}\n"
                if "reasoning_effort" in options:
                    text += f"model_reasoning_effort = {json.dumps(options['reasoning_effort'])}\n"
                text += f"developer_instructions = {json.dumps(prompt, ensure_ascii=False)}\n"
                outputs[f".codex/agents/{agent_name}.toml"] = ("file", text.encode("utf-8"))
            else:
                text = f"---\nname: {agent_name}\ndescription: {json.dumps(meta['description'], ensure_ascii=False)}\n"
                if model:
                    text += f"model: {json.dumps(model)}\n"
                if "tools" in options:
                    text += f"tools: {', '.join(options['tools'])}\n"
                if tool == "cursor" and short != "worker":
                    text += "readonly: true\n"
                text += "---\n\n" + prompt
                outputs[f".{tool}/agents/{agent_name}.md"] = ("file", text.encode("utf-8"))
    if "cursor" in tools:
        text = """---
description: Entrada compartilhada do Spec Dev Arcega
alwaysApply: true
---

Leia AGENTS.md e .specdev/project.json. Siga .agents/rules/WORKFLOW.md.
As skills canônicas estão em .agents/skills/; consulte .agents/CATALOG.md.
Antes de delegar, leia .agents/rules/DELEGATION.md.
"""
        outputs[".cursor/rules/specdev.mdc"] = ("file", text.encode("utf-8"))
    if "claude" in tools:
        block = f"{BEGIN}\n## Spec Dev Arcega\n@AGENTS.md\n\nSkills compartilhadas: .agents/skills/. Catálogo: .agents/CATALOG.md.\n{END}"
        outputs["CLAUDE.md"] = ("block", block.encode("utf-8"))
        for name, value in list(outputs.items()):
            if name.startswith(".agents/skills/"):
                outputs[".claude/skills/" + name.removeprefix(".agents/skills/")] = value
    return outputs


def load_state(target, profile, tools, kit_root):
    config_path = safe_path(target, CONFIG)
    manifest_path = safe_path(target, MANIFEST)
    manifest = read_json(manifest_path) if manifest_path.exists() else None
    if manifest is not None and (not isinstance(manifest, dict) or manifest.get("schema_version") != 1 or
                                 not isinstance(manifest.get("files"), dict) or
                                 not isinstance(manifest.get("tools"), list) or
                                 any(tool not in TOOLS for tool in manifest["tools"])):
        raise KitError("Manifest inválido.")
    if config_path.exists():
        if profile:
            raise KitError("Projeto já configurado: edite .specdev/project.json; não reaplique --profile.")
        config = validate_config(read_json(config_path))
    else:
        candidate = kit_root / "profiles" / f"{profile or 'generic'}.json"
        if not re.fullmatch(r"[a-z0-9-]+", profile or "generic") or not candidate.is_file():
            raise KitError(f"Perfil desconhecido: {profile}")
        config = read_json(candidate)
        config["project"]["name"] = target.name
        validate_config(config)
    selected = list(dict.fromkeys(tools or (manifest["tools"] if manifest else TOOLS)))
    if manifest and not set(manifest["tools"]).issubset(selected):
        raise KitError("Remover adaptadores exige remoção manual dos arquivos gerados; a instalação não apaga arquivos.")
    return config, manifest, selected, not config_path.exists()


def plan_install(target, config, manifest, tools, new_config, kit_root):
    outputs = build_outputs(kit_root, config, tools)
    for name in config["context"]:
        if name not in outputs and not safe_path(target, name).exists():
            raise KitError(f"Documento de contexto não encontrado: {name}")
    entries, changes, conflicts = {}, [], []
    for name, (mode, content) in outputs.items():
        path = safe_path(target, name)
        raw = path.read_bytes() if path.exists() else None
        actual = raw
        desired = content
        if mode == "block":
            try:
                text = raw.decode("utf-8-sig") if raw is not None else ""
                part = block_part(text)
            except (UnicodeError, KitError) as exc:
                conflicts.append(f"{name}: {exc}")
                continue
            actual = part.replace("\r\n", "\n").encode("utf-8") if part is not None else None
            desired = with_block(text, content.decode("utf-8")).encode("utf-8")
            if raw and raw.startswith(b"\xef\xbb\xbf"):
                desired = b"\xef\xbb\xbf" + desired
        canonical, hash_mode = normalized_content(name, content)
        normalized = normalized_content(name, actual)[0] if actual is not None else None
        previous = (manifest or {}).get("files", {}).get(name)
        expected = digest(canonical)
        entries[name] = {"mode": mode, "sha256": expected, "hash_mode": hash_mode}
        # An identical file can be adopted. Other existing files require a matching receipt.
        if actual is not None and normalized != canonical:
            if not receipt_matches(previous, mode, actual, normalized, hash_mode):
                conflicts.append(f"{name}: conteúdo local não gerenciado ou modificado.")
                continue
        if mode == "file" and raw is not None and hash_mode == "text-lf":
            # Keep the consumer's EOL and avoid writing when only EOL differs.
            desired = raw if normalized == canonical else canonical
            if normalized != canonical and b"\r\n" in raw:
                desired = canonical.replace(b"\n", b"\r\n")
        if raw != desired:
            changes.append((name, desired))
    if new_config:
        changes.append((CONFIG, json_text(config).encode("utf-8")))
    metadata = read_json(kit_root / "kit.json")
    lock = {"schema_version": 1, "kit": metadata["name"], "version": metadata["version"],
            "tools": tools, "files": entries}
    lock_content = json_text(lock).encode("utf-8")
    manifest_path = safe_path(target, MANIFEST)
    if not manifest_path.exists() or normalized_content(MANIFEST, manifest_path.read_bytes())[0] != lock_content:
        changes.append((MANIFEST, lock_content))
    return changes, conflicts


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temporary.open("xb") as handle:
            handle.write(data)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def install(target, profile=None, tools=None, dry_run=False, kit_root=ROOT):
    target = target.absolute()
    if target.exists() and not target.is_dir():
        raise KitError("O destino deve ser um diretório.")
    if target.is_symlink() or getattr(target, "is_junction", lambda: False)():
        raise KitError("A raiz do destino não pode ser link/junction.")
    config, manifest, selected, new_config = load_state(target, profile, tools, kit_root)
    changes, conflicts = plan_install(target, config, manifest, selected, new_config, kit_root)
    if conflicts:
        raise KitError("Instalação interrompida antes de gravar:\n" + "\n".join(conflicts))
    result = {"version": read_json(kit_root / "kit.json")["version"], "tools": selected,
              "dry_run": dry_run, "changed": [name for name, _ in changes], "backup": None}
    if dry_run or not changes:
        return result
    lock_path = safe_path(target, ".specdev/install.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise KitError("Outra instalação está em andamento (.specdev/install.lock).") from exc
    try:
        os.close(descriptor)
        # Recheck under the exclusive lock before touching any managed file.
        fresh_config, fresh_manifest, fresh_tools, fresh_new = load_state(target, profile, tools, kit_root)
        fresh_changes, fresh_conflicts = plan_install(target, fresh_config, fresh_manifest, fresh_tools, fresh_new, kit_root)
        if fresh_conflicts or fresh_changes != changes or fresh_tools != selected:
            raise KitError("Destino mudou durante a instalação. Execute a simulação novamente.")
        backup_id = uuid.uuid4().hex
        for name, _ in changes:
            path = safe_path(target, name)
            if path.exists():
                backup = safe_path(target, f".specdev/backups/{backup_id}/{name}")
                atomic_write(backup, path.read_bytes())
                result["backup"] = f".specdev/backups/{backup_id}"
        for name, content in changes:
            atomic_write(safe_path(target, name), content)
    finally:
        lock_path.unlink()
    return result


def check(target, kit_root=ROOT):
    target = target.absolute()
    if not safe_path(target, CONFIG).exists() or not safe_path(target, MANIFEST).exists():
        raise KitError("Projeto ainda não instalado.")
    config, manifest, tools, new_config = load_state(target, None, None, kit_root)
    changes, conflicts = plan_install(target, config, manifest, tools, new_config, kit_root)
    messages = conflicts + [f"Desatualizado/ausente: {name}" for name, _ in changes]
    warnings = []
    if not config["validation"]:
        warnings.append("Nenhuma validação configurada; configure os comandos antes de implementar tickets.")
    return {"ok": not messages, "issues": messages, "warnings": warnings}


def configuration_warnings(config):
    known = {
        "project": {"name", "language"},
        "git": {"remote", "repository", "base_branch", "branch_pattern"},
        "paths": {"plans", "status"},
        "tracking": {"provider", "list_id", "workspace_id", "statuses"},
        "delivery": {"create_pr"},
    }
    warnings = [f"Campo desconhecido preservado: {key}" for key in config if key not in
                {*known, "schema_version", "context", "validation", "models"}]
    for section, fields in known.items():
        warnings.extend(f"Campo desconhecido preservado: {section}.{key}" for key in config[section] if key not in fields)
    for command in config["validation"]:
        warnings.extend(f"Campo desconhecido preservado: validation.{command['id']}.{key}" for key in command if key not in
                        {"id", "cwd", "argv", "surfaces", "requires", "required"})
    return warnings


def find_executable(executable, cwd):
    """Resolve PATH relative to the declared cwd, without changing process state."""
    program = Path(executable)
    if program.is_absolute() or "/" in executable or "\\" in executable:
        candidates = [program if program.is_absolute() else cwd / program]
    else:
        paths = os.environ.get("PATH", os.defpath).split(os.pathsep)
        if os.name == "nt" and "NoDefaultCurrentDirectoryInExePath" not in os.environ:
            paths.insert(0, str(cwd))
        candidates = [(Path(path) if Path(path).is_absolute() else cwd / path) / program for path in paths]
    extensions = [""]
    if os.name == "nt":
        extensions.extend(extension for extension in os.environ.get("PATHEXT", ".COM;.EXE;.BAT;.CMD").split(";") if extension)
    for candidate in candidates:
        for extension in extensions:
            path = Path(str(candidate) + extension)
            if path.is_file() and os.access(path, os.F_OK | os.X_OK):
                return str(path.resolve())
    return None


def doctor(target, surfaces=None, kit_root=ROOT):
    """Inspect configuration and local command availability without running programs."""
    target = target.absolute()
    configuration = {"ready": False, "issues": [], "warnings": []}
    environment = {"ready": False, "commands": [], "executed": False}
    result = {"ok": False, "integrity": {"ok": False, "issues": []},
              "configuration": configuration, "environment": environment,
              "limitations": ["Não executa comandos, testes, Git ou serviços externos.",
                              "requires exige verificação na tarefa; disponibilidade não comprova testes verdes.",
                              "Modelos, autenticação e descoberta nos clientes não são verificados online."]}
    try:
        config = validate_config(read_json(safe_path(target, CONFIG)))
    except (KitError, OSError) as exc:
        configuration["issues"].append(str(exc))
        return result
    try:
        result["integrity"] = check(target, kit_root)
    except (KitError, OSError) as exc:
        result["integrity"]["issues"].append(str(exc))
    configuration["warnings"] = configuration_warnings(config)
    commands = [command for command in config["validation"]
                if not surfaces or set(surfaces).intersection(command["surfaces"])]
    if not commands:
        configuration["issues"].append("Nenhuma validação configurada para as superfícies selecionadas.")
    if surfaces:
        covered = {surface for command in commands for surface in command["surfaces"]}
        configuration["issues"].extend(f"Superfície sem validação: {surface}" for surface in surfaces if surface not in covered)
    if config["project"]["name"] == "configure-me":
        configuration["issues"].append("Configure project.name para este projeto.")
    if config["tracking"]["provider"] == "clickup":
        for key in ("list_id", "workspace_id"):
            if not config["tracking"].get(key):
                configuration["issues"].append(f"Resolva tracking.{key} antes de usar ClickUp.")
    configuration["ready"] = not configuration["issues"]
    required_ready = True
    for command in commands:
        entry = {"id": command["id"], "cwd": command["cwd"], "argv": command["argv"],
                 "required": command["required"], "requires": command["requires"], "status": "available"}
        try:
            cwd = safe_path(target, command["cwd"], directory=True)
            if not cwd.is_dir():
                raise KitError(f"Diretório não encontrado: {command['cwd']}")
            executable = command["argv"][0]
            resolved = find_executable(executable, cwd)
            entry["executable"] = resolved
            if resolved is None:
                raise KitError(f"Executável não encontrado: {executable}")
            if command["requires"]:
                entry["status"] = "requires_verification"
        except (KitError, OSError) as exc:
            entry["status"] = "unavailable"
            entry["reason"] = str(exc)
        if command["required"] and entry["status"] != "available":
            required_ready = False
        environment["commands"].append(entry)
    environment["ready"] = bool(commands) and required_ready
    result["ok"] = result["integrity"]["ok"] and configuration["ready"] and environment["ready"]
    return result


def validate_kit(kit_root=ROOT):
    skills = []
    for path in sorted((kit_root / ".agents/skills").glob("*/SKILL.md")):
        meta, _ = frontmatter(path.read_text(encoding="utf-8"))
        if meta["name"] != path.parent.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", meta["name"]):
            raise KitError(f"Nome de skill inválido: {path}")
        skills.append(meta["name"])
    if not skills:
        raise KitError("Nenhuma skill encontrada.")
    for profile in (kit_root / "profiles").glob("*.json"):
        config = validate_config(read_json(profile))
        build_outputs(kit_root, config, TOOLS)
    return {"ok": True, "skills": skills}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    command = subs.add_parser("install", help="Instala ou atualiza sem sobrescrever alterações locais.")
    command.add_argument("--target", type=Path, required=True)
    command.add_argument("--profile", help="generic, python ou dotnet-angular; apenas na primeira instalação.")
    command.add_argument("--tools", nargs="+", choices=TOOLS)
    command.add_argument("--dry-run", action="store_true")
    command = subs.add_parser("check", help="Confere configuração, integridade e versão.")
    command.add_argument("--target", type=Path, required=True)
    command = subs.add_parser("doctor", help="Diagnóstico read-only de integridade, configuração e disponibilidade local.")
    command.add_argument("--target", type=Path, required=True)
    command.add_argument("--surfaces", nargs="+", help="Superfícies de validação a diagnosticar; padrão: todas.")
    subs.add_parser("validate", help="Valida as skills e os perfis do kit.")
    args = parser.parse_args(argv)
    try:
        if args.command == "install":
            result = install(args.target, args.profile, args.tools, args.dry_run)
        elif args.command == "check":
            result = check(args.target)
        elif args.command == "doctor":
            result = doctor(args.target, args.surfaces)
        else:
            result = validate_kit()
        print(json_text(result), end="")
        return 0 if result.get("ok", True) else 1
    except (KitError, OSError, UnicodeError, ValueError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
