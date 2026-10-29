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
        raise SchemaError(f"Schema contains unsupported rule: {sorted(unknown)}")
    if "$ref" in rule:
        reference = rule["$ref"]
        if not reference.startswith("#/$defs/") or reference.count("/") != 2:
            raise SchemaError("Only local references in $defs are supported.")
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
        raise ValueError(f"{location}: expected {kind}.")
    if "const" in rule and value != rule["const"]:
        raise ValueError(f"{location}: value must be {rule['const']!r}.")
    if "enum" in rule and value not in rule["enum"]:
        raise ValueError(f"{location}: value is not an allowed option.")
    if isinstance(value, dict):
        missing = set(rule.get("required", [])) - set(value)
        if missing:
            raise ValueError(f"{location}: missing fields {sorted(missing)}.")
        properties = rule.get("properties", {})
        if rule.get("additionalProperties") is False and set(value) - set(properties):
            raise ValueError(f"{location}: additional fields {sorted(set(value) - set(properties))}.")
        for key, child in properties.items():
            if key in value:
                _validate(value[key], child, schema, f"{location}.{key}")
    if isinstance(value, str):
        if len(value) < rule.get("minLength", 0):
            raise ValueError(f"{location}: empty text.")
        if "pattern" in rule and re.search(rule["pattern"], value) is None:
            raise ValueError(f"{location}: text must contain non-whitespace content.")
    if isinstance(value, list):
        if len(value) < rule.get("minItems", 0) or len(value) > rule.get("maxItems", math.inf):
            raise ValueError(f"{location}: invalid number of items.")
        if "items" in rule:
            for index, child in enumerate(value):
                _validate(child, rule["items"], schema, f"{location}[{index}]")
        if "contains" in rule and not any(_matches(child, rule["contains"], schema) for child in value):
            raise ValueError(f"{location}: missing an item required for this result.")
    if "minimum" in rule and type(value) in (int, float) and value < rule["minimum"]:
        raise ValueError(f"{location}: value is below the minimum.")
    for child in rule.get("allOf", []):
        _validate(value, child, schema, location)
    if "if" in rule and _matches(value, rule["if"], schema) and "then" in rule:
        _validate(value, rule["then"], schema, location)
    if "not" in rule and _matches(value, rule["not"], schema):
        raise ValueError(f"{location}: combination is incompatible with the result.")
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
            raise ValueError(f"{location}: invalid contract. " + " | ".join(errors))


def validate(review, require_evidence=False):
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    _validate(review, schema, schema)
    if require_evidence and review.get("schema_version") != 2:
        raise ValueError("This review requires schema_version=2 and structured evidence.")
    return review


def _reject_constant(value):
    raise ValueError(f"Invalid JSON constant: {value}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", type=Path, help="Path to the JSON review.")
    parser.add_argument("--require-evidence", action="store_true", help="Require the v2 contract.")
    args = parser.parse_args(argv)
    try:
        review = json.loads(args.review.read_text(encoding="utf-8-sig"), parse_constant=_reject_constant)
        validate(review, require_evidence=args.require_evidence)
    except (OSError, ValueError) as exc:
        print(f"Invalid review: {exc}", file=sys.stderr)
        return 1
    print("Review valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
