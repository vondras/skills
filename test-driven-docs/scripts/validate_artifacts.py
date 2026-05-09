#!/usr/bin/env python3
"""Validate test-driven-docs skill artifacts.

Checks:
- YAML syntax for schemas and examples
- JSON Schema validity for contract/questions/evaluation/frontmatter examples
- Evaluation summary counts match result statuses
- Document-set cross-document summary counts match cross_document_findings
- test-driven-docs frontmatter referenced files and optional document hashes remain valid

Usage:
  python scripts/validate_artifacts.py
  python scripts/validate_artifacts.py --root path/to/skill
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: PyYAML. Install with: pip install pyyaml jsonschema") from exc

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: jsonschema. Install with: pip install pyyaml jsonschema") from exc



class NoDatesSafeLoader(yaml.SafeLoader):
    pass


# Keep YAML dates as strings so common frontmatter like `last_reviewed: 2026-05-07`
# validates consistently across Markdown/frontmatter toolchains.
for first_char, resolvers in list(NoDatesSafeLoader.yaml_implicit_resolvers.items()):
    NoDatesSafeLoader.yaml_implicit_resolvers[first_char] = [
        (tag, regexp) for tag, regexp in resolvers if tag != "tag:yaml.org,2002:timestamp"
    ]

STATUS_TO_SUMMARY = {
    "PASS": "passed",
    "PARTIAL": "partial",
    "FAIL": "failed",
    "CONTRADICTORY": "contradictory",
    "NOT_APPLICABLE": "not_applicable",
}


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.load(handle, Loader=NoDatesSafeLoader)

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_markdown_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    frontmatter = yaml.load(match.group(1), Loader=NoDatesSafeLoader) or {}
    body = text[match.end():]
    return frontmatter, body


def validate_frontmatter(path: Path, schema_path: Path) -> list[str]:
    frontmatter, body = parse_markdown_frontmatter(path)
    if frontmatter is None or "tddoc" not in frontmatter:
        return []

    schema = load_yaml(schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(frontmatter), key=lambda e: list(e.absolute_path))
    output = [f"{path}: {'.'.join(map(str, err.absolute_path)) or '<root>'}: {err.message}" for err in errors]

    tddoc = frontmatter.get("tddoc", {})
    tests = tddoc.get("tests") or {}
    suite = tests.get("suite")
    if suite:
        suite_path = (path.parent / suite).resolve()
        if not suite_path.exists():
            output.append(f"{path}: tddoc.tests.suite points to missing file: {suite}")

    evaluation = tddoc.get("evaluation") or {}
    latest = evaluation.get("latest")
    if latest:
        latest_path = (path.parent / latest).resolve()
        if not latest_path.exists():
            output.append(f"{path}: tddoc.evaluation.latest points to missing file: {latest}")

    document_hash = evaluation.get("document_hash")
    if document_hash:
        actual_hash = "sha256:" + hashlib.sha256(body.encode("utf-8")).hexdigest()
        if document_hash != actual_hash:
            output.append(f"{path}: tddoc.evaluation.document_hash expected {actual_hash}, found {document_hash}")

    for idx, related in enumerate(tddoc.get("related_documents") or []):
        rel_path = related.get("path")
        if rel_path and not (path.parent / rel_path).resolve().exists():
            output.append(f"{path}: tddoc.related_documents[{idx}].path points to missing file: {rel_path}")

    return output


def validate_schema(schema_path: Path, data_path: Path) -> list[str]:
    schema = load_yaml(schema_path)
    data = load_yaml(data_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
    return [f"{data_path}: {'.'.join(map(str, err.absolute_path)) or '<root>'}: {err.message}" for err in errors]


def count_results(results: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(result.get("status") for result in results)
    return {
        "total": len(results),
        "passed": counts["PASS"],
        "partial": counts["PARTIAL"],
        "failed": counts["FAIL"],
        "contradictory": counts["CONTRADICTORY"],
        "not_applicable": counts["NOT_APPLICABLE"],
    }


def compare_summary(path: Path, label: str, actual_summary: dict[str, Any], expected: dict[str, int]) -> list[str]:
    errors: list[str] = []
    for key, expected_value in expected.items():
        actual_value = actual_summary.get(key)
        if actual_value != expected_value:
            errors.append(f"{path}: {label}.summary.{key} expected {expected_value}, found {actual_value}")
    return errors


def validate_evaluation_counts(path: Path) -> list[str]:
    data = load_yaml(path)
    evaluation = data.get("evaluation", {})
    artifact_type = evaluation.get("artifact_type")
    errors: list[str] = []

    if artifact_type == "single_document":
        errors.extend(compare_summary(path, "evaluation", evaluation.get("summary", {}), count_results(evaluation.get("results", []))))
        return errors

    if artifact_type != "document_set":
        return [f"{path}: evaluation.artifact_type must be single_document or document_set"]

    all_results: list[dict[str, Any]] = []
    for idx, item in enumerate(evaluation.get("per_document_evaluations", [])):
        results = item.get("results", [])
        all_results.extend(results)
        errors.extend(compare_summary(path, f"per_document_evaluations[{idx}]", item.get("summary", {}), count_results(results)))

    set_eval = evaluation.get("set_level_evaluation", {})
    set_results = set_eval.get("results", [])
    all_results.extend(set_results)
    set_expected = count_results(set_results)

    cross_findings = set_eval.get("cross_document_findings", [])
    cross_contradictions = [f for f in cross_findings if f.get("kind") == "CONTRADICTION"]
    blocking_cross = [f for f in cross_findings if f.get("blocking")]
    set_expected["cross_document_findings"] = len(cross_findings)
    set_expected["cross_document_contradictions"] = len(cross_contradictions)
    set_expected["blocking_findings"] = len([r for r in set_results if r.get("blocking") and r.get("status") != "PASS"]) + len(blocking_cross)
    errors.extend(compare_summary(path, "set_level_evaluation", set_eval.get("summary", {}), set_expected))

    top_expected = count_results(all_results)
    top_expected["cross_document_findings"] = len(cross_findings)
    top_expected["cross_document_contradictions"] = len(cross_contradictions)
    top_expected["blocking_findings"] = len([r for r in all_results if r.get("blocking") and r.get("status") != "PASS"]) + len(blocking_cross)
    errors.extend(compare_summary(path, "evaluation", evaluation.get("summary", {}), top_expected))

    blocking_list = evaluation.get("blocking_findings")
    if blocking_list is not None and len(blocking_list) != top_expected["blocking_findings"]:
        errors.append(
            f"{path}: evaluation.blocking_findings length expected {top_expected['blocking_findings']}, found {len(blocking_list)}"
        )

    return errors


def check_duplicate_roles_in_set(root: Path) -> tuple[list[str], list[str]]:
    """Error on duplicate entry_point/index roles; warn on other duplicate roles within a set."""
    # role_in_set values that must be unique within a document set
    unique_roles = {"entry_point", "index"}

    from collections import defaultdict
    set_roles: dict[str, dict[str, list[Path]]] = defaultdict(lambda: defaultdict(list))

    for path in sorted(root.rglob("*.md")):
        if path.name == "authoring-template.md":
            continue
        frontmatter, _ = parse_markdown_frontmatter(path)
        if not frontmatter or "tddoc" not in frontmatter:
            continue
        tddoc = frontmatter.get("tddoc") or {}
        doc_set = tddoc.get("document_set")
        role = tddoc.get("role_in_set")
        if doc_set and role:
            set_roles[doc_set][role].append(path.resolve())

    errors: list[str] = []
    warnings: list[str] = []
    for doc_set, roles in sorted(set_roles.items()):
        for role, paths in sorted(roles.items()):
            if len(paths) > 1:
                names = ", ".join(str(p.relative_to(root)) for p in paths)
                if role in unique_roles:
                    errors.append(f"document_set '{doc_set}': role_in_set '{role}' claimed by {len(paths)} documents: {names}")
                else:
                    warnings.append(f"WARN: document_set '{doc_set}': role_in_set '{role}' claimed by {len(paths)} documents: {names}")
    return errors, warnings


def check_bidirectional_related_documents(root: Path) -> list[str]:
    """Warn when document A lists document B but B has no link back to A."""
    # Build a map: absolute_path -> list of absolute paths it links to
    links: dict[Path, list[Path]] = {}
    for path in sorted(root.rglob("*.md")):
        if path.name == "authoring-template.md":
            continue
        frontmatter, _ = parse_markdown_frontmatter(path)
        if not frontmatter or "tddoc" not in frontmatter:
            continue
        tddoc = frontmatter.get("tddoc") or {}
        targets = []
        for related in tddoc.get("related_documents") or []:
            rel_path = related.get("path")
            if rel_path:
                target = (path.parent / rel_path).resolve()
                if target.exists():
                    targets.append(target)
        links[path.resolve()] = targets

    warnings = []
    for src, targets in links.items():
        for tgt in targets:
            if tgt not in links:
                continue  # target has no tddoc frontmatter, skip
            if src not in links[tgt]:
                warnings.append(
                    f"WARN: {src.relative_to(root)}: lists {tgt.relative_to(root)} in related_documents but no reciprocal link found"
                )
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()

    errors: list[str] = []
    examples = root / "resources" / "examples"
    schemas = root / "resources"

    for path in sorted(root.rglob("*.yaml")):
        try:
            load_yaml(path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path}: YAML parse failed: {exc}")

    referenced_suites: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        if path.name == "authoring-template.md":
            continue
        errors.extend(validate_frontmatter(path, schemas / "tddoc.frontmatter.schema.yaml"))
        frontmatter, _ = parse_markdown_frontmatter(path)
        if frontmatter and "tddoc" in frontmatter:
            suite = (frontmatter.get("tddoc") or {}).get("tests", {}) or {}
            suite_path_str = suite.get("suite") if isinstance(suite, dict) else None
            if suite_path_str:
                suite_path = (path.parent / suite_path_str).resolve()
                if suite_path.exists():
                    referenced_suites.append(suite_path)

    schema_pairs = [
        (schemas / "contract.schema.yaml", examples / "example.contract.yaml"),
        (schemas / "questions.schema.yaml", examples / "example.questions.yaml"),
        (schemas / "questions.schema.yaml", examples / "example.docset.questions.yaml"),
        (schemas / "evaluation.schema.yaml", examples / "example.evaluation.yaml"),
        (schemas / "evaluation.schema.yaml", examples / "example.docset.evaluation.yaml"),
    ]
    for suite_path in referenced_suites:
        if suite_path not in {p for _, p in schema_pairs}:
            schema_pairs.append((schemas / "questions.schema.yaml", suite_path))

    for schema_path, data_path in schema_pairs:
        if not data_path.exists():
            errors.append(f"Missing expected example: {data_path}")
            continue
        errors.extend(validate_schema(schema_path, data_path))

    for path in [examples / "example.evaluation.yaml", examples / "example.docset.evaluation.yaml"]:
        if path.exists():
            errors.extend(validate_evaluation_counts(path))

    role_errors, role_warnings = check_duplicate_roles_in_set(root)
    errors.extend(role_errors)
    for warning in role_warnings:
        print(warning, file=sys.stderr)

    for warning in check_bidirectional_related_documents(root):
        print(warning, file=sys.stderr)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("All test-driven-docs skill artifacts validated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
