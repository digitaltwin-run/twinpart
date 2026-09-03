"""CLI interface for twinpart library."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from .registry import list_parts, get_part, PARTS_ROOT
from .installer import install_part


def cmd_list(args: argparse.Namespace) -> int:
    parts = list_parts()
    if args.kind:
        parts = [p for p in parts if p.kind == args.kind]
    if args.status:
        parts = [p for p in parts if p.status == args.status]

    if args.format == "json":
        print(json.dumps([p.data for p in parts], indent=2, ensure_ascii=False))
        return 0

    print(f"Znaleziono {len(parts)} komponent(ów) w bibliotece twinpart:")
    for p in parts:
        status_badge = f"[{p.status}]"
        mpn_info = f"({p.manufacturer} {p.mpn})" if p.mpn else ""
        print(f"  • {p.component_id:<25} {status_badge:<14} {p.kind:<12} {p.footprint:<30} {mpn_info}")
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    part = get_part(args.component_id)
    if part is None:
        print(f"Błąd: Nie znaleziono komponentu {args.component_id!r}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(part.data, indent=2, ensure_ascii=False))
        return 0

    data = part.data
    source = data.get("source") or {}
    mech = data.get("mechanical") or {}
    print(f"Komponent:    {part.component_id} (wersja {part.version})")
    print(f"Status:       {part.status}")
    print(f"Rodzaj:       {part.kind}")
    print(f"Producent:    {source.get('manufacturer', '—')} {source.get('mpn', '—')}")
    print(f"Footprint:    {part.footprint}")
    if mech:
        print(f"Wymiary:      {mech.get('length_mm', '—')} × {mech.get('width_mm', '—')} × {mech.get('height_mm', '—')} mm")
    print(f"Ścieżka:      {part.directory}")
    return 0


def cmd_install(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    try:
        installed = install_part(args.component_id, target)
        print(f"Zainstalowano {args.component_id} w {target}:")
        for k, v in installed.items():
            print(f"  ✓ {k:<10}: {v}")
        return 0
    except Exception as exc:
        print(f"Błąd instalacji: {exc}", file=sys.stderr)
        return 1


def cmd_check(args: argparse.Namespace) -> int:
    try:
        from twin_kicad.component import validate_component_manifest
    except ImportError:
        print("Brak twin-kicad; pomijam zaawansowaną walidację geometrii.", file=sys.stderr)
        return 0

    parts = list_parts()
    errors = 0
    print(f"Weryfikacja {len(parts)} komponent(ów) w {PARTS_ROOT}:")
    for p in parts:
        report = validate_component_manifest(p.data, p.directory)
        errs = [f for f in report.findings if f.severity == "error"]
        warns = [f for f in report.findings if f.severity == "warning"]
        if errs:
            errors += len(errs)
            print(f"  ✗ {p.component_id}: {len(errs)} błąd(ów)")
            for e in errs:
                print(f"      - [{e.code}] {e.message}")
        else:
            w_str = f" ({len(warns)} ostrzeżeń)" if warns else ""
            print(f"  ✔ {p.component_id}: OK{w_str}")

    if errors > 0:
        print(f"Wykryto {errors} błąd(ów) integralności.", file=sys.stderr)
        return 1
    print("Wszystkie komponenty są poprawne!")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="twinpart", description="Central hardware parts library for digitaltwin-run")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="Wypisz dostępne części")
    p_list.add_argument("--kind", help="Filtruj wg rodzaju (connector, mcu, passive, switch)")
    p_list.add_argument("--status", help="Filtruj wg statusu (qualified, provisional, quarantined)")
    p_list.add_argument("--format", choices=("text", "json"), default="text")
    p_list.set_defaults(func=cmd_list)

    p_info = sub.add_parser("info", help="Szczegóły wybranego komponentu")
    p_info.add_argument("component_id", help="Identyfikator części")
    p_info.add_argument("--format", choices=("text", "json"), default="text")
    p_info.set_defaults(func=cmd_info)

    p_inst = sub.add_parser("install", help="Zainstaluj komponent w projekcie docelowym")
    p_inst.add_argument("component_id", help="Identyfikator części")
    p_inst.add_argument("--target", default=".", help="Katalog docelowy projektu")
    p_inst.set_defaults(func=cmd_install)

    p_check = sub.add_parser("check", help="Sprawdź integralność biblioteki części")
    p_check.set_defaults(func=cmd_check)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
