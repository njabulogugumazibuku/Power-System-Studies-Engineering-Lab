"""Tests for loading engineering data from CSV files."""

import pytest

from power_system.io import load_network


def write_test_csv_files(directory) -> None:
    """Create a small, synthetic two-bus test network."""
    (directory / "bus_data.csv").write_text(
        "bus_id,name,base_kv,bus_type,vm_pu,va_deg,"
        "p_load_mw,q_load_mvar,in_service\n"
        "1,Grid Bus,132,SLACK,1.0,0,0,0,true\n"
        "2,Load Bus,33,PQ,1.0,0,10,3.0,true\n",
        encoding="utf-8",
    )

    (directory / "generator_data.csv").write_text(
        "generator_id,bus_id,name,generator_type,vm_pu,"
        "p_min_mw,p_max_mw,q_min_mvar,q_max_mvar,in_service\n"
        "G1,1,External Grid,SLACK,1.0,,,,,true\n",
        encoding="utf-8",
    )

    (directory / "transformer_data.csv").write_text(
        "transformer_id,from_bus,to_bus,rated_mva,hv_kv,"
        "lv_kv,r_pu,x_pu,tap_ratio,in_service\n"
        "T1,1,2,50,132,33,0.0,0.2,1.0,true\n",
        encoding="utf-8",
    )

    (directory / "line_data.csv").write_text(
        "line_id,from_bus,to_bus,length_km,"
        "r_ohm_per_km,x_ohm_per_km,in_service\n"
        "L1,2,1,8,0.40,0.35,true\n",
        encoding="utf-8",
    )


def test_load_network_constructs_all_components(tmp_path) -> None:
    """Verify that all four files become network objects."""
    write_test_csv_files(tmp_path)

    network = load_network(
        data_dir=tmp_path,
        base_power_mva=100,
    )

    assert network.base_power_mva == pytest.approx(100)
    assert network.frequency_hz == pytest.approx(50)

    assert set(network.buses) == {1, 2}
    assert set(network.generators) == {"G1"}
    assert set(network.transformers) == {"T1"}
    assert set(network.lines) == {"L1"}

    assert network.buses[2].p_load_mw == pytest.approx(10)
    assert network.lines["L1"].impedance_ohm == pytest.approx(
        3.2 + 2.8j
    )


def test_optional_generator_limits_are_none(tmp_path) -> None:
    """Empty optional CSV fields must remain unknown, not become zero."""
    write_test_csv_files(tmp_path)

    network = load_network(tmp_path, base_power_mva=100)
    generator = network.generators["G1"]

    assert generator.p_min_mw is None
    assert generator.p_max_mw is None
    assert generator.q_min_mvar is None
    assert generator.q_max_mvar is None


def test_missing_csv_file_is_reported(tmp_path) -> None:
    """A missing input file should produce a useful error."""
    with pytest.raises(FileNotFoundError):
        load_network(tmp_path, base_power_mva=100)


def test_unknown_bus_reference_is_rejected(tmp_path) -> None:
    """A branch must not reference a bus absent from the model."""
    write_test_csv_files(tmp_path)

    line_file = tmp_path / "line_data.csv"
    content = line_file.read_text(encoding="utf-8")
    line_file.write_text(
        content.replace("L1,2,1,8", "L1,2,99,8"),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="unknown.*bus"):
        load_network(tmp_path, base_power_mva=100)


def test_missing_required_column_is_reported(tmp_path) -> None:
    """Required CSV columns must not be silently omitted."""
    write_test_csv_files(tmp_path)

    bus_file = tmp_path / "bus_data.csv"
    content = bus_file.read_text(encoding="utf-8")
    content = content.replace("base_kv,", "")
    bus_file.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError, match="missing required columns"):
        load_network(tmp_path, base_power_mva=100)