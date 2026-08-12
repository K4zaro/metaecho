import pathlib

from metaecho.extractors.image import ImageExtractor
from metaecho.extractors.ooxml import OoxmlExtractor
from metaecho.rules.engine import key_presence_matcher, non_default_matcher, value_pattern_matcher
from metaecho.rules.loader import load_rules


def test_key_presence() -> None:
    path = (
        pathlib.Path(__file__).parents[1] / "src" / "metaecho" / "rules" / "catalog" / "rules.json"
    )
    image_path = pathlib.Path(__file__).parent / "fixtures" / "generated_gps.jpeg"
    extractor = ImageExtractor()
    metadata = extractor.extract(image_path)
    rules = load_rules(path)
    path_rule = next(r for r in rules if r.id == "GPS-001")
    occurrences = key_presence_matcher(path_rule, metadata)
    assert isinstance(occurrences, list)
    assert len(occurrences) > 0


def test_non_default() -> None:
    path = (
        pathlib.Path(__file__).parents[1] / "src" / "metaecho" / "rules" / "catalog" / "rules.json"
    )
    file_path = pathlib.Path(__file__).parent / "fixtures" / "generated_docx.docx"
    extractor = OoxmlExtractor()
    metadata = extractor.extract(file_path)
    rules = load_rules(path)
    path_rule = next(r for r in rules if r.id == "PII-001")
    occurrences = non_default_matcher(path_rule, metadata)
    assert isinstance(occurrences, list)
    assert len(occurrences) > 0


def test_value_pattern() -> None:
    path = (
        pathlib.Path(__file__).parents[1] / "src" / "metaecho" / "rules" / "catalog" / "rules.json"
    )
    file_path = pathlib.Path(__file__).parent / "fixtures" / "generated_docx.docx"
    extractor = OoxmlExtractor()
    metadata = extractor.extract(file_path)
    rules = load_rules(path)
    path_rule = next(r for r in rules if r.id == "PATH-001")
    occurrences = value_pattern_matcher(path_rule, metadata)
    assert isinstance(occurrences, list)
    assert len(occurrences) > 0


def test_cross_file() -> None:
    pass
