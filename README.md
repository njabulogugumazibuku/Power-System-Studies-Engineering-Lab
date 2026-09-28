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

The project follows the workflow:

LEARN
→ UNDERSTAND
→ WORK A NUMERICAL EXAMPLE
→ IMPLEMENT IN PYTHON
→ TEST
→ INTERPRET RESULTS
→ DOCUMENT
→ MOVE TO THE NEXT STUDY

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

Three-phase apparent power is represented using:

S = √3 × V × I

### Per-Unit

The primary per-unit relationships used in the project are:

V_pu = V_actual / V_base

I_pu = I_actual / I_base

Z_pu = Z_actual / Z_base

S_pu = S_actual / S_base

### Sign Convention

Loads are treated as consuming positive active and reactive power.

Therefore:

P_load > 0

Q_load > 0

within the engineering input data.

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

Each major study should connect:

Physical system
→ Mathematical model
→ Numerical method
→ Python implementation
→ Verification
→ Engineering interpretation

The project should favour incremental development over large implementations.

Code should be understandable, testable and traceable to the engineering equations it implements.