import pathlib

from metaecho.detect import detect


def test_detect_jpg() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "example.jpg"
    detected_type = detect(path)
    assert detected_type == "image/jpeg"


def test_detect_docx() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "example.docx"
    detected_type = detect(path)
    assert (
        detected_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


def test_detect_xlsx() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "example.xlsx"
    detected_type = detect(path)
    assert detected_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def test_detect_pdf() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "example.pdf"
    detected_type = detect(path)
    assert detected_type == "application/pdf"


def test_detect_pptx() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "example.pptx"
    detected_type = detect(path)
    assert (
        detected_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )


def test_detect_png() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "example.png"
    detected_type = detect(path)
    assert detected_type == "image/png"


def test_detect_unknown() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "example.txt"
    detected_type = detect(path)
    assert detected_type is None


def test_detect_edge_case_empty_file() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "empty_file"
    detected_type = detect(path)
    assert detected_type is None
