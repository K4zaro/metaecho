import pathlib
import zipfile


def detect(path: pathlib.Path) -> str | None:
    with open(path, "rb") as f:
        signature = f.read(8)
    if signature[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    elif signature[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    elif signature[:4] == b"%PDF":
        return "application/pdf"
    elif signature[:4] == b"PK\x03\x04":
        # Check for specific file types within the ZIP archive
        with zipfile.ZipFile(path, "r") as zip_file:
            if "word/document.xml" in zip_file.namelist():
                return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            elif "xl/workbook.xml" in zip_file.namelist():
                return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            elif "ppt/presentation.xml" in zip_file.namelist():
                return "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    return None
