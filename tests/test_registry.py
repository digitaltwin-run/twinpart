from pathlib import Path
from twinpart.registry import list_parts, get_part


def test_list_parts_finds_all_migrated_parts() -> None:
    parts = list_parts()
    ids = {p.component_id for p in parts}
    assert "rj45-molex-85513-5013" in ids
    assert "rp2040-zero" in ids
    assert "sw-tact-5.2x5.2" in ids
    assert "c-0603" in ids


def test_get_part_returns_correct_details() -> None:
    part = get_part("rj45-molex-85513-5013")
    assert part is not None
    assert part.manufacturer == "Molex"
    assert part.mpn == "85513-5013"
    assert part.footprint == "local:RJ45_Molex_85513-5013"
    assert (part.directory / "RJ45_Molex_85513-5013.kicad_mod").is_file()
