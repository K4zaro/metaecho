import json
import pathlib
import re

from metaecho.models import Severity
from metaecho.rules.models import MatchType, Rule


def load_rules(path: pathlib.Path) -> list[Rule]:
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as e:
        raise RuleValidationError(f"File not found : {path}") from e
    except json.JSONDecodeError as e:
        raise RuleValidationError(f"rules.json is not valid JSON: {e}") from e
    rules: list[Rule] = []
    unique_ids: set[str] = set()
    for raw_rule in data["rules"]:
        rule = Rule(
            id=raw_rule["id"],
            title=raw_rule["title"],
            description=raw_rule["description"],
            category=raw_rule["category"],
            severity=Severity(raw_rule["severity"]),
            match_type=MatchType(raw_rule["matchType"]),
            keys=raw_rule["keys"],
            file_types=raw_rule["fileTypes"],
            defaults=raw_rule.get("defaults"),
            pattern=raw_rule.get("pattern"),
        )
        if rule.match_type == MatchType.NON_DEFAULT and rule.defaults is None:
            raise RuleValidationError(
                f"Rule {rule.id} has matchType 'non-default' but no 'defaults' field"
            )
        if rule.match_type == MatchType.VALUE_PATTERN and rule.pattern is None:
            raise RuleValidationError(
                f"Rule {rule.id} has matchType 'value-pattern' but no 'pattern' field"
            )
        if rule.match_type == MatchType.VALUE_PATTERN and rule.pattern is not None:
            try:
                re.compile(rule.pattern)
            except re.error as e:
                raise RuleValidationError(
                    f"Rule {rule.id} has broken regex in its pattern: {e}"
                ) from e
        if rule.id in unique_ids:
            raise RuleValidationError(f"Duplicate rule ID found: {rule.id}")

        unique_ids.add(rule.id)
        rules.append(rule)
    return rules


class RuleValidationError(Exception):
    pass
