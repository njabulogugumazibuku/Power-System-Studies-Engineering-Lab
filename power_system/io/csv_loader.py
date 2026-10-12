"""
CSV loader for the Power System Studies Engineering Lab.

Reads synthetic engineering data and constructs a validated Network.

Expected input files:
    bus_data.csv
    generator_data.csv
    transformer_data.csv
    line_data.csv
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from power_system.models import (
    Bus,
    Generator,
    Line,
    Network,
    Transformer,
)


BUS_COLUMNS = {
    "bus_id", "name", "base_kv", "bus_type", "vm_pu",
    "va_deg", "p_load_mw", "q_load_mvar", "in_service",
}

GENERATOR_COLUMNS = {
    "generator_id", "bus_id", "name", "generator_type", "vm_pu",
    "p_min_mw", "p_max_mw", "q_min_mvar", "q_max_mvar",
    "in_service",
}

TRANSFORMER_COLUMNS = {
    "transformer_id", "from_bus", "to_bus", "rated_mva",
    "hv_kv", "lv_kv", "r_pu", "x_pu", "tap_ratio",
    "in_service",
}

LINE_COLUMNS = {
    "line_id", "from_bus", "to_bus", "length_km",
    "r_ohm_per_km", "x_ohm_per_km", "in_service",
}


def _read_csv(
    path: Path,
    required_columns: set[str],
) -> list[dict[str, str]]:
    """Read a CSV file and verify its required column names."""
    if not path.is_file():
        raise FileNotFoundError(f"Required data file not found: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError(f"CSV file has no header: {path}")

        headers = {
            header.strip()
            for header in reader.fieldnames
            if header is not None
        }

        missing = required_columns - headers
        if missing:
            raise ValueError(
                f"{path.name} is missing required columns: "
                f"{sorted(missing)}"
            )

        rows = []
        for row_number, row in enumerate(reader, start=2):
            # Strip whitespace from both column names and text values.
            cleaned = {
                key.strip(): value.strip() if value is not None else ""
                for key, value in row.items()
                if key is not None
            }

            if not any(cleaned.values()):
                continue

            rows.append(cleaned)

    return rows


def _required(
    row: dict[str, str],
    column: str,
    filename: str,
    row_number: int,
) -> str:
    """Return a required non-empty CSV value."""
    value = row.get(column, "")

    if value == "":
        raise ValueError(
            f"{filename}, row {row_number}: "
            f"'{column}' must not be empty."
        )

    return value


def _number(
    row: dict[str, str],
    column: str,
    filename: str,
    row_number: int,
) -> float:
    """Read a required numeric value with a useful error message."""
    value = _required(row, column, filename, row_number)

    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(
            f"{filename}, row {row_number}: "
            f"'{column}' must be numeric; received {value!r}."
        ) from exc


def _integer(
    row: dict[str, str],
    column: str,
    filename: str,
    row_number: int,
) -> int:
    """Read an integer field without silently truncating decimals."""
    value = _required(row, column, filename, row_number)

    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(
            f"{filename}, row {row_number}: "
            f"'{column}' must be an integer; received {value!r}."
        ) from exc

    return parsed


def _optional_number(
    row: dict[str, str],
    column: str,
    filename: str,
    row_number: int,
) -> float | None:
    """Return None for an empty optional numeric field."""
    value = row.get(column, "")

    if value == "":
        return None

    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(
            f"{filename}, row {row_number}: "
            f"'{column}' must be numeric or empty; received {value!r}."
        ) from exc


def _boolean(
    row: dict[str, str],
    column: str,
    filename: str,
    row_number: int,
) -> bool:
    """Parse explicit Boolean representations from CSV."""
    value = _required(row, column, filename, row_number).lower()

    if value in {"true", "1", "yes"}:
        return True

    if value in {"false", "0", "no"}:
        return False

    raise ValueError(
        f"{filename}, row {row_number}: "
        f"'{column}' must be true/false, 1/0, or yes/no."
    )


def _text(
    row: dict[str, str],
    column: str,
    filename: str,
    row_number: int,
) -> str:
    """Read a required text field."""
    return _required(row, column, filename, row_number)


def load_network(
    data_dir: str | Path,
    base_power_mva: float,
    frequency_hz: float = 50.0,
) -> Network:
    """
    Load the four engineering CSV files into a Network.

    Parameters
    ----------
    data_dir:
        Directory containing the four CSV input files.

    base_power_mva:
        Common apparent-power base in MVA.

    frequency_hz:
        System frequency in Hz. Defaults to 50 Hz for this project.

    Returns
    -------
    Network
        A network containing the buses, generators, lines and transformers.

    Raises
    ------
    FileNotFoundError
        If a required input file does not exist.

    ValueError
        If the data has missing columns, invalid values, duplicate IDs,
        or references to buses that do not exist.
    """
    directory = Path(data_dir)

    bus_rows = _read_csv(directory / "bus_data.csv", BUS_COLUMNS)
    generator_rows = _read_csv(
        directory / "generator_data.csv", GENERATOR_COLUMNS
    )
    transformer_rows = _read_csv(
        directory / "transformer_data.csv", TRANSFORMER_COLUMNS
    )
    line_rows = _read_csv(directory / "line_data.csv", LINE_COLUMNS)

    network = Network(
        base_power_mva=base_power_mva,
        frequency_hz=frequency_hz,
    )

    for row_number, row in enumerate(bus_rows, start=2):
        filename = "bus_data.csv"

        bus = Bus(
            bus_id=_integer(row, "bus_id", filename, row_number),
            name=_text(row, "name", filename, row_number),
            base_kv=_number(row, "base_kv", filename, row_number),
            bus_type=_text(
                row, "bus_type", filename, row_number
            ).upper(),
            vm_pu=_number(row, "vm_pu", filename, row_number),
            va_deg=_number(row, "va_deg", filename, row_number),
            p_load_mw=_number(
                row, "p_load_mw", filename, row_number
            ),
            q_load_mvar=_number(
                row, "q_load_mvar", filename, row_number
            ),
            in_service=_boolean(
                row, "in_service", filename, row_number
            ),
        )
        network.add_bus(bus)

    for row_number, row in enumerate(generator_rows, start=2):
        filename = "generator_data.csv"

        generator = Generator(
            generator_id=_text(
                row, "generator_id", filename, row_number
            ),
            bus_id=_integer(row, "bus_id", filename, row_number),
            name=_text(row, "name", filename, row_number),
            generator_type=_text(
                row, "generator_type", filename, row_number
            ).upper(),
            vm_pu=_number(row, "vm_pu", filename, row_number),
            p_min_mw=_optional_number(
                row, "p_min_mw", filename, row_number
            ),
            p_max_mw=_optional_number(
                row, "p_max_mw", filename, row_number
            ),
            q_min_mvar=_optional_number(
                row, "q_min_mvar", filename, row_number
            ),
            q_max_mvar=_optional_number(
                row, "q_max_mvar", filename, row_number
            ),
            in_service=_boolean(
                row, "in_service", filename, row_number
            ),
        )
        network.add_generator(generator)

    for row_number, row in enumerate(transformer_rows, start=2):
        filename = "transformer_data.csv"

        transformer = Transformer(
            transformer_id=_text(
                row, "transformer_id", filename, row_number
            ),
            from_bus=_integer(
                row, "from_bus", filename, row_number
            ),
            to_bus=_integer(row, "to_bus", filename, row_number),
            rated_mva=_number(
                row, "rated_mva", filename, row_number
            ),
            hv_kv=_number(row, "hv_kv", filename, row_number),
            lv_kv=_number(row, "lv_kv", filename, row_number),
            r_pu=_number(row, "r_pu", filename, row_number),
            x_pu=_number(row, "x_pu", filename, row_number),
            tap_ratio=_number(
                row, "tap_ratio", filename, row_number
            ),
            in_service=_boolean(
                row, "in_service", filename, row_number
            ),
        )
        network.add_transformer(transformer)

    for row_number, row in enumerate(line_rows, start=2):
        filename = "line_data.csv"

        line = Line(
            line_id=_text(row, "line_id", filename, row_number),
            from_bus=_integer(
                row, "from_bus", filename, row_number
            ),
            to_bus=_integer(row, "to_bus", filename, row_number),
            length_km=_number(
                row, "length_km", filename, row_number
            ),
            r_ohm_per_km=_number(
                row, "r_ohm_per_km", filename, row_number
            ),
            x_ohm_per_km=_number(
                row, "x_ohm_per_km", filename, row_number
            ),
            in_service=_boolean(
                row, "in_service", filename, row_number
            ),
        )
        network.add_line(line)

    return network
