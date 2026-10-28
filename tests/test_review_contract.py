"""Behavioral coverage for the portable legacy and evidence-v2 review contracts."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/review-changes/scripts/validate_review.py"
spec = importlib.util.spec_from_file_location("evidence_review", SCRIPT)
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


def finding(severity="P2"):
    return {"severity": severity, "file": "src/file.py", "line": 1,
            "title": "Behavior risk", "body": "A verified condition causes the described effect."}


def evidence_review():
    return {
        "schema_version": 2,
        "summary": "Inspected the listed source snapshot.",
        "verdict": "approve",
        "scope": {"base": "unborn", "head": "working-tree:verified-snapshot", "files": ["src/file.py"]},
        "checks": [{"cwd": ".", "argv": ["python", "-m", "unittest"],
                    "status": "passed", "evidence": "Observed exit 0; suite output retained."}],
        "limitations": [], "blockers": [], "findings": [],
    }


class ReviewEvidenceTests(unittest.TestCase):
    def test_valid_contracts_and_numeric_integer_semantics(self):
        legacy = {"summary": "Historical review.", "verdict": "request_changes", "findings": []}
        approved = evidence_review()
        approved["findings"] = [finding("P3")]
        approved["findings"][0]["line"] = 1.0
        approved["schema_version"] = 2.0
        requested = evidence_review()
        requested.update(verdict="request_changes", findings=[finding()])
        blocked = evidence_review()
        blocked.update(verdict="blocked", blockers=["Required database unavailable."])
        blocked["checks"][0].update(status="not_run", evidence="Database prerequisite unavailable.")
        no_commands = evidence_review()
        no_commands.update(checks=[], limitations=["Read-only document review; no applicable executable checks."])
        for value in (legacy, evidence_review(), approved, requested, blocked, no_commands):
            with self.subTest(value=value):
                self.assertEqual(review.validate(value), value)

    def test_legacy_requires_explicit_opt_in_for_new_evidence_flow(self):
        legacy = {"summary": "Historical approval.", "verdict": "approve", "findings": []}
        review.validate(legacy)
        with self.assertRaisesRegex(ValueError, "schema_version=2"):
            review.validate(legacy, require_evidence=True)
        review.validate(evidence_review(), require_evidence=True)

    def test_invalid_documents_and_findings(self):
        cases = [None, [], {}, {"summary": " ", "verdict": "approve", "findings": []}]
        for field, value in (("summary", "\u0085\u00a0\u2003"), ("verdict", "unknown"),
                             ("schema_version", True), ("schema_version", 3),
                             ("findings", {}), ("extra", "unsupported")):
            document = evidence_review()
            document[field] = value
            cases.append(document)
        for field, value in (("line", True), ("line", 0), ("line", 1.5),
                             ("line", float("nan")), ("line", float("inf")),
                             ("file", " "), ("body", "\t\n"), ("severity", "P0"),
                             ("extra", "unsupported")):
            document = evidence_review()
            document["findings"] = [finding("P3")]
            document["findings"][0][field] = value
            cases.append(document)
        for value in cases:
            with self.subTest(value=value), self.assertRaises(ValueError):
                review.validate(value)

    def test_scope_and_check_evidence_are_required(self):
        cases = []
        for field in ("scope", "checks", "limitations", "blockers"):
            document = evidence_review()
            del document[field]
            cases.append(document)
        for field, value in (("base", ""), ("head", " "), ("files", []),
                             ("files", [" "]), ("extra", "unsupported")):
            document = evidence_review()
            document["scope"][field] = value
            cases.append(document)
        for field, value in (("cwd", ""), ("argv", []), ("argv", "python -m unittest"),
                             ("argv", ["python", " "]), ("status", "read"),
                             ("evidence", " "), ("extra", "unsupported")):
            document = evidence_review()
            document["checks"][0][field] = value
            cases.append(document)
        for value in cases:
            with self.subTest(value=value), self.assertRaises(ValueError):
                review.validate(value)

    def test_verdict_conditions_are_enforced_in_both_contracts(self):
        cases = []
        for severity in ("P1", "P2"):
            cases.append({"summary": "Cannot approve.", "verdict": "approve", "findings": [finding(severity)]})
            document = evidence_review()
            document["findings"] = [finding(severity)]
            cases.append(document)
        for status in ("failed", "not_run"):
            document = evidence_review()
            document["checks"][0]["status"] = status
            cases.append(document)
        for changes in ({"blockers": ["Unresolved prerequisite."]},
                        {"verdict": "blocked"},
                        {"verdict": "request_changes"},
                        {"verdict": "request_changes", "findings": [finding("P3")]},
                        {"limitations": [" "]}, {"blockers": [""]}):
            document = evidence_review()
            document.update(changes)
            cases.append(document)
        for value in cases:
            with self.subTest(value=value), self.assertRaises(ValueError):
                review.validate(value)

    def test_validator_reads_the_published_schema_instead_of_duplicating_rules(self):
        schema = json.loads(review.SCHEMA.read_text(encoding="utf-8"))
        schema["$defs"]["scope"]["properties"]["files"]["minItems"] = 2
        source = SimpleNamespace(read_text=lambda **kwargs: json.dumps(schema))
        with mock.patch.object(review, "SCHEMA", source):
            with self.assertRaises(ValueError):
                review.validate(evidence_review())
            document = evidence_review()
            document["scope"]["files"].append("src/second.py")
            review.validate(document)

    def test_unsupported_schema_rules_are_not_silently_accepted(self):
        with self.assertRaises(review.SchemaError):
            review._validate([], {"not": {"unsupportedValidation": True}}, {})

    def test_cli_validates_without_executing_or_resolving_evidence(self):
        with tempfile.TemporaryDirectory(prefix="review-contract-") as directory:
            path = Path(directory) / "review.json"
            marker = Path(directory) / "must-not-exist"
            document = evidence_review()
            document["scope"]["files"] = ["does-not-exist.py"]
            document["checks"][0]["argv"] = [sys.executable, "-c", f"open({str(marker)!r}, 'w').write('executed')"]
            path.write_text(json.dumps(document), encoding="utf-8-sig")
            result = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), str(path), "--require-evidence"],
                                    capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists())

    def test_cli_errors_are_controlled_and_legacy_flag_is_enforced(self):
        with tempfile.TemporaryDirectory(prefix="review-contract-") as directory:
            path = Path(directory) / "review.json"
            cases = [
                (json.dumps({"summary": "Legacy.", "verdict": "approve", "findings": []}), [], 0),
                (json.dumps({"summary": "Legacy.", "verdict": "approve", "findings": []}), ["--require-evidence"], 1),
                ("{", [], 1),
                ('{"summary": NaN, "verdict": "approve", "findings": []}', [], 1),
                (json.dumps(evidence_review()), ["--require-evidence"], 0),
            ]
            for content, flags, expected in cases:
                with self.subTest(content=content, flags=flags):
                    path.write_text(content, encoding="utf-8")
                    result = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), str(path), *flags],
                                            capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(result.returncode, expected, result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
            result = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), str(path.with_name("missing.json"))],
                                    capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 1)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
