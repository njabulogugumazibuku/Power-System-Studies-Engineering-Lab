"""Load and summarise the fictional engineering network."""

from power_system.io import load_network


def main() -> None:
    network = load_network(
        data_dir="",
        base_power_mva=100.0,
        frequency_hz=50.0,
    )

    print("POWER SYSTEM MODEL SUMMARY")
    print("=" * 32)

    print(f"System base: {network.base_power_mva:.1f} MVA")
    print(f"Frequency: {network.frequency_hz:.1f} Hz")

    print(f"\nBuses: {len(network.buses)}")
    for bus in network.buses.values():
        print(
            f"  Bus {bus.bus_id}: {bus.name}, "
            f"{bus.base_kv:.1f} kV, {bus.bus_type}"
        )

    print(f"\nGenerators: {len(network.generators)}")
    for generator in network.generators.values():
        print(
            f"  {generator.generator_id}: "
            f"{generator.name}, Bus {generator.bus_id}"
        )

    print(f"\nTransformers: {len(network.transformers)}")
    for transformer in network.transformers.values():
        print(
            f"  {transformer.transformer_id}: "
            f"Bus {transformer.from_bus} -> Bus {transformer.to_bus}, "
            f"{transformer.rated_mva:.1f} MVA"
        )

    print(f"\nLines: {len(network.lines)}")
    for line in network.lines.values():
        print(
            f"  {line.line_id}: "
            f"Bus {line.from_bus} -> Bus {line.to_bus}, "
            f"Z = {line.impedance_ohm:.3f} ohm"
        )


if __name__ == "__main__":
    main()