
"""
Per-unit system calculations for the Power System Studies Engineering Lab.

This module contains the engineering calculations required to establish
and use a common per-unit system for the fictional educational network.

The primary relationships implemented here are:

    Z_base = V_base^2 / S_base
    I_base = S_base / (sqrt(3) * V_base)
    Z_pu = Z_actual / Z_base
    Z_actual = Z_pu * Z_base

    Z_pu,new = Z_pu,old * (S_base,new / S_base,old)
                         * (V_base,old / V_base,new)^2

For three-phase systems, voltage is interpreted as line-to-line RMS voltage
and apparent power is the three-phase system apparent power.

Public methods use engineering units:

    Voltage        -> kV
    Apparent power -> MVA
    Current        -> A
    Impedance      -> ohms

Per-unit quantities are dimensionless.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from numbers import Real
from typing import Union


Impedance = Union[Real, complex]


def _validate_positive_finite(value: float, name: str) -> None:
    """Raise ValueError unless value is a positive, finite real number."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a positive, finite number.")

    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a positive, finite number.")


@dataclass(frozen=True)
class PerUnitSystem:
    """
    Represent the common base quantities for a power-system study.

    Parameters
    ----------
    base_power_mva:
        Three-phase apparent-power base in MVA.
    base_voltage_kv:
        Line-to-line voltage base in kV.

    Notes
    -----
    The voltage base must correspond to the voltage level at which a
    calculation is being performed.

    Example system bases for the project are 100 MVA / 132 kV and
    100 MVA / 33 kV.
    """

    base_power_mva: float
    base_voltage_kv: float

    def __post_init__(self) -> None:
        """Validate the selected system bases."""
        _validate_positive_finite(
            self.base_power_mva, "Base apparent power"
        )
        _validate_positive_finite(
            self.base_voltage_kv, "Base voltage"
        )

    @property
    def base_impedance_ohm(self) -> float:
        """
        Calculate base impedance in ohms.

        Z_base = V_base^2 / S_base

        With voltage in kV and apparent power in MVA, the result is ohms.
        """
        return (self.base_voltage_kv ** 2) / self.base_power_mva

    @property
    def base_current_a(self) -> float:
        """
        Calculate base current in amperes for a balanced three-phase system.

        I_base = S_base / (sqrt(3) * V_base)
        """
        base_power_va = self.base_power_mva * 1_000_000
        base_voltage_v = self.base_voltage_kv * 1_000

        return base_power_va / (
            math.sqrt(3) * base_voltage_v
        )

    def impedance_to_pu(self, impedance_ohm: Impedance) -> complex:
        """
        Convert physical impedance in ohms to per-unit.

        Parameters
        ----------
        impedance_ohm:
            Real or complex physical impedance in ohms.

        Returns
        -------
        complex
            Impedance expressed in per-unit.
        """
        return complex(impedance_ohm) / self.base_impedance_ohm

    def impedance_from_pu(self, impedance_pu: Impedance) -> complex:
        """
        Convert per-unit impedance to physical ohms.

        Parameters
        ----------
        impedance_pu:
            Real or complex impedance expressed in per-unit.

        Returns
        -------
        complex
            Corresponding physical impedance in ohms.
        """
        return complex(impedance_pu) * self.base_impedance_ohm

    @staticmethod
    def convert_impedance_base(
        impedance_pu: Impedance,
        old_base_power_mva: float,
        new_base_power_mva: float,
        old_base_voltage_kv: float | None = None,
        new_base_voltage_kv: float | None = None,
    ) -> complex:
        """
        Convert per-unit impedance from an old base to a new base.

        The conversion is:

            Z_pu,new = Z_pu,old
                       * (S_base,new / S_base,old)
                       * (V_base,old / V_base,new)^2

        If both voltage bases are omitted, their ratio is assumed to be 1.
        If voltage conversion is required, both voltage bases must be given.
        The voltage bases must refer to the same electrical side of the
        equipment; this method does not model transformer turns ratios.

        Parameters
        ----------
        impedance_pu:
            Real or complex impedance on the old per-unit base.
        old_base_power_mva:
            Old three-phase apparent-power base in MVA.
        new_base_power_mva:
            New three-phase apparent-power base in MVA.
        old_base_voltage_kv:
            Old line-to-line voltage base in kV, optional.
        new_base_voltage_kv:
            New line-to-line voltage base in kV, optional.

        Returns
        -------
        complex
            Impedance expressed on the new per-unit base.

        Raises
        ------
        ValueError
            If any supplied base is not positive and finite, or only one
            of the two voltage bases is supplied.
        """
        _validate_positive_finite(
            old_base_power_mva, "Old power base"
        )
        _validate_positive_finite(
            new_base_power_mva, "New power base"
        )

        if (old_base_voltage_kv is None) != (
            new_base_voltage_kv is None
        ):
            raise ValueError(
                "Both old and new voltage bases must be supplied together."
            )

        voltage_factor = 1.0

        if old_base_voltage_kv is not None:
            _validate_positive_finite(
                old_base_voltage_kv, "Old voltage base"
            )
            _validate_positive_finite(
                new_base_voltage_kv, "New voltage base"
            )

            voltage_factor = (
                old_base_voltage_kv / new_base_voltage_kv
            ) ** 2

        power_factor = (
            new_base_power_mva / old_base_power_mva
        )

        return complex(impedance_pu) * power_factor * voltage_factor
