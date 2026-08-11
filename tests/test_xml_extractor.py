import pathlib

from metaecho.extractors.ooxml import OoxmlExtractor


def test_ooxml_xml_content_presence() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "generated_docx.docx"
    extractor = OoxmlExtractor()
    metadata = extractor.extract(path)

    assert metadata["OOXML.Core.dc:creator"] == "Test Author"


def test_ooxml_app_content_presence() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "generated_docx.docx"
    extractor = OoxmlExtractor()
    metadata = extractor.extract(path)

    assert metadata["OOXML.App.ep:Application"] == "Microsoft Office Word"


def test_ooxml_xml_content_omit() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "example.docx"
    extractor = OoxmlExtractor()
    metadata = extractor.extract(path)

    assert "OOXML.Core.dc:creator" not in metadata


def test_ooxml_app_content_omit() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "example.docx"
    extractor = OoxmlExtractor()
    metadata = extractor.extract(path)

    assert "OOXML.App.ep:Application" not in metadata


def test_ooxml_pptx_xml_content_omit() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "example.pptx"
    extractor = OoxmlExtractor()
    metadata = extractor.extract(path)

    assert "OOXML.Core.dc:creator" not in metadata


def test_ooxml_pptx_app_content_omit() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "example.pptx"
    extractor = OoxmlExtractor()
    metadata = extractor.extract(path)

    assert "OOXML.App.ep:Application" not in metadata


def test_ooxml_xlsx_core_content_omit() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "example.xlsx"
    extractor = OoxmlExtractor()
    metadata = extractor.extract(path)

    assert "OOXML.Core.dc:creator" not in metadata


def test_ooxml_xlsx_app_content_omit() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "example.xlsx"
    extractor = OoxmlExtractor()
    metadata = extractor.extract(path)

    assert "OOXML.App.ep:Application" not in metadata
