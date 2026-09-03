from pathlib import Path
from twinpart.swap import ripup_and_swap_component

def test_ripup_and_swap_component() -> None:
    pcb_path = Path("/home/tom/github/maskservice/viewer/artifacts/pcb/panel9.kicad_pcb")
    if not pcb_path.is_file():
        return
    board_text = pcb_path.read_text(encoding="utf-8")
    new_board, res = ripup_and_swap_component(board_text, "J1", "rj45-molex-85513-5013", margin_mm=5.0)

    assert res.reference == "J1"
    assert res.old_footprint == "local:RJ45_SMD"
    assert res.new_footprint == "local:RJ45_Molex_85513-5013"
    assert res.ripped_segments == 20
    assert "+5V" in res.unconnected_nets
    assert "GND" in res.unconnected_nets
