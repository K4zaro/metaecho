import hashlib
import re
from collections import Counter
from collections.abc import Callable

from metaecho.models import Finding, Occurrence, Severity, Summary
from metaecho.rules.models import MatchType, Rule


def key_presence_matcher(rule: Rule, metadata: dict[str, str]) -> list[Occurrence]:
    matched = []
    for key in rule.keys:
        if key in metadata:
            matched.append(Occurrence(key=key, value=metadata[key]))
    return matched


def non_default_matcher(rule: Rule, metadata: dict[str, str]) -> list[Occurrence]:
    assert rule.defaults is not None
    matched = []
    for key in rule.keys:
        if key in metadata and metadata[key] not in rule.defaults:
            matched.append(Occurrence(key=key, value=metadata[key]))
    return matched


def value_pattern_matcher(rule: Rule, metadata: dict[str, str]) -> list[Occurrence]:
    assert rule.pattern is not None
    pattern = re.compile(rule.pattern)
    matched = []
    for key in rule.keys:
        if key in metadata and pattern.search(metadata[key]) is not None:
            matched.append(Occurrence(key=key, value=metadata[key]))
    return matched


def cross_file_matcher() -> None:
    pass


MATCHERS: dict[MatchType, Callable[[Rule, dict[str, str]], list[Occurrence]]] = {
    MatchType.KEY_PRESENCE: key_presence_matcher,
    MatchType.NON_DEFAULT: non_default_matcher,
    MatchType.VALUE_PATTERN: value_pattern_matcher,
    # MatchType.CROSS_FILE: cross_file_matcher,
}


def evaluate_rules(metadata: dict[str, str], file_path: str, rules: list[Rule]) -> list[Finding]:
    findings: list[Finding] = []
    for rule in rules:
        if rule.match_type == MatchType.CROSS_FILE:
            continue  # delete when implementing crossfile
        occurrences = MATCHERS[rule.match_type](rule, metadata)
        if occurrences:
            finding = Finding(
                id=_make_finding_id(rule.id, file_path),
                rule_id=rule.id,
                category=rule.category,
                severity=rule.severity,
                file_path=file_path,
                title=rule.title,
                description=rule.description,
                occurrences=occurrences,
            )
            findings.append(finding)
    return findings


def _make_finding_id(rule_id: str, file_path: str) -> str:
    return hashlib.sha256(f"{rule_id}:{file_path}".encode()).hexdigest()


def build_summary(findings: list[Finding]) -> Summary:
    by_severity: Counter[Severity] = Counter()
    by_category: Counter[str] = Counter()
    for finding in findings:
        by_severity[finding.severity] += 1
        by_category[finding.category] += 1
    return Summary(by_severity=dict(by_severity), by_category=dict(by_category))
