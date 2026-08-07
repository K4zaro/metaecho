import pathlib

from metaecho.extractors.base import MetadataExtractor
from metaecho.models import FileError, FileRecord

MIME_TO_EXTENSIONS: dict[str, set[str]] = {
    "image/jpeg": {".jpg", ".jpeg"},
    "image/png": {".png"},
    "application/pdf": {".pdf"},
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {".docx"},
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {".xlsx"},
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": {".pptx"},
}


def get_extractor(file_type: str, extractors: list[MetadataExtractor]) -> MetadataExtractor | None:
    for extractor in extractors:
        if extractor.supports(file_type):
            return extractor
    return None


def build_file_record(
    path: pathlib.Path, file_type: str, extractors: list[MetadataExtractor]
) -> FileRecord:
    extractor = get_extractor(file_type, extractors)

    file_size = path.stat().st_size
    expected_extensions = MIME_TO_EXTENSIONS.get(file_type, set())
    if extractor is None:
        return FileRecord(
            path=str(path),
            size=file_size,
            file_type=file_type,
            extension_mismatch=path.suffix.lower() not in expected_extensions,
            metadata={},
            errors=[FileError(type="UnsupportedFileType", message=f"File type {file_type} is not supported.")],
        )
    errors: list[FileError] = []
    try:
        extracted_data = extractor.extract(path)
    except Exception as e:
        errors.append(FileError(type=type(e).__name__, message=str(e)))
        extracted_data = {}
    return FileRecord(
        path=str(path),
        size=file_size,
        file_type=file_type,
        extension_mismatch=path.suffix.lower() not in expected_extensions,
        metadata=extracted_data,
        errors=errors,
    )
