"""
Bus model for the Power System Studies Engineering Lab.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Bus:
    """
    Represent an electrical bus in the power-system model.

    Parameters
    ----------
    bus_id:
        Unique numerical identifier for the bus.

    name:
        Human-readable bus name.

    base_kv:
        Voltage base / nominal voltage in kV.

    bus_type:
        Power-flow bus type. Initially supported values are
        "SLACK", "PV", and "PQ".

    vm_pu:
        Initial or specified voltage magnitude in per-unit.

    va_deg:
        Initial or specified voltage angle in degrees.

    p_load_mw:
        Active power consumed by the connected load in MW.

    q_load_mvar:
        Reactive power consumed by the connected load in MVAr.

    in_service:
        Whether the bus is currently in service.
    """

    bus_id: int
    name: str
    base_kv: float
    bus_type: str
    vm_pu: float = 1.0
    va_deg: float = 0.0
    p_load_mw: float = 0.0
    q_load_mvar: float = 0.0
    in_service: bool = True

    def __post_init__(self) -> None:
        """Validate the bus data."""
        valid_bus_types = {"SLACK", "PV", "PQ"}

        if self.bus_id <= 0:
            raise ValueError("Bus ID must be greater than zero.")

        if self.base_kv <= 0:
            raise ValueError("Bus base voltage must be greater than zero.")

        if self.bus_type not in valid_bus_types:
            raise ValueError(
                f"Invalid bus type '{self.bus_type}'. "
                f"Expected one of {sorted(valid_bus_types)}."
            )

        if self.vm_pu <= 0:
            raise ValueError(
                "Initial voltage magnitude must be greater than zero."
            )