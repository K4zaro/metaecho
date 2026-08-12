from dataclasses import dataclass
from enum import StrEnum

from metaecho.models import Severity


class MatchType(StrEnum):
    KEY_PRESENCE = "key-presence"
    NON_DEFAULT = "non-default"
    VALUE_PATTERN = "value-pattern"
    CROSS_FILE = "cross-file"


@dataclass
class Rule:
    id: str
    title: str
    description: str
    category: str
    severity: Severity
    match_type: MatchType
    keys: list[str]
    file_types: list[str]
    defaults: list[str] | None = None
    pattern: str | None = None
