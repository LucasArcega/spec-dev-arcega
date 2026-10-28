#!/usr/bin/env python3
"""Validate review JSON against the bundled contract, using only the stdlib.

The evaluator implements only the schema keywords used by this contract.
Unknown validation keywords fail closed instead of being ignored.
"""
import argparse
import json
import math
from pathlib import Path
import re
import sys


SCHEMA = Path(__file__).resolve().parents[1] / "references/review.schema.json"
KEYWORDS = {
    "$schema", "$defs", "$ref", "title", "description", "type", "const",
    "enum", "required", "properties", "additionalProperties", "items",
    "minLength", "minItems", "maxItems", "minimum", "pattern", "oneOf",
    "allOf", "if", "then", "not", "contains",
}


class SchemaError(ValueError):
    """A bundled schema rule cannot be interpreted safely."""


def _matches(value, rule, schema):
    try:
        _validate(value, rule, schema)
    except SchemaError:
        raise
    except ValueError:
        return False
    return True


def _validate(value, rule, schema, location="review"):
    unknown = set(rule) - KEYWORDS
    if unknown:
        raise SchemaError(f"Schema contém regra não suportada: {sorted(unknown)}")
    if "$ref" in rule:
        reference = rule["$ref"]
        if not reference.startswith("#/$defs/") or reference.count("/") != 2:
            raise SchemaError("Somente referências locais em $defs são suportadas.")
        _validate(value, schema["$defs"][reference.rsplit("/", 1)[1]], schema, location)
    kind = rule.get("type")
    valid_type = {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": (type(value) is int or
                    (type(value) is float and math.isfinite(value) and value.is_integer())),
    }
    if kind is not None and not valid_type.get(kind, False):
        raise ValueError(f"{location}: esperado {kind}.")
    if "const" in rule and value != rule["const"]:
        raise ValueError(f"{location}: valor deve ser {rule['const']!r}.")
    if "enum" in rule and value not in rule["enum"]:
        raise ValueError(f"{location}: valor fora das opções permitidas.")
    if isinstance(value, dict):
        missing = set(rule.get("required", [])) - set(value)
        if missing:
            raise ValueError(f"{location}: campos ausentes {sorted(missing)}.")
        properties = rule.get("properties", {})
        if rule.get("additionalProperties") is False and set(value) - set(properties):
            raise ValueError(f"{location}: campos extras {sorted(set(value) - set(properties))}.")
        for key, child in properties.items():
            if key in value:
                _validate(value[key], child, schema, f"{location}.{key}")
    if isinstance(value, str):
        if len(value) < rule.get("minLength", 0):
            raise ValueError(f"{location}: texto vazio.")
        if "pattern" in rule and re.search(rule["pattern"], value) is None:
            raise ValueError(f"{location}: texto deve conter conteúdo além de espaços.")
    if isinstance(value, list):
        if len(value) < rule.get("minItems", 0) or len(value) > rule.get("maxItems", math.inf):
            raise ValueError(f"{location}: quantidade de itens inválida.")
        if "items" in rule:
            for index, child in enumerate(value):
                _validate(child, rule["items"], schema, f"{location}[{index}]")
        if "contains" in rule and not any(_matches(child, rule["contains"], schema) for child in value):
            raise ValueError(f"{location}: falta um item obrigatório para este resultado.")
    if "minimum" in rule and type(value) in (int, float) and value < rule["minimum"]:
        raise ValueError(f"{location}: valor abaixo do mínimo.")
    for child in rule.get("allOf", []):
        _validate(value, child, schema, location)
    if "if" in rule and _matches(value, rule["if"], schema) and "then" in rule:
        _validate(value, rule["then"], schema, location)
    if "not" in rule and _matches(value, rule["not"], schema):
        raise ValueError(f"{location}: combinação incompatível com o resultado.")
    if "oneOf" in rule:
        matches, errors = 0, []
        for child in rule["oneOf"]:
            try:
                _validate(value, child, schema, location)
                matches += 1
            except SchemaError:
                raise
            except ValueError as exc:
                errors.append(str(exc))
        if matches != 1:
            raise ValueError(f"{location}: contrato inválido. " + " | ".join(errors))


def validate(review, require_evidence=False):
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    _validate(review, schema, schema)
    if require_evidence and review.get("schema_version") != 2:
        raise ValueError("Esta revisão exige schema_version=2 e evidência estruturada.")
    return review


def _reject_constant(value):
    raise ValueError(f"Constante JSON inválida: {value}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", type=Path, help="Caminho do review JSON.")
    parser.add_argument("--require-evidence", action="store_true", help="Exige o contrato v2.")
    args = parser.parse_args(argv)
    try:
        review = json.loads(args.review.read_text(encoding="utf-8-sig"), parse_constant=_reject_constant)
        validate(review, require_evidence=args.require_evidence)
    except (OSError, ValueError) as exc:
        print(f"Review inválido: {exc}", file=sys.stderr)
        return 1
    print("Review válido.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
