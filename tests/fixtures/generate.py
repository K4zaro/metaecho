import io
import pathlib

import piexif
from PIL import Image


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


if __name__ == "__main__":
    generate_gps_jpeg()
