import pathlib

from metaecho.extractors.image import ImageExtractor, _dms_to_decimal


def test_dms_to_decimal_north() -> None:
    assert _dms_to_decimal(45, 30, 0, "N") == 45.5


def test_dms_to_decimal_east() -> None:
    assert _dms_to_decimal(45, 30, 0, "E") == 45.5


def test_dms_to_decimal_south() -> None:
    assert _dms_to_decimal(45, 30, 0, "S") == -45.5


def test_dms_to_decimal_west() -> None:
    assert _dms_to_decimal(45, 30, 0, "W") == -45.5


def test_dms_to_decimal_zero_north() -> None:
    assert _dms_to_decimal(0, 0, 0, "N") == 0.0


def test_dms_to_decimal_zero_south() -> None:
    assert _dms_to_decimal(0, 0, 0, "S") == 0.0


def test_extract_gps_coordinates() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "generated_gps.jpeg"
    extractor = ImageExtractor()
    metadata = extractor.extract(path)

    latitude = float(metadata["EXIF.GPSInfo.GPSLatitude"])
    longitude = float(metadata["EXIF.GPSInfo.GPSLongitude"])

    assert latitude < 0
    assert longitude < 0


def test_omit_nonexistent_gps_coordinates() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "example.jpg"
    extractor = ImageExtractor()
    metadata = extractor.extract(path)

    assert "EXIF.GPSInfo.GPSLatitude" not in metadata
    assert "EXIF.GPSInfo.GPSLongitude" not in metadata


def test_exif_thumbnail_not_present() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "example.jpg"
    extractor = ImageExtractor()
    metadata = extractor.extract(path)

    assert "EXIF.Thumbnail.Present" not in metadata


def test_exif_thumbnail_present() -> None:
    path = pathlib.Path(__file__).parent / "fixtures" / "generated_gps.jpeg"
    extractor = ImageExtractor()
    metadata = extractor.extract(path)

    assert "EXIF.Thumbnail.Present" in metadata
