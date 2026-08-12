from dataclasses import dataclass
from enum import StrEnum


class Severity(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class FileError:
    type: str
    message: str


@dataclass
class FileRecord:
    path: str
    size: int
    file_type: str
    extension_mismatch: bool
    metadata: dict[str, str]
    errors: list[FileError]


@dataclass
class Occurrence:
    key: str
    value: str


@dataclass
class Finding:
    id: str
    rule_id: str
    category: str
    severity: Severity
    file_path: str
    title: str
    description: str
    occurrences: list[Occurrence]


@dataclass
class Tool:
    name: str
    version: str
    python_version: str


@dataclass
class Scan:
    started_at: str
    finished_at: str
    duration_seconds: float
    root: str
    files_scanned: int
    files_skipped: int


@dataclass
class Summary:
    by_severity: dict[Severity, int]
    by_category: dict[str, int]


@dataclass
class ScanResult:
    schema_version: str
    tool: Tool
    ruleset_version: str
    flags: list[str]
    scan: Scan
    files: list[FileRecord]
    findings: list[Finding]
    correlations: list[dict[str, str]]
    summary: Summary
