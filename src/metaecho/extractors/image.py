import pathlib
from typing import Literal

from PIL import ExifTags, Image

from metaecho.extractors.base import MetadataExtractor

# MAX_IMAGE_PIXELS = value  # change if you need more than 89,478,485 pixels (e.g. for high res img)

CAMERA_TAGS = {
    "Make",
    "Model",
    "LensMake",
    "LensModel",
    "BodySerialNumber",
    "LensSerialNumber",
    "InternalSerialNumber",
}

SOFTWARE_TAGS = {
    "Software",
    "ProcessingSoftware",
    "HostComputer",
}

PII_TAGS = {
    "Artist",
    "Copyright",
    "CameraOwnerName",
    "OwnerName",
}

TIMESTAMP_TAGS = {
    "DateTime",
    "DateTimeOriginal",
    "DateTimeDigitized",
    "OffsetTime",
    "OffsetTimeOriginal",
    "OffsetTimeDigitized",
    "SubsecTime",
    "SubsecTimeOriginal",
    "SubsecTimeDigitized",
}


def _dms_to_decimal(
    degrees: float, minutes: float, seconds: float, direction: Literal["N", "S", "E", "W"]
) -> float:
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if direction in ["S", "W"]:
        decimal = -decimal
    return decimal


def get_tag_prefix(tag_name: str) -> str:
    if tag_name in CAMERA_TAGS:
        return "EXIF.Camera."
    if tag_name in SOFTWARE_TAGS:
        return "EXIF.Software."
    if tag_name in PII_TAGS:
        return "EXIF.PII."
    if tag_name in TIMESTAMP_TAGS:
        return "EXIF.Timestamp."
    return "EXIF."


class ImageExtractor(MetadataExtractor):
    def supports(self, file_type: str) -> bool:
        return file_type in ["image/jpeg", "image/png"]

    def extract(self, path: pathlib.Path) -> dict[str, str]:
        img = Image.open(path)
        exif = {
            str(ExifTags.TAGS[k]): str(v) for k, v in img.getexif().items() if k in ExifTags.TAGS
        }
        exif = {f"{get_tag_prefix(name)}{name}": value for name, value in exif.items()}

        exifGPS = {
            str(ExifTags.GPSTAGS[k]): v
            for k, v in img.getexif().get_ifd(ExifTags.IFD.GPSInfo).items()
            if k in ExifTags.GPSTAGS
        }
        ifd1 = {
            str(ExifTags.TAGS[k]): v
            for k, v in img.getexif().get_ifd(ExifTags.IFD.IFD1).items()
            if k in ExifTags.TAGS
        }
        if ifd1.get("JpegIFByteCount", 0) > 0:
            exif["EXIF.Thumbnail.Present"] = "true"

        if "GPSLatitude" in exifGPS and "GPSLatitudeRef" in exifGPS:
            exifGPS.update(
                {
                    "GPSLatitude": _dms_to_decimal(
                        exifGPS["GPSLatitude"][0],
                        exifGPS["GPSLatitude"][1],
                        exifGPS["GPSLatitude"][2],
                        exifGPS["GPSLatitudeRef"],
                    )
                }
            )
        if "GPSLongitude" in exifGPS and "GPSLongitudeRef" in exifGPS:
            exifGPS.update(
                {
                    "GPSLongitude": _dms_to_decimal(
                        exifGPS["GPSLongitude"][0],
                        exifGPS["GPSLongitude"][1],
                        exifGPS["GPSLongitude"][2],
                        exifGPS["GPSLongitudeRef"],
                    )
                }
            )

        exifGPS = {"EXIF.GPSInfo." + name: str(value) for name, value in exifGPS.items()}

        return exif | exifGPS
