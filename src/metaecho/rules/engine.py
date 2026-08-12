import re

from metaecho.models import Occurrence
from metaecho.rules.models import Rule


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
