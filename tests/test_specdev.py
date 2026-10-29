"""Behavioral tests: all consumer data lives in disposable temporary directories."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


kit = module_at("specdev", ROOT / "scripts/specdev.py")
review = module_at("validate_review", ROOT / ".agents/skills/review-changes/scripts/validate_review.py")


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="specdev-test-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.target = self.base / "consumer with spaces"
        self.source = self.base / "kit"
        self.source.mkdir()
        shutil.copytree(ROOT / ".agents", self.source / ".agents", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(ROOT / "profiles", self.source / "profiles")
        shutil.copy2(ROOT / "kit.json", self.source / "kit.json")

    def install(self, **kwargs):
        return kit.install(self.target, kit_root=self.source, **kwargs)

    def config(self):
        return kit.read_json(self.target / kit.CONFIG)

    def write_config(self, value):
        (self.target / kit.CONFIG).write_text(kit.json_text(value), encoding="utf-8")

    def snapshot(self):
        if not self.target.exists():
            return {}
        return {p.relative_to(self.target).as_posix(): p.read_bytes()
                for p in self.target.rglob("*") if p.is_file()}

    def test_dry_run_does_not_create_target(self):
        result = self.install(dry_run=True)
        self.assertTrue(result["changed"])
        self.assertFalse(self.target.exists())

    def test_install_generates_native_formats_for_three_clients(self):
        self.install()
        for role in ("explorer", "worker", "reviewer", "investigator"):
            name = f"specdev-{role}"
            codex = tomllib.loads((self.target / f".codex/agents/{name}.toml").read_text(encoding="utf-8"))
            self.assertEqual(codex["name"], name)
            self.assertTrue(codex["developer_instructions"])
            self.assertNotIn("model", codex)
            for tool in ("cursor", "claude"):
                meta, body = kit.frontmatter((self.target / f".{tool}/agents/{name}.md").read_text(encoding="utf-8"))
                self.assertEqual(meta["name"], name)
                self.assertTrue(body)
        self.assertTrue((self.target / ".cursor/rules/specdev.mdc").is_file())
        self.assertIn("@AGENTS.md", (self.target / "CLAUDE.md").read_text(encoding="utf-8"))
        for path in (self.source / ".agents/skills").rglob("*"):
            if path.is_file():
                relative = path.relative_to(self.source / ".agents/skills")
                self.assertEqual(path.read_bytes(), (self.target / ".claude/skills" / relative).read_bytes())

    def test_reinstall_is_idempotent(self):
        self.install()
        before = self.snapshot()
        self.assertEqual(self.install()["changed"], [])
        self.assertEqual(before, self.snapshot())
        self.assertTrue(kit.check(self.target, self.source)["ok"])

    def test_english_update_preserves_consumer_language_and_local_instructions(self):
        self.install()
        config = self.config()
        config["project"]["language"] = "pt-BR"
        self.write_config(config)
        config_bytes = (self.target / kit.CONFIG).read_bytes()
        instructions = self.target / "AGENTS.md"
        previous_block = f"{kit.BEGIN}\n## Spec Dev Arcega\nRead the old shared instructions.\n{kit.END}"
        instructions.write_text("# Local instructions\n\nKeep our conventions.\n\n" + previous_block + "\n", encoding="utf-8")
        skill_name = ".agents/skills/setup-project/SKILL.md"
        skill = self.target / skill_name
        previous_skill = b"---\nname: setup-project\ndescription: Old workflow\n---\n\nOld instructions.\n"
        skill.write_bytes(previous_skill)
        manifest_path = self.target / kit.MANIFEST
        manifest = kit.read_json(manifest_path)
        manifest["files"]["AGENTS.md"]["sha256"] = kit.digest(previous_block.encode("utf-8"))
        manifest["files"][skill_name]["sha256"] = kit.digest(previous_skill)
        manifest_path.write_text(kit.json_text(manifest), encoding="utf-8")

        result = self.install()
        self.assertIn("AGENTS.md", result["changed"])
        self.assertIn(skill_name, result["changed"])
        self.assertEqual((self.target / kit.CONFIG).read_bytes(), config_bytes)
        self.assertEqual(self.config()["project"]["language"], "pt-BR")
        self.assertTrue(instructions.read_text(encoding="utf-8").startswith("# Local instructions\n\nKeep our conventions."))
        self.assertEqual(skill.read_bytes(), (self.source / skill_name).read_bytes())
        self.assertTrue(kit.check(self.target, self.source)["ok"])

    def test_new_profiles_default_to_english(self):
        for profile in ("generic", "python", "dotnet-angular", "node", "react", "node-react"):
            with self.subTest(profile=profile):
                config = kit.read_json(self.source / "profiles" / f"{profile}.json")
                self.assertEqual(config["project"]["language"], "en")

    def test_setup_resources_are_distributed_without_starting_setup(self):
        self.install(tools=["codex", "cursor", "claude"])
        skill = ".agents/skills/setup-project"
        for relative in ("SKILL.md", "references/questions.md", "assets/project-context.md"):
            canonical = (self.target / skill / relative).read_bytes()
            self.assertEqual(canonical, (self.source / skill / relative).read_bytes())
            self.assertEqual(canonical, (self.target / ".claude/skills/setup-project" / relative).read_bytes())
        self.assertFalse((self.target / ".specdev/setup-state.json").exists())
        self.assertFalse((self.target / "docs/PROJECT_CONTEXT.md").exists())
        manifest = kit.read_json(self.target / kit.MANIFEST)
        self.assertNotIn(".specdev/setup-state.json", manifest["files"])
        self.assertNotIn("docs/PROJECT_CONTEXT.md", manifest["files"])

    def test_setup_consumer_data_survives_skill_updates(self):
        self.install()
        state = self.target / ".specdev/setup-state.json"
        state.write_text('{"schema_version":1,"status":"in_progress","next_question":"validation"}\n', encoding="utf-8")
        context = self.target / "docs/PROJECT_CONTEXT.md"
        context.parent.mkdir()
        context.write_text("# Consumer-owned context\n\nExisting team notes.\n", encoding="utf-8")
        config = self.config()
        config["context"].append("docs/PROJECT_CONTEXT.md")
        self.write_config(config)
        original = (state.read_bytes(), context.read_bytes(), (self.target / kit.CONFIG).read_bytes())
        source = self.source / ".agents/skills/setup-project/SKILL.md"
        source.write_bytes(source.read_bytes() + b"\nUpdated kit workflow.\n")
        result = self.install()
        self.assertIn(".agents/skills/setup-project/SKILL.md", result["changed"])
        self.assertIn(".claude/skills/setup-project/SKILL.md", result["changed"])
        self.assertEqual(original, (state.read_bytes(), context.read_bytes(), (self.target / kit.CONFIG).read_bytes()))
        self.assertTrue(kit.check(self.target, self.source)["ok"])

    def test_node_and_react_profiles_install_and_preserve_consumer_architecture(self):
        contexts = {
            "node": [".agents/context/node.md"],
            "react": [".agents/context/react.md"],
            "node-react": [".agents/context/node.md", ".agents/context/react.md"],
        }
        for name, selected in contexts.items():
            with self.subTest(profile=name):
                target = self.base / name
                kit.install(target, profile=name, kit_root=self.source)
                config = kit.read_json(target / kit.CONFIG)
                self.assertEqual(config["context"], selected)
                self.assertEqual(config["validation"], [])
                self.assertTrue(all((target / path).is_file() for path in selected))
                context = target / "docs/PROJECT_CONTEXT.md"
                context.parent.mkdir()
                context.write_text("# Local architecture\nService A must not import service B.\n", encoding="utf-8")
                config["context"].append("docs/PROJECT_CONTEXT.md")
                (target / kit.CONFIG).write_text(kit.json_text(config), encoding="utf-8")
                before = (context.read_bytes(), (target / kit.CONFIG).read_bytes())
                kit.install(target, kit_root=self.source)
                self.assertEqual(before, (context.read_bytes(), (target / kit.CONFIG).read_bytes()))
                self.assertNotIn("docs/PROJECT_CONTEXT.md", kit.read_json(target / kit.MANIFEST)["files"])
                self.assertTrue(kit.check(target, self.source)["ok"])

    def test_crlf_checkout_is_clean_and_updates_keep_eol(self):
        self.install()
        names = (".agents/rules/WORKFLOW.md", ".codex/agents/specdev-reviewer.toml", kit.MANIFEST)
        for name in names:
            path = self.target / name
            path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        before = self.snapshot()
        self.assertTrue(kit.check(self.target, self.source)["ok"])
        self.assertEqual(self.install()["changed"], [])
        self.assertEqual(before, self.snapshot())
        source = self.source / names[0]
        source.write_bytes(source.read_bytes() + b"\nUpdated agreement.\n")
        self.install()
        updated = (self.target / names[0]).read_bytes()
        self.assertIn(b"Updated agreement.\r\n", updated)
        self.assertNotIn(b"\n", updated.replace(b"\r\n", b""))
        self.assertTrue(kit.check(self.target, self.source)["ok"])

    def test_legacy_receipts_migrate_after_eol_conversion_without_losing_edits(self):
        self.install()
        name = ".agents/rules/WORKFLOW.md"
        path = self.target / name
        original = path.read_bytes().replace(b"\r\n", b"\n")
        manifest = kit.read_json(self.target / kit.MANIFEST)
        for entry in manifest["files"].values():
            entry.pop("hash_mode", None)
        manifest["files"][name]["sha256"] = kit.digest(original)
        (self.target / kit.MANIFEST).write_text(kit.json_text(manifest), encoding="utf-8")
        path.write_bytes(original.replace(b"\n", b"\r\n"))
        (self.source / name).write_bytes(original + b"New agreement.\n")
        self.install()
        self.assertIn(b"New agreement.\r\n", path.read_bytes())
        path.write_bytes(path.read_bytes() + b"Local change.\r\n")
        before = self.snapshot()
        with self.assertRaises(kit.KitError):
            self.install()
        self.assertEqual(before, self.snapshot())

    def test_binary_assets_remain_byte_exact(self):
        source = self.source / ".agents/binary.dat"
        source.write_bytes(b"\x00\r\n\xff")
        self.install()
        target = self.target / ".agents/binary.dat"
        self.assertEqual(target.read_bytes(), source.read_bytes())
        target.write_bytes(b"\x00\n\xff")
        with self.assertRaises(kit.KitError):
            self.install()

    def test_local_bytecode_does_not_enter_consumer_or_manifest(self):
        cache = self.source / ".agents/skills/review-changes/scripts/__pycache__"
        cache.mkdir()
        (cache / "validate_review.cpython-314.pyc").write_bytes(b"Local interpreter cache.")
        self.install()
        manifest = kit.read_json(self.target / kit.MANIFEST)
        self.assertFalse(any("__pycache__" in name or name.endswith(".pyc") for name in manifest["files"]))
        self.assertFalse(any("__pycache__" in str(path) for path in self.target.rglob("*")))

    def test_subset_installs_only_requested_client(self):
        self.install(tools=["cursor"])
        self.assertTrue((self.target / ".cursor").exists())
        self.assertFalse((self.target / ".codex").exists())
        self.assertFalse((self.target / ".claude").exists())
        self.assertFalse((self.target / "CLAUDE.md").exists())

    def test_existing_instructions_are_preserved_including_bom(self):
        self.target.mkdir()
        original = b"\xef\xbb\xbf# Local\r\n\r\nUse local tests.\r\n"
        (self.target / "AGENTS.md").write_bytes(original)
        (self.target / "CLAUDE.md").write_text("# Claude local\n", encoding="utf-8")
        self.install()
        self.assertTrue((self.target / "AGENTS.md").read_bytes().startswith(original))
        self.assertTrue((self.target / "CLAUDE.md").read_text(encoding="utf-8").startswith("# Claude local\n"))
        self.assertEqual(self.install()["changed"], [])

    def test_outside_block_edits_survive_updates(self):
        self.install()
        path = self.target / "AGENTS.md"
        path.write_text("# Custom instructions\n\n" + path.read_text(encoding="utf-8") + "\nKeep this footer.\n", encoding="utf-8")
        self.assertEqual(self.install()["changed"], [])
        self.assertTrue(kit.check(self.target, self.source)["ok"])
        self.assertIn("Keep this footer.", path.read_text(encoding="utf-8"))

    def test_modified_managed_file_blocks_every_write(self):
        self.install()
        path = self.target / ".agents/rules/WORKFLOW.md"
        path.write_text("Local customization.\n", encoding="utf-8")
        config = self.config()
        config["models"]["codex"]["reviewer"] = "some-local-model"
        self.write_config(config)
        before = self.snapshot()
        with self.assertRaises(kit.KitError):
            self.install()
        self.assertEqual(before, self.snapshot())
        self.assertFalse(kit.check(self.target, self.source)["ok"])

    def test_first_install_collision_blocks_before_config_creation(self):
        path = self.target / ".cursor/agents/specdev-worker.md"
        path.parent.mkdir(parents=True)
        path.write_text("Existing agent owned by project.\n", encoding="utf-8")
        before = self.snapshot()
        with self.assertRaises(kit.KitError):
            self.install()
        self.assertEqual(before, self.snapshot())

    def test_modified_managed_block_blocks_update(self):
        self.install()
        path = self.target / "AGENTS.md"
        path.write_text(path.read_text(encoding="utf-8").replace("## Spec Dev Arcega", "## Customized"), encoding="utf-8")
        before = self.snapshot()
        with self.assertRaises(kit.KitError):
            self.install()
        self.assertEqual(before, self.snapshot())

    def test_malformed_markers_block_without_overwriting(self):
        self.target.mkdir()
        path = self.target / "AGENTS.md"
        path.write_text("# Local\n" + kit.BEGIN, encoding="utf-8")
        before = self.snapshot()
        with self.assertRaises(kit.KitError):
            self.install()
        self.assertEqual(before, self.snapshot())

    def test_update_backs_up_and_preserves_project_config(self):
        self.install()
        config_path = self.target / kit.CONFIG
        config_path.write_text(config_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        local_config = config_path.read_bytes()
        name = ".agents/rules/WORKFLOW.md"
        old = (self.target / name).read_bytes()
        (self.source / name).write_bytes(old + b"\nNew kit agreement.\n")
        result = self.install()
        self.assertIn(name, result["changed"])
        self.assertEqual((self.target / result["backup"] / name).read_bytes(), old)
        self.assertEqual(config_path.read_bytes(), local_config)
        self.assertTrue(kit.check(self.target, self.source)["ok"])

    def test_custom_models_are_applied_per_client(self):
        self.install()
        config = self.config()
        config["models"]["codex"]["reviewer"] = "codex-account-model"
        config["models"]["claude"]["reviewer"] = "claude-account-model"
        self.write_config(config)
        self.install()
        codex = tomllib.loads((self.target / ".codex/agents/specdev-reviewer.toml").read_text(encoding="utf-8"))
        claude, _ = kit.frontmatter((self.target / ".claude/agents/specdev-reviewer.md").read_text(encoding="utf-8"))
        cursor, _ = kit.frontmatter((self.target / ".cursor/agents/specdev-reviewer.md").read_text(encoding="utf-8"))
        self.assertEqual(codex["model"], "codex-account-model")
        self.assertEqual(claude["model"], "claude-account-model")
        self.assertNotIn("model", cursor)

    def test_native_agent_options_preserve_defaults_and_limit_tools(self):
        self.install()
        config = self.config()
        config["models"]["codex"]["reviewer"] = {"model": "account-model", "reasoning_effort": "high"}
        config["models"]["claude"]["explorer"] = {"model": "inherit", "tools": ["Read", "Grep", "Glob"]}
        self.write_config(config)
        self.install()
        codex = tomllib.loads((self.target / ".codex/agents/specdev-reviewer.toml").read_text(encoding="utf-8"))
        self.assertEqual(codex["model_reasoning_effort"], "high")
        self.assertEqual(codex["model"], "account-model")
        claude, _ = kit.frontmatter((self.target / ".claude/agents/specdev-explorer.md").read_text(encoding="utf-8"))
        self.assertEqual(claude["tools"], "Read, Grep, Glob")
        self.assertNotIn("model", claude)
        worker = tomllib.loads((self.target / ".codex/agents/specdev-worker.toml").read_text(encoding="utf-8"))
        self.assertNotIn("model_reasoning_effort", worker)
        self.assertNotIn("tools", (self.target / ".claude/agents/specdev-worker.md").read_text(encoding="utf-8"))
        self.assertTrue(kit.check(self.target, self.source)["ok"])

    def test_invalid_native_options_and_profile_types_are_rejected(self):
        cases = [
            ("codex", {"reasoning_effort": []}), ("codex", {"reasoning_effort": "unknown"}),
            ("cursor", {"reasoning_effort": "high"}), ("claude", {"tools": []}),
            ("claude", {"tools": ["Bash(git push *)"]}), ("claude", {"sandbox_mode": "read-only"}),
        ]
        for tool, value in cases:
            config = kit.read_json(self.source / "profiles/generic.json")
            config["models"][tool]["reviewer"] = value
            with self.subTest(tool=tool, value=value), self.assertRaises(kit.KitError):
                kit.validate_config(config)
        for section, key, value in [("git", "branch_pattern", "{unknown}-{slug}"),
                                    ("git", "branch_pattern", "{ticket!r}"),
                                    ("git", "branch_pattern", "{ticket"),
                                    ("tracking", "list_id", 123), ("tracking", "statuses", []),
                                    ("tracking", "statuses", {"done": " "})]:
            config = kit.read_json(self.source / "profiles/generic.json")
            config[section][key] = value
            with self.subTest(field=key, value=value), self.assertRaises(kit.KitError):
                kit.validate_config(config)

    def test_doctor_distinguishes_integrity_from_missing_validation_without_writes(self):
        self.install(profile="generic")
        before = self.snapshot()
        result = kit.doctor(self.target, kit_root=self.source)
        self.assertTrue(result["integrity"]["ok"])
        self.assertFalse(result["configuration"]["ready"])
        self.assertFalse(result["ok"])
        self.assertEqual(before, self.snapshot())

    def test_doctor_inspects_commands_without_executing_them(self):
        self.install()
        marker = self.base / "doctor-must-not-execute"
        config = self.config()
        config["validation"] = [{"id": "safe", "cwd": ".",
            "argv": [sys.executable, "-c", f"open({str(marker)!r}, 'w').write('executed')"],
            "surfaces": ["tooling"], "requires": [], "required": True}]
        config["local_extension"] = {"preserve": True}
        self.write_config(config)
        before = self.snapshot()
        result = kit.doctor(self.target, ["tooling"], self.source)
        self.assertTrue(result["ok"], result)
        self.assertFalse(result["environment"]["executed"])
        self.assertEqual(result["environment"]["commands"][0]["status"], "available")
        self.assertTrue(result["configuration"]["warnings"])
        self.assertFalse(marker.exists())
        self.assertEqual(before, self.snapshot())
        self.assertFalse(kit.doctor(self.target, ["ui"], self.source)["ok"])

    def test_doctor_reports_missing_cwd_executable_and_unverified_prerequisites(self):
        self.install()
        config = self.config()
        config["validation"] = []
        for name, cwd, executable, requires, required in [
            ("missing-directory", "absent", sys.executable, [], True),
            ("missing-executable", ".", "specdev-executable-does-not-exist", [], True),
            ("integration", ".", sys.executable, ["Service must be running"], True),
            ("optional", ".", "specdev-executable-does-not-exist", [], False),
        ]:
            config["validation"].append({"id": name, "cwd": cwd, "argv": [executable],
                "surfaces": [name], "requires": requires, "required": required})
        self.write_config(config)
        before = self.snapshot()
        result = kit.doctor(self.target, kit_root=self.source)
        self.assertFalse(result["environment"]["ready"])
        self.assertEqual([entry["status"] for entry in result["environment"]["commands"]],
                         ["unavailable", "unavailable", "requires_verification", "unavailable"])
        self.assertTrue(kit.doctor(self.target, ["optional"], self.source)["ok"])
        self.assertEqual(before, self.snapshot())

    def test_doctor_reports_drift_and_cli_incomplete_configuration(self):
        self.install()
        (self.target / ".agents/rules/WORKFLOW.md").write_text("Local edit.\n", encoding="utf-8")
        result = kit.doctor(self.target, kit_root=self.source)
        self.assertFalse(result["integrity"]["ok"])
        self.assertFalse(result["ok"])
        missing = self.base / "not installed"
        cli = subprocess.run([sys.executable, str(ROOT / "scripts/specdev.py"), "doctor", "--target", str(missing)],
                             capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"})
        self.assertEqual(cli.returncode, 1)
        self.assertFalse(json.loads(cli.stdout)["configuration"]["ready"])
        self.assertFalse(missing.exists())

    def test_doctor_resolves_relative_path_from_validation_cwd(self):
        self.install()
        cwd = self.target / "validation area"
        binary = cwd / "bin" / ("specdev-probe.cmd" if os.name == "nt" else "specdev-probe")
        binary.parent.mkdir(parents=True)
        binary.write_text("exit 0\n", encoding="utf-8")
        binary.chmod(0o700)
        config = self.config()
        config["validation"] = [{"id": "relative-path", "cwd": "validation area", "argv": ["specdev-probe"],
                                 "surfaces": ["tooling"], "requires": [], "required": True}]
        self.write_config(config)
        original_cwd = Path.cwd()
        before = self.snapshot()
        with mock.patch.dict(os.environ, {"PATH": "bin"}):
            result = kit.doctor(self.target, kit_root=self.source)
            self.assertTrue(result["ok"], result)
            self.assertEqual(result["environment"]["commands"][0]["executable"], str(binary.resolve()))
            config["validation"][0]["cwd"] = "."
            self.write_config(config)
            self.assertFalse(kit.doctor(self.target, kit_root=self.source)["ok"])
            self.assertEqual(Path.cwd(), original_cwd)
            self.write_config({**config, "validation": [{**config["validation"][0], "cwd": "validation area"}]})
        self.assertEqual(before, self.snapshot())

    def test_tracking_without_statuses_remains_compatible(self):
        self.install()
        config = self.config()
        config["tracking"] = {"provider": "none"}
        self.write_config(config)
        before = (self.target / kit.CONFIG).read_bytes()
        self.assertEqual(self.install()["changed"], [])
        self.assertEqual(before, (self.target / kit.CONFIG).read_bytes())
        self.assertTrue(kit.check(self.target, self.source)["ok"])

    def test_project_profile_is_never_replaced_implicitly(self):
        self.install(profile="python")
        before = self.snapshot()
        with self.assertRaises(kit.KitError):
            self.install(profile="generic")
        self.assertEqual(before, self.snapshot())

    def test_tools_can_be_added_but_are_not_silently_deleted(self):
        self.install(tools=["codex"])
        self.install(tools=["codex", "claude"])
        self.assertTrue((self.target / ".claude/skills/implement-ticket/SKILL.md").exists())
        before = self.snapshot()
        with self.assertRaises(kit.KitError):
            self.install(tools=["codex"])
        self.assertEqual(before, self.snapshot())

    def test_missing_managed_file_is_detected_and_repaired(self):
        self.install()
        path = self.target / ".codex/agents/specdev-explorer.toml"
        path.unlink()
        self.assertFalse(kit.check(self.target, self.source)["ok"])
        self.install()
        self.assertTrue(kit.check(self.target, self.source)["ok"])

    def test_parent_file_collision_fails_before_writes(self):
        self.target.mkdir()
        (self.target / ".agents").write_text("This is a file.\n", encoding="utf-8")
        before = self.snapshot()
        with self.assertRaises(kit.KitError):
            self.install()
        self.assertEqual(before, self.snapshot())

    def test_local_context_can_be_selected_without_becoming_managed(self):
        self.install()
        path = self.target / "docs/LOCAL.md"
        path.parent.mkdir()
        path.write_text("Project context.\n", encoding="utf-8")
        config = self.config()
        config["context"] = ["docs/LOCAL.md"]
        self.write_config(config)
        self.install()
        manifest = kit.read_json(self.target / kit.MANIFEST)
        self.assertNotIn("docs/LOCAL.md", manifest["files"])
        self.assertTrue(kit.check(self.target, self.source)["ok"])

    def test_escape_paths_in_config_are_rejected(self):
        self.install()
        for invalid in ("../escape", "C:/outside", "/outside", "safe/../../escape", "safe\\escape"):
            with self.subTest(path=invalid):
                config = self.config()
                config["paths"]["plans"] = invalid
                self.write_config(config)
                with self.assertRaises(kit.KitError):
                    self.install()
                config["paths"]["plans"] = "Plans"
                self.write_config(config)

    def test_symlink_cannot_redirect_installation(self):
        self.target.mkdir()
        outside = self.base / "outside"
        outside.mkdir()
        try:
            (self.target / ".agents").symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"Symlink unavailable in this session: {exc}")
        with self.assertRaises(kit.KitError):
            self.install()
        self.assertEqual(list(outside.iterdir()), [])

    def test_commands_are_declarative_and_never_executed(self):
        self.install()
        marker = self.base / "should-not-exist.txt"
        config = self.config()
        config["validation"] = [{
            "id": "do-not-run", "cwd": ".", "argv": [sys.executable, "-c", f"open({str(marker)!r}, 'w').write('executed')"],
            "surfaces": ["tooling"], "requires": [], "required": True
        }]
        self.write_config(config)
        self.install()
        self.assertFalse(marker.exists())

    def test_install_lock_blocks_without_touching_project_files(self):
        self.install()
        path = self.target / ".codex/agents/specdev-explorer.toml"
        path.unlink()
        lock = self.target / ".specdev/install.lock"
        lock.write_text("Busy.\n", encoding="utf-8")
        before = self.snapshot()
        with self.assertRaises(kit.KitError):
            self.install()
        self.assertEqual(before, self.snapshot())

    def test_bad_profile_and_manifest_have_clear_errors(self):
        with self.assertRaises(kit.KitError):
            self.install(profile="../escape")
        self.install()
        manifest = self.target / kit.MANIFEST
        manifest.write_text('{"schema_version":1,"files":{},"tools":[55]}', encoding="utf-8")
        with self.assertRaises(kit.KitError):
            self.install()

    def test_profiles_work_on_distinct_consumers(self):
        for name in ("generic", "python", "dotnet-angular", "node", "react", "node-react"):
            with self.subTest(profile=name):
                target = self.base / name
                kit.install(target, profile=name, kit_root=self.source)
                self.assertTrue(kit.check(target, self.source)["ok"])

    def test_invalid_command_schema_is_rejected(self):
        config = kit.read_json(self.source / "profiles/python.json")
        config["validation"][0]["argv"] = "python -m unittest"
        with self.assertRaises(kit.KitError):
            kit.validate_config(config)

    def test_cli_invalid_profile_returns_controlled_error(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/specdev.py"), "install", "--target", str(self.target), "--profile", "missing"],
            capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse(self.target.exists())


class ReviewContractTests(unittest.TestCase):
    def test_valid_review_and_low_priority_observation(self):
        result = {"summary": "Checked.", "verdict": "approve", "findings": []}
        self.assertEqual(review.validate(result), result)
        result["findings"] = [{"severity": "P3", "file": "file.py", "line": 3, "title": "Observation", "body": "Details."}]
        review.validate(result)

    def test_approve_cannot_hide_relevant_findings(self):
        result = {"summary": "Checked.", "verdict": "approve", "findings": [
            {"severity": "P2", "file": "file.py", "line": 1, "title": "Regression", "body": "Condition and effect."}]}
        with self.assertRaises(ValueError):
            review.validate(result)
        result["verdict"] = "request_changes"
        review.validate(result)

    def test_invalid_location_or_missing_evidence_is_rejected(self):
        template = {"summary": "Checked.", "verdict": "request_changes", "findings": [
            {"severity": "P1", "file": "file.py", "line": 1, "title": "Failure", "body": "Evidence."}]}
        for field, value in (("line", True), ("line", 0), ("file", ""), ("body", " ")):
            result = copy.deepcopy(template)
            result["findings"][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                review.validate(result)


if __name__ == "__main__":
    unittest.main()
