import pathlib
import zipfile

import defusedxml.ElementTree as ET

from metaecho.extractors.base import MetadataExtractor
from metaecho.extractors.utils import truncate

CORE_NAMESPACES = {
    "dc": "http://purl.org/dc/elements/1.1/",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dcterms": "http://purl.org/dc/terms/",
}

APP_NAMESPACES = {
    "ep": "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties",
}

CORE_FIELDS = [
    "dc:creator",
    "dc:title",
    "dc:subject",
    "dc:description",
    "cp:lastModifiedBy",
    "cp:revision",
    "cp:keywords",
    "cp:category",
    "dcterms:created",
    "dcterms:modified",
]

APP_FIELDS = [
    "ep:Application",
    "ep:AppVersion",
    "ep:Company",
    "ep:Manager",
    "ep:Template",
    "ep:TotalTime",
    "ep:Pages",
    "ep:DocSecurity",
]

MAX_XML_SIZE = 10 * 1024 * 1024  # 10 MB


class OoxmlExtractor(MetadataExtractor):
    def supports(self, file_type: str) -> bool:
        return file_type in [
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ]

    def extract(self, path: pathlib.Path) -> dict[str, str]:
        with zipfile.ZipFile(path, "r") as zip_file:
            if "docProps/core.xml" in zip_file.namelist():
                info = zip_file.getinfo("docProps/core.xml")
                if info.file_size > MAX_XML_SIZE:
                    raise ValueError(
                        f"docProps/core.xml exceeds maximum allowed size ({info.file_size} bytes)"
                    )
                root = ET.fromstring(zip_file.read("docProps/core.xml"))
                ooxml_meta_core = {}
                for field in CORE_FIELDS:
                    data = root.find(field, CORE_NAMESPACES)
                    if data is not None and data.text is not None:
                        ooxml_meta_core.update({f"OOXML.Core.{field}": truncate(data.text)})
            else:
                ooxml_meta_core = {}
            if "docProps/app.xml" in zip_file.namelist():
                info = zip_file.getinfo("docProps/app.xml")
                if info.file_size > MAX_XML_SIZE:
                    raise ValueError(
                        f"docProps/app.xml exceeds maximum allowed size ({info.file_size} bytes)"
                    )
                root = ET.fromstring(zip_file.read("docProps/app.xml"))
                ooxml_meta_app = {}
                for field in APP_FIELDS:
                    data = root.find(field, APP_NAMESPACES)
                    if data is not None and data.text is not None:
                        ooxml_meta_app.update({f"OOXML.App.{field}": truncate(data.text)})
            else:
                ooxml_meta_app = {}
        return ooxml_meta_core | ooxml_meta_app
