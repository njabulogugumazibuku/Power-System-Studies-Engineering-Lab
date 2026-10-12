"""
Transformer model for the Power System Studies Engineering Lab.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Transformer:
    """
    Represent a two-winding transformer.

    Parameters
    ----------
    transformer_id:
        Unique transformer identifier.

    from_bus:
        HV-side bus ID.

    to_bus:
        LV-side bus ID.

    rated_mva:
        Transformer apparent-power rating in MVA.

    hv_kv:
        High-voltage winding rating in kV.

    lv_kv:
        Low-voltage winding rating in kV.

    r_pu:
        Transformer resistance on the project system base.

    x_pu:
        Transformer reactance on the project system base.

    tap_ratio:
        Transformer tap ratio. 1.0 represents nominal tap.

    in_service:
        Whether the transformer is currently in service.
    """

    transformer_id: str
    from_bus: int
    to_bus: int
    rated_mva: float
    hv_kv: float
    lv_kv: float
    r_pu: float
    x_pu: float
    tap_ratio: float = 1.0
    in_service: bool = True

    def __post_init__(self) -> None:
        """Validate transformer data."""
        if self.rated_mva <= 0:
            raise ValueError(
                "Transformer rating must be greater than zero."
            )

        if self.hv_kv <= 0 or self.lv_kv <= 0:
            raise ValueError(
                "Transformer voltage ratings must be greater than zero."
            )

        if self.r_pu < 0:
            raise ValueError(
                "Transformer resistance cannot be negative."
            )

        if self.x_pu < 0:
            raise ValueError(
                "Transformer reactance cannot be negative."
            )

        if self.tap_ratio <= 0:
            raise ValueError(
                "Transformer tap ratio must be greater than zero."
            )

        if self.from_bus == self.to_bus:
            raise ValueError(
                "A transformer cannot connect a bus to itself."
            )

    @property
    def impedance_pu(self) -> complex:
        """Return the transformer series impedance in per-unit."""
        return complex(self.r_pu, self.x_pu)