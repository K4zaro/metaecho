import pathlib
from datetime import datetime

from metaecho.extractors.pdf import PDFExtractor


def test_pdf_doc_info_presence() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "generated_pdf_with_meta.pdf"
    extractor = PDFExtractor()
    metadata = extractor.extract(path)

    assert metadata["PDF.DocInfo.Author"] == "Martin"


def test_pdf_xmp_presence() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "generated_pdf_with_meta.pdf"
    extractor = PDFExtractor()
    metadata = extractor.extract(path)

    assert metadata["PDF.XMP.dc_coverage"] == "Global coverage"


def test_pdf_xmp_list_presence() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "generated_pdf_with_meta.pdf"
    extractor = PDFExtractor()
    metadata = extractor.extract(path)

    assert metadata["PDF.XMP.dc_creator"] == "Author One, Author Two"


def test_pdf_xmp_dict_presence() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "generated_pdf_with_meta.pdf"
    extractor = PDFExtractor()
    metadata = extractor.extract(path)

    assert metadata["PDF.XMP.dc_title.x-default"] == "Title"
    assert metadata["PDF.XMP.dc_title.en"] == "English Title"
    assert metadata["PDF.XMP.dc_title.pl"] == "Polski tytuł"


def test_pdf_xmp_date_presence() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "generated_pdf_with_meta.pdf"
    extractor = PDFExtractor()
    metadata = extractor.extract(path)

    assert "PDF.XMP.Date.xmp_modify_date" in metadata
    assert datetime.fromisoformat(metadata["PDF.XMP.Date.xmp_modify_date"])
    assert "PDF.XMP.Date.xmp_create_date" in metadata
    assert datetime.fromisoformat(metadata["PDF.XMP.Date.xmp_create_date"])


def test_pdf_xmp_dc_date_presence() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "generated_pdf_with_meta.pdf"
    extractor = PDFExtractor()
    metadata = extractor.extract(path)

    assert "PDF.XMP.dc_date" in metadata


def test_omit_empty_metadata_pdf() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "example.pdf"
    extractor = PDFExtractor()
    metadata = extractor.extract(path)

    assert "PDF.XMP.dc_title.x-default" not in metadata
    assert "PDF.XMP.dc_creator" not in metadata
    assert "PDF.XMP.dc_coverage" not in metadata
