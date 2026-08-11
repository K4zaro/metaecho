import pathlib
from datetime import datetime

from pypdf import PdfReader

from metaecho.extractors.base import MetadataExtractor
from metaecho.extractors.utils import truncate


def _join_list(values: list[str]) -> str:
    return ", ".join(values)


def _flatten_lang_dict(values: dict[str, str], field_name: str) -> dict[str, str]:
    return {f"PDF.XMP.{field_name}.{lang}": truncate(text) for lang, text in values.items()}


def _join_dates(values: list[datetime]) -> str:
    return ", ".join([v.isoformat() for v in values])


class PDFExtractor(MetadataExtractor):
    def supports(self, file_type: str) -> bool:
        return file_type in ["application/pdf"]

    def extract(self, path: pathlib.Path) -> dict[str, str]:
        pdf = PdfReader(path)

        # DocInfo
        doc_info = pdf.metadata
        if doc_info is not None:
            doc_meta = {
                str("PDF.DocInfo." + str(k).lstrip("/")): truncate(str(v))
                for k, v in doc_info.items()
                if v is not None
            }
        else:
            doc_meta = {}

        # XMP
        CAT_STR = [
            "dc_coverage",
            "dc_format",
            "dc_identifier",
            "dc_source",
            "pdf_keywords",
            "pdf_pdfversion",
            "pdf_producer",
            "xmp_creator_tool",
            "xmpmm_document_id",
            "xmpmm_instance_id",
            "pdfaid_part",
            "pdfaid_conformance",
        ]
        CAT_LIST = [
            "dc_contributor",
            "dc_creator",
            "dc_language",
            "dc_publisher",
            "dc_relation",
            "dc_subject",
            "dc_type",
        ]
        CAT_DICT = ["dc_description", "dc_rights", "dc_title"]
        CAT_DATE = ["xmp_create_date", "xmp_modify_date", "xmp_metadata_date"]
        xmp_info = pdf.xmp_metadata
        if xmp_info is not None:
            xmp_meta_str = {
                f"PDF.XMP.{name}": truncate(str(getattr(xmp_info, name)))
                for name in CAT_STR
                if getattr(xmp_info, name) is not None
            }
            xmp_meta_list = {
                f"PDF.XMP.{name}": truncate(_join_list(getattr(xmp_info, name)))
                for name in CAT_LIST
                if getattr(xmp_info, name) is not None
            }
            xmp_meta_dict = {}
            for name in CAT_DICT:
                field_value = getattr(xmp_info, name)
                if field_value is not None:
                    xmp_meta_dict.update(_flatten_lang_dict(field_value, name))
            dc_date_value = xmp_info.dc_date
            if dc_date_value is not None:
                xmp_meta_list_date = {"PDF.XMP.dc_date": _join_dates(dc_date_value)}
            else:
                xmp_meta_list_date = {}
            xmp_meta_date = {
                f"PDF.XMP.Date.{name}": truncate(getattr(xmp_info, name).isoformat())
                for name in CAT_DATE
                if getattr(xmp_info, name) is not None
            }
            dc_custom = xmp_info.custom_properties
            xmp_meta_custom = {
                str(f"PDF.XMP.Custom.{name}"): truncate(str(v)) for name, v in dc_custom.items()
            }

            xmp_meta = (
                xmp_meta_str
                | xmp_meta_list
                | xmp_meta_dict
                | xmp_meta_list_date
                | xmp_meta_date
                | xmp_meta_custom
            )
        else:
            xmp_meta = {}

        return doc_meta | xmp_meta
