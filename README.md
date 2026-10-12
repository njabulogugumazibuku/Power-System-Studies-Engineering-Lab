<<<<<<< HEAD
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
=======
# Power System Studies Engineering Lab

## Purpose

The Power System Studies Engineering Lab is a long-term engineering learning and development project focused on practical power-system studies implemented using Python.

The project uses a fictional but technically coherent electrical network as a laboratory environment for developing:

- Power-system analysis knowledge
- Numerical methods
- Python programming skills
- Engineering modelling skills
- Automated verification and testing
- Engineering interpretation and documentation

The project is intended for educational and portfolio development purposes.

It does not represent an actual utility network and must not be treated as a substitute for a utility-grade engineering study.

---

## Engineering Philosophy

The project follows this workflow:

1. Learn the engineering concept.
2. Understand the physical principles and model.
3. Work through a numerical example.
4. Implement the method in Python.
5. Test the implementation.
6. Interpret the results.
7. Document the findings.
8. Move to the next study.

Python is used as the laboratory through which power-system engineering concepts are explored.

The objective is not simply to produce numerical answers, but to understand:

1. What engineering problem is being solved.
2. Why the study is performed.
3. What physical principles govern the problem.
4. What mathematical model represents the system.
5. How the numerical method works.
6. How the method is implemented.
7. How the implementation is verified.
8. What the results mean physically.
9. What engineering decisions the results could support.

---

## Initial Study Scope

The first milestone is:

**Milestone 01 — Power-System Model & Per-Unit System**

The initial milestone covers:

- System topology
- Bus modelling
- Generator/grid representation
- Load modelling
- Transformer modelling
- Line modelling
- System base selection
- Voltage bases
- Base impedance
- Base current
- Per-unit conversion
- Engineering assumptions
- Manual verification
- Python implementation
- Automated tests

The next major study will be:

**Milestone 02 — Y-Bus Formation**

---

## Initial System

The initial fictional network consists of:

- One external grid source
- One 132/33 kV transformer
- One 33 kV main bus
- Three 33 kV feeders
- Three load buses

Conceptually:

```text
    GRID
      |
    BUS 1
    132 kV
      |
    T1
    132/33 kV
      |
    BUS 2
    33 kV
    /  |  \
   /   |   \
   L1   L2   L3
  |    |    |
  B3   B4   B5
  |    |    |
  L1   L2   L3
```

---

## System Base

The initial common system base is:

- Apparent power base: 100 MVA
- HV voltage base: 132 kV
- MV voltage base: 33 kV
- Frequency: 50 Hz

The 33 kV voltage base is derived from the 132/33 kV transformer ratio.

---

## Important Modelling Conventions

### Voltage

Bus voltage is represented using line-to-line RMS voltage for the three-phase system.

### Power

Three-phase apparent power is calculated as:

$$
S = \sqrt{3}\,V_{LL}I_L
$$

### Per-Unit

The primary per-unit relationships used in the project are:

$$
V_{pu} = \frac{V_{actual}}{V_{base}},\qquad
I_{pu} = \frac{I_{actual}}{I_{base}},\qquad
Z_{pu} = \frac{Z_{actual}}{Z_{base}},\qquad
S_{pu} = \frac{S_{actual}}{S_{base}}
$$

### Sign Convention

Loads are treated as consuming positive active and reactive power.

Within the engineering input data, this means:

$$
P_{load} > 0,\qquad Q_{load} > 0
$$

The power-flow formulation will later translate these quantities into the sign convention required by the numerical solver.

---

## Data Classification

Engineering information in this repository is classified conceptually as:

### Physical Principle

A fundamental electrical relationship or physical law.

### Textbook Model

A mathematical simplification used for analysis.

### Project Assumption

A value or modelling decision deliberately selected for this educational network.

### Industry Practice

A convention commonly used in professional power-system studies.

### Engineering Requirement

A requirement that would need to be established from an applicable standard, grid code, utility specification, equipment specification or actual engineering study.

Project assumptions must not be represented as real utility requirements.

---

## Project Limitations

The initial model is intentionally simplified.

It does not currently represent:

- Actual utility network data
- Detailed conductor geometry
- Detailed transformer construction
- Detailed generator models
- Protection settings
- Actual protection coordination
- Detailed grounding systems
- Dynamic machine behaviour
- Detailed load models
- Harmonic behaviour
- Electromagnetic transients
- Real utility operating constraints

These may be introduced later where they support the learning objectives.

---

## Learning Approach

Each major study should connect these stages:

**Physical system → Mathematical model → Numerical method → Python implementation → Verification → Engineering interpretation**

The project should favour incremental development over large implementations.

Code should be understandable, testable and traceable to the engineering equations it implements.
>>>>>>> src
