"""
Power-system network model for the Power System Studies Engineering Lab.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .bus import Bus
from .generator import Generator
from .line import Line
from .transformer import Transformer


@dataclass
class Network:
    """
    Represent the complete electrical network.

    The Network object acts as the container for buses, generators,
    lines and transformers.

    Parameters
    ----------
    base_power_mva:
        Common system apparent-power base in MVA.

    frequency_hz:
        System frequency in Hz.

    buses:
        Collection of Bus objects.

    generators:
        Collection of Generator objects.

    lines:
        Collection of Line objects.

    transformers:
        Collection of Transformer objects.
    """

    base_power_mva: float
    frequency_hz: float = 50.0

    buses: dict[int, Bus] = field(default_factory=dict)
    generators: dict[str, Generator] = field(default_factory=dict)
    lines: dict[str, Line] = field(default_factory=dict)
    transformers: dict[str, Transformer] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        """Validate network-level parameters."""
        if self.base_power_mva <= 0:
            raise ValueError(
                "Network base power must be greater than zero."
            )

        if self.frequency_hz <= 0:
            raise ValueError(
                "Network frequency must be greater than zero."
            )

    def add_bus(self, bus: Bus) -> None:
        """Add a bus to the network."""
        if bus.bus_id in self.buses:
            raise ValueError(
                f"Bus {bus.bus_id} already exists."
            )

        self.buses[bus.bus_id] = bus

    def add_generator(self, generator: Generator) -> None:
        """Add a generator to the network."""
        if generator.generator_id in self.generators:
            raise ValueError(
                f"Generator {generator.generator_id} already exists."
            )

        if generator.bus_id not in self.buses:
            raise ValueError(
                f"Generator {generator.generator_id} references "
                f"unknown bus {generator.bus_id}."
            )

        self.generators[generator.generator_id] = generator

    def add_line(self, line: Line) -> None:
        """Add a line to the network."""
        if line.line_id in self.lines:
            raise ValueError(
                f"Line {line.line_id} already exists."
            )

        self._validate_bus_connection(
            line.from_bus,
            line.to_bus,
            line.line_id,
        )

        self.lines[line.line_id] = line

    def add_transformer(
        self,
        transformer: Transformer,
    ) -> None:
        """Add a transformer to the network."""
        if transformer.transformer_id in self.transformers:
            raise ValueError(
                f"Transformer {transformer.transformer_id} "
                f"already exists."
            )

        self._validate_bus_connection(
            transformer.from_bus,
            transformer.to_bus,
            transformer.transformer_id,
        )

        self.transformers[transformer.transformer_id] = transformer

    def _validate_bus_connection(
        self,
        from_bus: int,
        to_bus: int,
        element_id: str,
    ) -> None:
        """Ensure both ends of a branch reference existing buses."""
        if from_bus not in self.buses:
            raise ValueError(
                f"{element_id} references unknown "
                f"from_bus {from_bus}."
            )

        if to_bus not in self.buses:
            raise ValueError(
                f"{element_id} references unknown "
                f"to_bus {to_bus}."
            )