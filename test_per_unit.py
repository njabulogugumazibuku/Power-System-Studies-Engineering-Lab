"""
Tests for the per-unit calculation engine.

The expected values in these tests come from the independent engineering
calculations performed during Milestone 01A and 01D.

These tests therefore act as acceptance criteria for the implementation.
"""

import math

import pytest

from power_system.calculations.per_unit import PerUnitSystem


def test_132kv_base_impedance() -> None:
    """Verify the impedance base for the 100 MVA / 132 kV system base."""
    pu_system = PerUnitSystem(
        base_power_mva=100,
        base_voltage_kv=132,
    )

    assert pu_system.base_impedance_ohm == pytest.approx(
        174.24,
        rel=1e-9,
    )


def test_33kv_base_impedance() -> None:
    """Verify the impedance base for the 100 MVA / 33 kV system base."""
    pu_system = PerUnitSystem(
        base_power_mva=100,
        base_voltage_kv=33,
    )

    assert pu_system.base_impedance_ohm == pytest.approx(
        10.89,
        rel=1e-9,
    )


def test_132kv_base_current() -> None:
    """Verify the base current at 132 kV."""
    pu_system = PerUnitSystem(
        base_power_mva=100,
        base_voltage_kv=132,
    )

    expected_current = (
        100_000_000
        / (math.sqrt(3) * 132_000)
    )

    assert pu_system.base_current_a == pytest.approx(
        expected_current,
        rel=1e-9,
    )


def test_33kv_base_current() -> None:
    """Verify the base current at 33 kV."""
    pu_system = PerUnitSystem(
        base_power_mva=100,
        base_voltage_kv=33,
    )

    expected_current = (
        100_000_000
        / (math.sqrt(3) * 33_000)
    )

    assert pu_system.base_current_a == pytest.approx(
        expected_current,
        rel=1e-9,
    )


def test_line_1_impedance_to_per_unit() -> None:
    """Verify conversion of L1 from ohms to per-unit."""
    pu_system = PerUnitSystem(
        base_power_mva=100,
        base_voltage_kv=33,
    )

    line_1_impedance = 3.20 + 2.80j

    expected_pu = (
        0.2938475665748393
        + 0.25711662075390266j
    )

    result = pu_system.impedance_to_pu(line_1_impedance)

    assert result.real == pytest.approx(
        expected_pu.real,
        rel=1e-9,
    )

    assert result.imag == pytest.approx(
        expected_pu.imag,
        rel=1e-9,
    )


def test_line_2_impedance_to_per_unit() -> None:
    """Verify conversion of L2 from ohms to per-unit."""
    pu_system = PerUnitSystem(
        base_power_mva=100,
        base_voltage_kv=33,
    )

    line_2_impedance = 5.40 + 4.56j

    expected_pu = (
        0.49586776859504134
        + 0.4187327823682278j
    )

    result = pu_system.impedance_to_pu(line_2_impedance)

    assert result.real == pytest.approx(
        expected_pu.real,
        rel=1e-9,
    )

    assert result.imag == pytest.approx(
        expected_pu.imag,
        rel=1e-9,
    )


def test_transformer_impedance_to_physical_ohms() -> None:
    """Verify conversion of the transformer impedance from pu to ohms."""
    pu_system = PerUnitSystem(
        base_power_mva=100,
        base_voltage_kv=33,
    )

    transformer_impedance_pu = 0.0 + 0.20j

    result = pu_system.impedance_from_pu(
        transformer_impedance_pu
    )

    expected = 0.0 + 2.178j

    assert result.real == pytest.approx(
        expected.real,
        abs=1e-12,
    )

    assert result.imag == pytest.approx(
        expected.imag,
        rel=1e-9,
    )


def test_impedance_conversion_is_reversible() -> None:
    """
    Verify that converting an impedance to pu and back returns the
    original physical impedance.
    """
    pu_system = PerUnitSystem(
        base_power_mva=100,
        base_voltage_kv=33,
    )

    original_impedance = 5.40 + 4.56j

    impedance_pu = pu_system.impedance_to_pu(
        original_impedance
    )

    reconstructed_impedance = pu_system.impedance_from_pu(
        impedance_pu
    )

    assert reconstructed_impedance.real == pytest.approx(
        original_impedance.real,
        rel=1e-9,
    )

    assert reconstructed_impedance.imag == pytest.approx(
        original_impedance.imag,
        rel=1e-9,
    )


def test_invalid_power_base_is_rejected() -> None:
    """Verify that a non-positive MVA base is rejected."""
    with pytest.raises(ValueError):
        PerUnitSystem(
            base_power_mva=0,
            base_voltage_kv=33,
        )


def test_invalid_voltage_base_is_rejected() -> None:
    """Verify that a non-positive voltage base is rejected."""
    with pytest.raises(ValueError):
        PerUnitSystem(
            base_power_mva=100,
            base_voltage_kv=0,
        )