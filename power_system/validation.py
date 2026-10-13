"""Structural and engineering validation for power-system network models."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from power_system.models.network import Network


@dataclass(frozen=True)
class ValidationIssue:
    """A single network-validation finding."""

    severity: str
    code: str
    message: str


@dataclass
class ValidationReport:
    """Collection of validation findings for a network."""

    issues: list[ValidationIssue]

    @property
    def errors(self) -> list[ValidationIssue]:
        """Return findings that make the model invalid."""
        return [
            issue for issue in self.issues
            if issue.severity == "ERROR"
        ]

    @property
    def warnings(self) -> list[ValidationIssue]:
        """Return findings that require engineering review."""
        return [
            issue for issue in self.issues
            if issue.severity == "WARNING"
        ]

    @property
    def is_valid(self) -> bool:
        """Return True when no validation errors were found."""
        return not self.errors


def _close(
    actual: float,
    expected: float,
    *,
    tolerance: float = 0.01,
) -> bool:
    """Compare engineering values using a relative tolerance."""
    scale = max(abs(actual), abs(expected), 1.0)
    return abs(actual - expected) <= tolerance * scale


def validate_network(network: Network) -> ValidationReport:
    """Validate network parameters, references, and connectivity.

    This function does not modify the network. It reports errors that
    must be corrected and warnings that need engineering review.
    """
    issues: list[ValidationIssue] = []

    def add_error(code: str, message: str) -> None:
        issues.append(ValidationIssue("ERROR", code, message))

    def add_warning(code: str, message: str) -> None:
        issues.append(ValidationIssue("WARNING", code, message))

    # 1. System-level parameters
    if network.base_power_mva <= 0:
        add_error(
            "INVALID_SYSTEM_BASE",
            "System base power must be greater than zero.",
        )

    if network.frequency_hz <= 0:
        add_error(
            "INVALID_FREQUENCY",
            "System frequency must be greater than zero.",
        )

    if not network.buses:
        add_error("NO_BUSES", "The network contains no buses.")

    # 2. Bus identity and parameters
    for bus_id, bus in network.buses.items():
        if bus_id != bus.bus_id:
            add_error(
                "BUS_KEY_MISMATCH",
                f"Bus dictionary key {bus_id!r} does not match "
                f"the bus ID {bus.bus_id!r}.",
            )

        if bus.base_kv <= 0:
            add_error(
                "INVALID_BUS_BASE_KV",
                f"Bus {bus.bus_id} has a non-positive voltage base.",
            )

        if bus.vm_pu <= 0:
            add_error(
                "INVALID_BUS_VOLTAGE",
                f"Bus {bus.bus_id} has a non-positive voltage magnitude.",
            )

        if not bus.in_service:
            add_warning(
                "BUS_OUT_OF_SERVICE",
                f"Bus {bus.bus_id} is out of service.",
            )

    # 3. Generator references and limits
    for generator_id, generator in network.generators.items():
        if generator_id != generator.generator_id:
            add_error(
                "GENERATOR_KEY_MISMATCH",
                f"Generator dictionary key {generator_id!r} does not "
                f"match generator ID {generator.generator_id!r}.",
            )

        if generator.bus_id not in network.buses:
            add_error(
                "UNKNOWN_GENERATOR_BUS",
                f"Generator {generator.generator_id} references "
                f"unknown bus {generator.bus_id}.",
            )
            continue

        for minimum_name, maximum_name, label in (
            ("p_min_mw", "p_max_mw", "active power"),
            ("q_min_mvar", "q_max_mvar", "reactive power"),
        ):
            minimum = getattr(generator, minimum_name)
            maximum = getattr(generator, maximum_name)

            if (
                minimum is not None
                and maximum is not None
                and minimum > maximum
            ):
                add_error(
                    "INVALID_GENERATOR_LIMITS",
                    f"Generator {generator.generator_id} has a minimum "
                    f"{label} limit greater than its maximum limit.",
                )

    # 4. Transformer ratings, references, and voltage compatibility
    for transformer_id, transformer in network.transformers.items():
        if transformer_id != transformer.transformer_id:
            add_error(
                "TRANSFORMER_KEY_MISMATCH",
                f"Transformer dictionary key {transformer_id!r} does "
                f"not match transformer ID {transformer.transformer_id!r}.",
            )

        from_bus = network.buses.get(transformer.from_bus)
        to_bus = network.buses.get(transformer.to_bus)

        if from_bus is None or to_bus is None:
            add_error(
                "UNKNOWN_TRANSFORMER_BUS",
                f"Transformer {transformer.transformer_id} references "
                "a bus that does not exist.",
            )
            continue

        if transformer.rated_mva <= 0:
            add_error(
                "INVALID_TRANSFORMER_RATING",
                f"Transformer {transformer.transformer_id} must have "
                "a positive MVA rating.",
            )

        if transformer.hv_kv <= 0 or transformer.lv_kv <= 0:
            add_error(
                "INVALID_TRANSFORMER_VOLTAGE",
                f"Transformer {transformer.transformer_id} must have "
                "positive HV and LV voltage ratings.",
            )
        elif transformer.hv_kv <= transformer.lv_kv:
            add_error(
                "INVALID_TRANSFORMER_VOLTAGE_ORDER",
                f"Transformer {transformer.transformer_id} has an HV "
                "rating that is not greater than its LV rating.",
            )
        else:
            forward_match = (
                _close(from_bus.base_kv, transformer.hv_kv)
                and _close(to_bus.base_kv, transformer.lv_kv)
            )
            reverse_match = (
                _close(from_bus.base_kv, transformer.lv_kv)
                and _close(to_bus.base_kv, transformer.hv_kv)
            )

            if not (forward_match or reverse_match):
                add_error(
                    "TRANSFORMER_BUS_VOLTAGE_MISMATCH",
                    f"Transformer {transformer.transformer_id} is rated "
                    f"{transformer.hv_kv:g}/{transformer.lv_kv:g} kV, "
                    f"but connects buses with base voltages "
                    f"{from_bus.base_kv:g}/{to_bus.base_kv:g} kV.",
                )

        if transformer.r_pu < 0:
            add_error(
                "NEGATIVE_TRANSFORMER_RESISTANCE",
                f"Transformer {transformer.transformer_id} has "
                "negative per-unit resistance.",
            )

        if transformer.x_pu < 0:
            add_error(
                "NEGATIVE_TRANSFORMER_REACTANCE",
                f"Transformer {transformer.transformer_id} has "
                "negative per-unit reactance.",
            )

        if transformer.tap_ratio <= 0:
            add_error(
                "INVALID_TRANSFORMER_TAP",
                f"Transformer {transformer.transformer_id} must have "
                "a positive tap ratio.",
            )

    # 5. Line parameters and references
    for line_id, line in network.lines.items():
        if line_id != line.line_id:
            add_error(
                "LINE_KEY_MISMATCH",
                f"Line dictionary key {line_id!r} does not match "
                f"line ID {line.line_id!r}.",
            )

        from_bus = network.buses.get(line.from_bus)
        to_bus = network.buses.get(line.to_bus)

        if from_bus is None or to_bus is None:
            add_error(
                "UNKNOWN_LINE_BUS",
                f"Line {line.line_id} references a bus that does not exist.",
            )
            continue

        if line.from_bus == line.to_bus:
            add_error(
                "LINE_SELF_CONNECTION",
                f"Line {line.line_id} connects a bus to itself.",
            )

        if line.length_km <= 0:
            add_error(
                "INVALID_LINE_LENGTH",
                f"Line {line.line_id} must have a positive length.",
            )

        if line.r_ohm_per_km < 0:
            add_error(
                "NEGATIVE_LINE_RESISTANCE",
                f"Line {line.line_id} has negative resistance per km.",
            )

        if line.x_ohm_per_km < 0:
            add_error(
                "NEGATIVE_LINE_REACTANCE",
                f"Line {line.line_id} has negative reactance per km.",
            )

        if (
            from_bus.base_kv > 0
            and to_bus.base_kv > 0
            and not _close(from_bus.base_kv, to_bus.base_kv)
        ):
            add_error(
                "LINE_VOLTAGE_LEVEL_MISMATCH",
                f"Line {line.line_id} connects buses with different "
                "voltage bases. Represent a voltage transformation "
                "with a transformer instead.",
            )

    # 6. Slack/reference bus configuration
    slack_types = {"SLACK", "SWING", "REFERENCE"}
    slack_buses = [
        bus for bus in network.buses.values()
        if str(bus.bus_type).strip().upper() in slack_types
        and bus.in_service
    ]

    if len(slack_buses) == 0:
        add_error(
            "NO_SLACK_BUS",
            "No in-service slack/reference bus was found.",
        )
    elif len(slack_buses) > 1:
        add_error(
            "MULTIPLE_SLACK_BUSES",
            f"Found {len(slack_buses)} in-service slack/reference buses. "
            "This lab's conventional load-flow model expects one.",
        )

    # A slack bus should have an in-service generator or external-grid
    # equivalent connected to it.
    for bus in slack_buses:
        source_found = any(
            generator.in_service
            and generator.bus_id == bus.bus_id
            for generator in network.generators.values()
        )
        if not source_found:
            add_warning(
                "SLACK_WITHOUT_GENERATOR",
                f"Slack bus {bus.bus_id} has no in-service generator "
                "object connected to it. Confirm how the external grid "
                "is represented in the model.",
            )

    # 7. In-service connectivity: find buses reachable from the slack bus.
    if len(slack_buses) == 1:
        adjacency: dict[int, set[int]] = {
            bus_id: set()
            for bus_id, bus in network.buses.items()
            if bus.in_service
        }

        for branch in (
            *network.lines.values(),
            *network.transformers.values(),
        ):
            if not branch.in_service:
                continue

            if (
                branch.from_bus in adjacency
                and branch.to_bus in adjacency
            ):
                adjacency[branch.from_bus].add(branch.to_bus)
                adjacency[branch.to_bus].add(branch.from_bus)

        start_bus = slack_buses[0].bus_id
        reachable: set[int] = set()

        if start_bus in adjacency:
            queue = deque([start_bus])
            reachable.add(start_bus)

            while queue:
                current_bus = queue.popleft()

                for neighbour in adjacency[current_bus]:
                    if neighbour not in reachable:
                        reachable.add(neighbour)
                        queue.append(neighbour)

        for bus_id in adjacency:
            if bus_id not in reachable:
                add_error(
                    "BUS_UNREACHABLE_FROM_SLACK",
                    f"In-service bus {bus_id} is not reachable from "
                    f"slack bus {start_bus} through in-service branches.",
                )

    return ValidationReport(issues=issues)