import pathlib
import re

from metaecho.rules.loader import load_rules
from metaecho.rules.models import Rule


def test_json_load() -> None:
    path = (
        pathlib.Path(__file__).parents[1] / "src" / "metaecho" / "rules" / "catalog" / "rules.json"
    )
    # print(f"\nTesting path: {path}")
    rules = load_rules(path)
    assert isinstance(rules, list)
    assert len(rules) > 0
    assert all(isinstance(r, Rule) for r in rules)


def test_path_patterns_match_examples() -> None:
    path = (
        pathlib.Path(__file__).parents[1] / "src" / "metaecho" / "rules" / "catalog" / "rules.json"
    )
    rules = load_rules(path)
    for rule in rules:
        if rule.id == "PATH-001":
            assert rule.pattern is not None
            pattern = re.compile(rule.pattern)
            assert pattern.search(r"C:\Users\jan_kowalski\Documents\flag.txt") is not None
            assert pattern.search(r"C:\opt\temp\honeypot.txt") is None
        if rule.id == "PATH-002":
            assert rule.pattern is not None
            pattern = re.compile(rule.pattern)
            assert pattern.search(r"\\serwer\dzial\pracownicy.xlsx") is not None
