"""Component registry for twinpart library."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PARTS_ROOT = Path(__file__).resolve().parents[2] / "parts"


@dataclass(frozen=True, slots=True)
class PartEntry:
    component_id: str
    version: str
    kind: str
    status: str
    mpn: str
    manufacturer: str
    footprint: str
    directory: Path
    manifest_path: Path
    data: dict[str, Any]


def list_parts(parts_root: Path | None = None) -> list[PartEntry]:
    """Scan parts directory and return all discovered PartEntry records."""
    root = (parts_root or PARTS_ROOT).resolve()
    entries: list[PartEntry] = []
    for manifest_path in sorted(root.glob("**/*/manifest.json")):
        if manifest_path.is_symlink() or any(p.is_symlink() for p in manifest_path.parents if p != root and root in p.parents):
            continue
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            source = data.get("source") or {}
            eda = data.get("eda") or {}
            entries.append(
                PartEntry(
                    component_id=data.get("component_id", ""),
                    version=data.get("version", ""),
                    kind=data.get("kind", ""),
                    status=data.get("status", ""),
                    mpn=source.get("mpn", ""),
                    manufacturer=source.get("manufacturer", ""),
                    footprint=eda.get("footprint", ""),
                    directory=manifest_path.parent,
                    manifest_path=manifest_path,
                    data=data,
                )
            )
        except Exception:
            continue
    return entries


def get_part(component_id: str, parts_root: Path | None = None) -> PartEntry | None:
    """Find a specific part by its component_id."""
    for part in list_parts(parts_root):
        if part.component_id == component_id:
            return part
    return None
