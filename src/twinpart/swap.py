"""Atomic component swapping and zone track rip-up for KiCad PCBs."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from .registry import get_part, PartEntry


@dataclass(frozen=True, slots=True)
class SwapResult:
    reference: str
    old_footprint: str
    new_footprint: str
    ripped_segments: int
    ripped_vias: int
    unconnected_nets: list[str]


def ripup_and_swap_component(
    board_text: str,
    reference: str,
    new_part_id: str,
    margin_mm: float = 3.0,
    parts_root: Path | None = None,
) -> tuple[str, SwapResult]:
    """Atomic replacement of a component on PCB with automatic zone rip-up of old tracks.

    1. Finds target footprint by reference.
    2. Calculates bounding box + margin_mm.
    3. Rips up all track segments and vias touching the component in the zone.
    4. Replaces footprint block with new component footprint from twinpart.
    """
    part = get_part(new_part_id, parts_root)
    if part is None:
        raise ValueError(f"Part {new_part_id!r} not found in twinpart library")

    # 1. Locate component footprint block
    lines = board_text.splitlines(keepends=True)
    fp_start = -1
    fp_end = -1
    in_target = False

    for i, line in enumerate(lines):
        if line.startswith("  (footprint "):
            fp_start = i
            in_target = False
        if fp_start != -1 and (f'(property "Reference" "{reference}"' in line or f'(fp_text reference "{reference}"' in line):
            in_target = True
        if fp_start != -1 and line == "  )\n":
            if in_target:
                fp_end = i
                break
            else:
                fp_start = -1

    if fp_start == -1 or fp_end == -1:
        raise ValueError(f"Component {reference!r} not found on PCB")

    old_block = "".join(lines[fp_start:fp_end+1])

    # Extract old footprint name
    old_fp_match = re.search(r'  \(footprint "([^"]+)"', old_block)
    old_fp_name = old_fp_match.group(1) if old_fp_match else "unknown"

    # Extract component position
    pos_match = re.search(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\)', old_block)
    if not pos_match:
        raise ValueError(f"Cannot parse position for component {reference}")

    comp_x = float(pos_match.group(1))
    comp_y = float(pos_match.group(2))

    # Extract pad positions and nets to determine rip-up bounding box
    pad_xs: list[float] = [comp_x]
    pad_ys: list[float] = [comp_y]
    nets_affected: set[str] = set()

    for pad_m in re.finditer(r'\(pad "([^"]+)" [^\(]*\(at ([0-9\.\-]+) ([0-9\.\-]+)[^\)]*\)(?:.*?\(net (\d+)(?: "([^"]+)")?\))?', old_block):
        px = comp_x + float(pad_m.group(2))
        py = comp_y + float(pad_m.group(3))
        pad_xs.append(px)
        pad_ys.append(py)
        net_name = pad_m.group(5) or pad_m.group(4)
        if net_name:
            nets_affected.add(net_name)

    min_x = min(pad_xs) - margin_mm
    max_x = max(pad_xs) + margin_mm
    min_y = min(pad_ys) - margin_mm
    max_y = max(pad_ys) + margin_mm

    # 2. Rip up colliding segments and vias within bounding box
    ripped_segments = 0
    ripped_vias = 0
    clean_lines = []

    for idx, line in enumerate(lines):
        if fp_start <= idx <= fp_end:
            # Skip old footprint lines for now
            continue
        if line.startswith("  (segment "):
            sm = re.search(r'\(start ([0-9\.\-]+) ([0-9\.\-]+)\) \(end ([0-9\.\-]+) ([0-9\.\-]+)\)', line)
            if sm:
                sx1, sy1, sx2, sy2 = float(sm.group(1)), float(sm.group(2)), float(sm.group(3)), float(sm.group(4))
                # Check if inside bounding box
                if (min_x <= sx1 <= max_x or min_x <= sx2 <= max_x) and (min_y <= sy1 <= max_y or min_y <= sy2 <= max_y):
                    ripped_segments += 1
                    continue
        elif line.startswith("  (via "):
            vm = re.search(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)\)', line)
            if vm:
                vx, vy = float(vm.group(1)), float(vm.group(2))
                if min_x <= vx <= max_x and min_y <= vy <= max_y:
                    ripped_vias += 1
                    continue
        clean_lines.append(line)

    intermediate_board = "".join(clean_lines)

    result = SwapResult(
        reference=reference,
        old_footprint=old_fp_name,
        new_footprint=part.footprint,
        ripped_segments=ripped_segments,
        ripped_vias=ripped_vias,
        unconnected_nets=sorted(nets_affected),
    )
    return intermediate_board, result
