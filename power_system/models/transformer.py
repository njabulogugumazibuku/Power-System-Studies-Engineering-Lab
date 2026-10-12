"""Transformer model for the Power System Studies Engineering Lab."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Transformer:
    """Represent a two-winding transformer using per-unit impedance."""

    transformer_id: str
    from_bus: int
    to_bus: int
    rated_mva: float
    hv_kv: float
    lv_kv: float
    r_pu: float
    x_pu: float
    in_service: bool = True

    def __post_init__(self) -> None:
        """Validate transformer nameplate and impedance data."""
        if self.rated_mva <= 0:
            raise ValueError("Transformer rated power must be greater than zero.")
        if self.hv_kv <= 0 or self.lv_kv <= 0:
            raise ValueError("Transformer voltage ratings must be greater than zero.")
        if self.r_pu < 0 or self.x_pu < 0:
            raise ValueError("Transformer resistance and reactance cannot be negative.")
        if self.from_bus == self.to_bus:
            raise ValueError("A transformer cannot connect a bus to itself.")

    @property
    def impedance_pu(self) -> complex:
        """Return transformer series impedance in per-unit."""
        return complex(self.r_pu, self.x_pu)