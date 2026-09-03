"""Install parts from twinpart library into target projects."""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from .registry import PartEntry, get_part


def install_part(
    part_or_id: str | PartEntry,
    target_project: Path,
    parts_root: Path | None = None,
) -> dict[str, str]:
    """Install a component into target project directory.

    Target structure:
    - <target>/components/manifests/<component_id>.json
    - <target>/local.pretty/<FootprintName>.kicad_mod
    - <target>/local.symbols/<SymbolName>.kicad_sym
    - <target>/local.3dshapes/<ModelName>.step
    """
    part = get_part(part_or_id, parts_root) if isinstance(part_or_id, str) else part_or_id
    if part is None:
        raise ValueError(f"Component {part_or_id!r} not found in twinpart library")

    target = Path(target_project).resolve()
    installed: dict[str, str] = {}

    # 1. Manifest
    manifests_dir = target / "components" / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)
    dest_manifest = manifests_dir / f"{part.component_id}.json"
    shutil.copy2(part.manifest_path, dest_manifest)
    installed["manifest"] = str(dest_manifest)

    # 2. Footprint
    pretty_dir = target / "local.pretty"
    pretty_dir.mkdir(parents=True, exist_ok=True)
    for mod in part.directory.glob("*.kicad_mod"):
        dest_mod = pretty_dir / mod.name
        shutil.copy2(mod, dest_mod)
        installed["footprint"] = str(dest_mod)

    # 3. Symbol
    symbols_dir = target / "local.symbols"
    symbols_dir.mkdir(parents=True, exist_ok=True)
    for sym in part.directory.glob("*.kicad_sym"):
        dest_sym = symbols_dir / sym.name
        shutil.copy2(sym, dest_sym)
        installed["symbol"] = str(dest_sym)

    # 4. 3D Model
    shapes_dir = target / "local.3dshapes"
    shapes_dir.mkdir(parents=True, exist_ok=True)
    for step in part.directory.glob("*.step"):
        dest_step = shapes_dir / step.name
        shutil.copy2(step, dest_step)
        installed["model"] = str(dest_step)

    return installed
