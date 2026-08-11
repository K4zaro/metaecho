import io
import pathlib
import zipfile
from datetime import datetime

import piexif
from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.xmp import XmpInformation


def generate_gps_jpeg() -> None:
    o = io.BytesIO()
    example = pathlib.Path(__file__).parent / "example.jpg"
    thumb_im = Image.open(example)
    thumb_im.thumbnail((50, 50), Image.Resampling.LANCZOS)
    thumb_im.save(o, "jpeg")
    thumbnail = o.getvalue()
    img = Image.new("RGB", (10, 10), color="red")

    zeroth_ifd = {
        piexif.ImageIFD.Make: "Canon",
        piexif.ImageIFD.XResolution: (96, 1),
        piexif.ImageIFD.YResolution: (96, 1),
        piexif.ImageIFD.Software: "piexif",
    }
    exif_ifd = {
        piexif.ExifIFD.DateTimeOriginal: "2099:09:29 10:10:10",
        piexif.ExifIFD.LensMake: "LensMake",
        piexif.ExifIFD.Sharpness: 65535,
        piexif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),
    }
    gps_ifd = {
        piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
        piexif.GPSIFD.GPSDateStamp: "2001:09:11 08:46:21",
        piexif.GPSIFD.GPSLatitudeRef: "S",
        piexif.GPSIFD.GPSLatitude: ((58, 1), (36, 1), (15, 1)),
        piexif.GPSIFD.GPSLongitudeRef: "W",
        piexif.GPSIFD.GPSLongitude: ((34, 1), (22, 1), (48, 1)),
        piexif.GPSIFD.GPSAltitudeRef: (0,),
        piexif.GPSIFD.GPSAltitude: (1700, 1),
    }
    first_ifd = {
        piexif.ImageIFD.Make: "Canon",
        piexif.ImageIFD.XResolution: (40, 1),
        piexif.ImageIFD.YResolution: (40, 1),
        piexif.ImageIFD.Software: "piexif",
    }
    exif_dict = {
        "0th": zeroth_ifd,
        "Exif": exif_ifd,
        "GPS": gps_ifd,
        "1st": first_ifd,
        "thumbnail": thumbnail,
    }
    exif_bytes = piexif.dump(exif_dict)
    path = pathlib.Path(__file__).parent / "generated_gps.jpeg"
    img.save(path, exif=exif_bytes)


def generate_pdf_with_metadata() -> None:

    writer = PdfWriter()
    writer.add_blank_page(width=8.27 * 72, height=11.7 * 72)
    path = pathlib.Path(__file__).parent / "example.pdf"
    with open(path, "wb") as f:
        writer.write(f)  # Save the PDF to a file

    reader = PdfReader(path)
    writer = PdfWriter()

    # Add all pages to the writer
    for page in reader.pages:
        writer.add_page(page)

    # If you want to add the old metadata, include these two lines
    if reader.metadata is not None:
        writer.add_metadata(reader.metadata)

    # Format the current date and time for the metadata
    utc_time = "-05'00'"  # UTC time optional
    time = datetime.now().strftime(f"D\072%Y%m%d%H%M%S{utc_time}")

    # Add the new metadata
    writer.add_metadata(
        {
            "/Author": "Martin",
            "/Producer": "Libre Writer",
            "/Title": "Title",
            "/Subject": "Subject",
            "/Keywords": "Keywords",
            "/CreationDate": time,
            "/ModDate": time,
            "/Creator": "Creator",
            "/CustomField": "CustomField",
        }
    )

    # Create a new XMP metadata object
    xmp = XmpInformation.create()

    # Set metadata fields
    xmp.dc_title = {"x-default": "Title", "en": "English Title", "pl": "Polski tytuł"}
    xmp.dc_creator = ["Author One", "Author Two"]
    xmp.dc_description = {
        "x-default": "Document description",
        "en": "English description",
        "pl": "Polski opis",
    }
    xmp.dc_rights = {"x-default": "All rights reserved"}
    xmp.pdf_producer = "pypdf"
    xmp.pdf_keywords = "keyword1, keyword2, keyword3"
    xmp.pdf_pdfversion = "1.4"
    xmp.xmp_creator_tool = "pypdf"
    xmp.dc_date = [datetime.now()]

    # Date fields
    xmp.xmp_create_date = datetime.now()
    xmp.xmp_modify_date = datetime.fromisoformat("2023-12-25T10:30:45Z")
    xmp.xmp_metadata_date = datetime.now()

    # Single value fields
    xmp.dc_coverage = "Global coverage"
    xmp.dc_format = "application/pdf"
    xmp.dc_identifier = "unique-id-123"
    xmp.dc_source = "Original Source"

    # Array fields (bags - unordered)
    xmp.dc_contributor = ["Contributor One", "Contributor Two"]
    xmp.dc_language = ["en", "pl", "de"]
    xmp.dc_publisher = ["Publisher One"]
    xmp.dc_relation = ["Related Doc 1", "Related Doc 2"]
    xmp.dc_subject = ["keyword1", "keyword2"]
    xmp.dc_type = ["Document", "Text"]

    # Save the new PDF to a file
    path_meta = pathlib.Path(__file__).parent / "generated_pdf_with_meta.pdf"
    writer.xmp_metadata = xmp
    writer.write(path_meta)


def generate_ooxml_with_metadata() -> None:

    core_xml_content = """<cp:coreProperties 
        xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" 
        xmlns:dc="http://purl.org/dc/elements/1.1/" 
        xmlns:dcterms="http://purl.org/dc/terms/"
        xmlns:dcmitype="http://purl.org/dc/dcmitype/" 
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <dc:creator>Test Author</dc:creator>
            <dc:title>Sample Document</dc:title>
            <dc:subject>Testing</dc:subject>
            <cp:lastModifiedBy>Test Editor</cp:lastModifiedBy>
            <cp:revision>3</cp:revision>
            <dcterms:created xsi:type="dcterms:W3CDTF">2024-01-01T00:00:00Z</dcterms:created>
            <dcterms:modified xsi:type="dcterms:W3CDTF">2024-01-02T00:00:00Z</dcterms:modified>
        </cp:coreProperties>"""

    app_xml_content = """<Properties 
        xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" 
        xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
            <Template>Normal.dotm</Template>
            <TotalTime>69</TotalTime>
            <Company>THE COMPANY</Company>
            <Pages>2</Pages>
            <Application>Microsoft Office Word</Application>
            <DocSecurity>0</DocSecurity>
            <Lines>21</Lines>
            <Paragraphs>6</Paragraphs>
            <ScaleCrop>false</ScaleCrop>
            <LinksUpToDate>false</LinksUpToDate>
            <CharactersWithSpaces>3015</CharactersWithSpaces>
            <SharedDoc>false</SharedDoc>
            <HyperlinksChanged>false</HyperlinksChanged>
            <AppVersion>16.0000</AppVersion>    
        </Properties>"""

    path_meta = pathlib.Path(__file__).parent / "generated_docx.docx"
    path = pathlib.Path(__file__).parent / "example.docx"
    path_pptx = pathlib.Path(__file__).parent / "example.pptx"
    path_xlsx = pathlib.Path(__file__).parent / "example.xlsx"
    with zipfile.ZipFile(path_pptx, "w") as zip_file:
        zip_file.writestr("ppt/presentation.xml", "<document></document>")
    with zipfile.ZipFile(path_xlsx, "w") as zip_file:
        zip_file.writestr("xl/workbook.xml", "<document></document>")
    with zipfile.ZipFile(path, "w") as zip_file:
        zip_file.writestr("word/document.xml", "<document></document>")
    with zipfile.ZipFile(path_meta, "w") as zip_file:
        zip_file.writestr("word/document.xml", "<document></document>")
        zip_file.writestr("docProps/core.xml", core_xml_content)
        zip_file.writestr("docProps/app.xml", app_xml_content)


if __name__ == "__main__":
    generate_gps_jpeg()
    generate_pdf_with_metadata()
    generate_ooxml_with_metadata()
