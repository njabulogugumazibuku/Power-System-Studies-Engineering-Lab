# 01 — System Model

## Purpose

This directory contains the source-of-truth definition of the fictional power network used throughout the Power System Studies Engineering Lab.

The data in this directory defines the initial network topology, equipment and operating conditions.

All data is synthetic and intended for educational and portfolio purposes.

---

## Network Topology

The initial network consists of:

- Bus 1 — 132 kV grid/slack bus
- Bus 2 — 33 kV main bus
- Bus 3 — 33 kV load bus
- Bus 4 — 33 kV load bus
- Bus 5 — 33 kV load bus
- Transformer T1 — 132/33 kV, 50 MVA
- Line L1 — Bus 2 to Bus 3
- Line L2 — Bus 2 to Bus 4
- Line L3 — Bus 2 to Bus 5

---

## System Bases

| Quantity | Value |
|---|---:|
| System MVA base | 100 MVA |
| HV voltage base | 132 kV |
| MV voltage base | 33 kV |
| Frequency | 50 Hz |

Derived quantities:

### 132 kV side

Z_base = V_base² / S_base

Z_base = 132² / 100

Z_base = 174.24 Ω

I_base = S_base / (√3 × V_base)

I_base ≈ 437.4 A

### 33 kV side

Z_base = 33² / 100

Z_base = 10.89 Ω

I_base = 100 MVA / (√3 × 33 kV)

I_base ≈ 1749.5 A

---

## Transformer

Transformer T1:

- Rating: 50 MVA
- HV: 132 kV
- LV: 33 kV
- Leakage impedance: 10%
- Transformer resistance: neglected initially
- Nominal tap: 1.0 pu

The transformer impedance is initially represented as purely reactive.

On the transformer base:

Z_T = j0.10 pu

Converted to the 100 MVA system base:

Z_T,new = Z_T,old × (S_base,new / S_base,old)

Z_T,new = j0.10 × (100 / 50)

Z_T,new = j0.20 pu

---

## Loads

### Load 1 — Bus 3

- Active power: 10 MW
- Power factor: 0.95 lagging
- Reactive power: approximately 3.29 MVAr

### Load 2 — Bus 4

- Active power: 12 MW
- Power factor: 0.92 lagging
- Reactive power: approximately 5.10 MVAr

### Load 3 — Bus 5

- Active power: 8 MW
- Power factor: 0.90 lagging
- Reactive power: approximately 3.88 MVAr

Total:

- Active power: 30 MW
- Reactive power: approximately 12.27 MVAr
- Apparent power: approximately 32.41 MVA

---

## Bus Types

| Bus | Type | Description |
|---|---|---|
| 1 | SLACK | External grid reference |
| 2 | PQ | 33 kV main bus |
| 3 | PQ | Load bus |
| 4 | PQ | Load bus |
| 5 | PQ | Load bus |

Bus 1 is initially specified as:

V = 1.0 pu

δ = 0°

---

## Modelling Assumptions

1. The network is balanced and represented using a positive-sequence, three-phase steady-state model.
2. The external grid is represented by a slack/reference bus for the initial power-flow study.
3. Transformer resistance is neglected initially.
4. Transformer tap position is fixed at nominal.
5. Lines are represented by lumped series impedance.
6. Line shunt capacitance is neglected initially.
7. Loads are represented as constant P-Q loads.
8. All network data is synthetic.
9. No equipment limits are enforced in the first system-model milestone.
10. No generator other than the external grid is represented initially.

---

## Engineering Purpose

This model will form the basis for:

- Per-unit calculations
- Y-bus formation
- Power-flow studies
- Voltage-profile analysis
- Loss calculations
- Contingency studies
- Short-circuit studies
- Protection-related analysis
- Future network expansion