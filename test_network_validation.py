"""Tests for power-system network integrity validation."""

import pytest

from power_system.io import load_network
from power_system.validation import validate_network


def write_valid_network(directory) -> None:
    """Write a small synthetic network with consistent voltage levels."""
    (directory / "bus_data.csv").write_text(
        "bus_id,name,base_kv,bus_type,vm_pu,va_deg,"
        "p_load_mw,q_load_mvar,in_service\n"
        "1,Grid Bus,132,SLACK,1.0,0,0,0,true\n"
        "2,Transformer LV Bus,33,PQ,1.0,0,0,0,true\n"
        "3,Feeder Bus,33,PQ,1.0,0,10,3,true\n",
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
        "L1,2,3,8,0.40,0.35,true\n",
        encoding="utf-8",
    )


def load_test_network(directory):
    """Load the synthetic network using the production CSV loader."""
    write_valid_network(directory)
    return load_network(directory, base_power_mva=100.0)


def test_valid_network_passes_validation(tmp_path) -> None:
    network = load_test_network(tmp_path)

    report = validate_network(network)

    assert report.is_valid
    assert report.errors == []


def test_transformer_voltage_mismatch_is_reported(tmp_path) -> None:
    network = load_test_network(tmp_path)

    # The transformer is rated 132/33 kV, but Bus 2 is changed to 11 kV.
    network.buses[2].base_kv = 11.0

    report = validate_network(network)

    assert not report.is_valid
    assert any(
        issue.code == "TRANSFORMER_BUS_VOLTAGE_MISMATCH"
        for issue in report.errors
    )


def test_missing_slack_bus_is_reported(tmp_path) -> None:
    network = load_test_network(tmp_path)
    network.buses[1].bus_type = "PQ"

    report = validate_network(network)

    assert not report.is_valid
    assert any(
        issue.code == "NO_SLACK_BUS"
        for issue in report.errors
    )


def test_disconnected_bus_is_reported(tmp_path) -> None:
    network = load_test_network(tmp_path)

    # Bus 3 is isolated when its only connecting line is out of service.
    network.lines["L1"].in_service = False

    report = validate_network(network)

    assert not report.is_valid
    assert any(
        issue.code == "BUS_UNREACHABLE_FROM_SLACK"
        and "bus 3" in issue.message
        for issue in report.errors
    )


def test_reversed_generator_limits_are_reported(tmp_path) -> None:
    network = load_test_network(tmp_path)
    generator = network.generators["G1"]

    generator.p_min_mw = 100.0
    generator.p_max_mw = 50.0

    report = validate_network(network)

    assert any(
        issue.code == "INVALID_GENERATOR_LIMITS"
        for issue in report.errors
    )