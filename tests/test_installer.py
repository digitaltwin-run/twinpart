from pathlib import Path
from twinpart.installer import install_part


def test_install_part_places_files_correctly(tmp_path: Path) -> None:
    installed = install_part("rj45-molex-85513-5013", tmp_path)
    assert "manifest" in installed
    assert (tmp_path / "components" / "manifests" / "rj45-molex-85513-5013.json").is_file()
    assert (tmp_path / "local.pretty" / "RJ45_Molex_85513-5013.kicad_mod").is_file()
    assert (tmp_path / "local.symbols" / "RJ45_Molex_85513-5013.kicad_sym").is_file()
    assert (tmp_path / "local.3dshapes" / "RJ45_Molex_85513-5013.step").is_file()
