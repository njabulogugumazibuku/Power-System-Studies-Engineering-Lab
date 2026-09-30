"""
Per-unit system calculations for the Power System Studies Engineering Lab.

This module contains the engineering calculations required to establish
and use a common per-unit system for the fictional educational network.

The primary relationships implemented here are:

    Z_base = V_base^2 / S_base

    I_base = S_base / (sqrt(3) * V_base)

    Z_pu = Z_actual / Z_base

    Z_actual = Z_pu * Z_base

For three-phase systems, voltage is interpreted as line-to-line RMS voltage
and apparent power is the three-phase system apparent power.

All quantities supplied to the public methods use engineering units:

    Voltage       -> kV
    Apparent power -> MVA
    Current       -> A
    Impedance     -> ohms

The per-unit quantities returned by the conversion methods are dimensionless.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


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
    The voltage base must correspond to the voltage level at which the
    calculation is being performed.

    For example, our project uses:

        100 MVA / 132 kV
        100 MVA / 33 kV

    as two voltage-level bases on the same 100 MVA system base.
    """

    base_power_mva: float
    base_voltage_kv: float

    def __post_init__(self) -> None:
        """Validate the selected system bases."""
        if self.base_power_mva <= 0:
            raise ValueError("Base apparent power must be greater than zero.")

        if self.base_voltage_kv <= 0:
            raise ValueError("Base voltage must be greater than zero.")

    @property
    def base_impedance_ohm(self) -> float:
        """
        Calculate the base impedance in ohms.

        For a three-phase system using line-to-line voltage:

            Z_base = V_base^2 / S_base

        When voltage is expressed in kV and apparent power in MVA,
        the result is directly obtained in ohms.
        """
        return (self.base_voltage_kv ** 2) / self.base_power_mva

    @property
    def base_current_a(self) -> float:
        """
        Calculate the base current in amperes.

        For a balanced three-phase system:

            I_base = S_base / (sqrt(3) * V_base)

        MVA and kV are converted to VA and V internally.
        """
        base_power_va = self.base_power_mva * 1_000_000
        base_voltage_v = self.base_voltage_kv * 1_000

        return base_power_va / (
            math.sqrt(3) * base_voltage_v
        )

    def impedance_to_pu(self, impedance_ohm: complex) -> complex:
        """
        Convert a physical impedance in ohms to per-unit.

        Parameters
        ----------
        impedance_ohm:
            Complex physical impedance in ohms.

        Returns
        -------
        complex
            The impedance expressed in per-unit.
        """
        return impedance_ohm / self.base_impedance_ohm

    def impedance_from_pu(self, impedance_pu: complex) -> complex:
        """
        Convert a per-unit impedance to physical ohms.

        Parameters
        ----------
        impedance_pu:
            Complex impedance expressed in per-unit.

        Returns
        -------
        complex
            The corresponding physical impedance in ohms.
        """
        return impedance_pu * self.base_impedance_ohm