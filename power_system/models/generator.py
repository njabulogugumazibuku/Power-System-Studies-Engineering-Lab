"""
Generator model for the Power System Studies Engineering Lab.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Generator:
    """
    Represent a generator or external grid source.

    Parameters
    ----------
    generator_id:
        Unique generator identifier.

    bus_id:
        ID of the bus to which the generator is connected.

    name:
        Human-readable generator name.

    generator_type:
        Generator operating type, such as "SLACK" or "PV".

    vm_pu:
        Specified voltage magnitude in per-unit.

    p_min_mw:
        Minimum active power output, if defined.

    p_max_mw:
        Maximum active power output, if defined.

    q_min_mvar:
        Minimum reactive power output, if defined.

    q_max_mvar:
        Maximum reactive power output, if defined.

    in_service:
        Whether the generator is currently in service.
    """

    generator_id: str
    bus_id: int
    name: str
    generator_type: str
    vm_pu: float = 1.0
    p_min_mw: float | None = None
    p_max_mw: float | None = None
    q_min_mvar: float | None = None
    q_max_mvar: float | None = None
    in_service: bool = True

    def __post_init__(self) -> None:
        """Validate generator data."""
        valid_generator_types = {"SLACK", "PV"}

        if self.generator_type not in valid_generator_types:
            raise ValueError(
                f"Invalid generator type '{self.generator_type}'. "
                f"Expected one of {sorted(valid_generator_types)}."
            )

        if self.vm_pu <= 0:
            raise ValueError(
                "Generator voltage magnitude must be greater than zero."
            )