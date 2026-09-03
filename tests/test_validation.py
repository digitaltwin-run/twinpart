import pytest
from twin_kicad.component import validate_component_manifest
from twinpart.registry import list_parts


@pytest.mark.parametrize("part", list_parts(), ids=lambda p: p.component_id)
def test_all_parts_manifests_are_valid(part) -> None:
    report = validate_component_manifest(part.data, part.directory)
    errors = [f"{f.code}: {f.message}" for f in report.findings if f.severity == "error"]
    assert not errors, f"Validation errors for {part.component_id}: {errors}"
