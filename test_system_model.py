"""
Tests for the core power-system engineering models.
"""

import pytest

from power_system.models import (
    Bus,
    Generator,
    Line,
    Network,
    Transformer,
)


def test_line_impedance() -> None:
    """Verify the physical impedance calculation for L1."""
    line = Line(
        line_id="L1",
        from_bus=2,
        to_bus=3,
        length_km=8,
        r_ohm_per_km=0.40,
        x_ohm_per_km=0.35,
    )

    assert line.resistance_ohm == pytest.approx(3.20)
    assert line.reactance_ohm == pytest.approx(2.80)
    assert line.impedance_ohm == pytest.approx(3.20 + 2.80j)


def test_transformer_impedance() -> None:
    """Verify the transformer per-unit impedance."""
    transformer = Transformer(
        transformer_id="T1",
        from_bus=1,
        to_bus=2,
        rated_mva=50,
        hv_kv=132,
        lv_kv=33,
        r_pu=0.0,
        x_pu=0.20,
    )

    assert transformer.impedance_pu == pytest.approx(
        0.0 + 0.20j
    )


def test_bus_creation() -> None:
    """Verify creation of a valid bus."""
    bus = Bus(
        bus_id=3,
        name="Feeder 1 Bus",
        base_kv=33,
        bus_type="PQ",
        p_load_mw=10,
        q_load_mvar=3.2869,
    )

    assert bus.bus_id == 3
    assert bus.base_kv == 33
    assert bus.bus_type == "PQ"
    assert bus.p_load_mw == pytest.approx(10)
    assert bus.q_load_mvar == pytest.approx(3.2869)


def test_generator_creation() -> None:
    """Verify creation of the external grid source."""
    generator = Generator(
        generator_id="G1",
        bus_id=1,
        name="External Grid",
        generator_type="SLACK",
        vm_pu=1.0,
    )

    assert generator.bus_id == 1
    assert generator.generator_type == "SLACK"
    assert generator.vm_pu == pytest.approx(1.0)


def test_network_accepts_valid_components() -> None:
    """Verify that valid components can be assembled."""
    network = Network(
        base_power_mva=100,
        frequency_hz=50,
    )

    bus_1 = Bus(
        bus_id=1,
        name="Grid Bus",
        base_kv=132,
        bus_type="SLACK",
    )

    bus_2 = Bus(
        bus_id=2,
        name="Main 33 kV Bus",
        base_kv=33,
        bus_type="PQ",
    )

    network.add_bus(bus_1)
    network.add_bus(bus_2)

    generator = Generator(
        generator_id="G1",
        bus_id=1,
        name="External Grid",
        generator_type="SLACK",
    )

    transformer = Transformer(
        transformer_id="T1",
        from_bus=1,
        to_bus=2,
        rated_mva=50,
        hv_kv=132,
        lv_kv=33,
        r_pu=0.0,
        x_pu=0.20,
    )

    network.add_generator(generator)
    network.add_transformer(transformer)

    assert len(network.buses) == 2
    assert len(network.generators) == 1
    assert len(network.transformers) == 1


def test_network_rejects_unknown_bus_connection() -> None:
    """Verify that branches cannot reference unknown buses."""
    network = Network(base_power_mva=100)

    network.add_bus(
        Bus(
            bus_id=1,
            name="Grid Bus",
            base_kv=132,
            bus_type="SLACK",
        )
    )

    line = Line(
        line_id="L1",
        from_bus=1,
        to_bus=99,
        length_km=8,
        r_ohm_per_km=0.40,
        x_ohm_per_km=0.35,
    )

    with pytest.raises(ValueError):
        network.add_line(line)


def test_network_rejects_duplicate_bus() -> None:
    """Verify that duplicate bus IDs are rejected."""
    network = Network(base_power_mva=100)

    bus = Bus(
        bus_id=1,
        name="Grid Bus",
        base_kv=132,
        bus_type="SLACK",
    )

    network.add_bus(bus)

    with pytest.raises(ValueError):
        network.add_bus(bus)