"""
Transmission/distribution line model for the Power System Studies
Engineering Lab.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Line:
    """
    Represent a balanced three-phase line using a lumped series impedance.

    Parameters
    ----------
    line_id:
        Unique line identifier.

    from_bus:
        Sending-end bus ID.

    to_bus:
        Receiving-end bus ID.

    length_km:
        Physical line length in kilometres.

    r_ohm_per_km:
        Series resistance per kilometre.

    x_ohm_per_km:
        Series reactance per kilometre.

    in_service:
        Whether the line is currently in service.

    Notes
    -----
    The initial project model neglects line shunt capacitance.

    Therefore the line is represented only by:

        Z = R + jX
    """

    line_id: str
    from_bus: int
    to_bus: int
    length_km: float
    r_ohm_per_km: float
    x_ohm_per_km: float
    in_service: bool = True

    def __post_init__(self) -> None:
        """Validate line data."""
        if self.length_km <= 0:
            raise ValueError("Line length must be greater than zero.")

        if self.r_ohm_per_km < 0:
            raise ValueError(
                "Line resistance per kilometre cannot be negative."
            )

        if self.x_ohm_per_km < 0:
            raise ValueError(
                "Line reactance per kilometre cannot be negative."
            )

        if self.from_bus == self.to_bus:
            raise ValueError(
                "A line cannot connect a bus to itself."
            )

    @property
    def resistance_ohm(self) -> float:
        """Return the total series resistance in ohms."""
        return self.length_km * self.r_ohm_per_km

    @property
    def reactance_ohm(self) -> float:
        """Return the total series reactance in ohms."""
        return self.length_km * self.x_ohm_per_km

    @property
    def impedance_ohm(self) -> complex:
        """
        Return the total series impedance in ohms.

        Z = R + jX
        """
        return complex(
            self.resistance_ohm,
            self.reactance_ohm,
        )