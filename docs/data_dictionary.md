# Power System Studies Engineering Lab — Data Dictionary

**Document ID:** PSL-DD-001  
**Version:** 0.1  
**Status:** Draft  
**Applies to:** `01_system_model/` CSV data files

---

## 1. Purpose

This document defines the meaning, units, expected data types, and validation requirements of the CSV fields used to represent the power system.

It provides a common reference for:

- Engineers interpreting the network model.
- Developers implementing the CSV loader and network classes.
- Tests validating the integrity of the input data.
- Future studies using the network model for per-unit calculations, admittance construction, and power-flow analysis.

The existing CSV files remain the authoritative source for the project's current input values. This document describes their intended interpretation; it does not replace or modify those values.

## 2. System modelling conventions

| Convention | Value |
|---|---|
| System base apparent power | 100 MVA |
| System frequency | 50 Hz |
| Bus 1 voltage base | 132 kV |
| Bus 2 voltage base | 33 kV |
| Bus 3 voltage base | 33 kV |
| Bus 4 voltage base | 33 kV |
| Bus 5 voltage base | 33 kV |
| Network representation | Balanced, steady-state, single-phase-equivalent calculations with three-phase system bases |

Voltage bases are line-to-line RMS values. The 100 MVA base is the three-phase apparent-power base.

The voltage bases and equipment data must be mutually consistent. In particular, transformer voltage ratings and the selected bus voltage bases must agree with the intended transformer connection and nominal ratio.

## 3. Network topology

The network consists of five buses.

- **Bus 1:** External grid connection at 132 kV.
- **Bus 2:** Common 33 kV bus supplied through transformer T1.
- **Bus 3:** Load bus supplied by feeder L1.
- **Bus 4:** Load bus supplied by feeder L2.
- **Bus 5:** Load bus supplied by feeder L3.

Transformer T1 connects Bus 1 to Bus 2. Feeders L1, L2, and L3 connect Bus 2 to Buses 3, 4, and 5 respectively.

The three feeder branches are connected in parallel at the common Bus 2. The load buses are not connected in series.

This topology determines the network connectivity and the structure of the five-by-five bus-admittance matrix.

## 4. File: `bus_data.csv`

**Purpose:** Defines the network buses, their voltage bases, bus classifications, operating-state fields, and any load demand assigned directly to a bus.

| Field | Intended meaning | Unit / type |
|---|---|---|
| `bus_id` | Unique identifier for the bus | Integer or identifier |
| `name` | Human-readable bus name | Text |
| `base_kv` | Nominal line-to-line voltage base | kV |
| `bus_type` | Bus classification used by the model | Text or enumeration |
| `vm_pu` | Voltage magnitude in per unit | p.u. |
| `va_deg` | Voltage phase angle | Degrees |
| `p_load_mw` | Active load assigned to the bus | MW |
| `q_load_mvar` | Reactive load assigned to the bus | MVAr |
| `in_service` | Whether the bus is in service | Boolean |

### Interpretation

**Bus voltage base**

`base_kv` is the voltage base associated with the bus. It is used when converting quantities between physical units and per-unit quantities.

For the current system, Bus 1 uses a 132 kV base, while Buses 2–5 use 33 kV bases.

**Bus type**

The model must define the accepted bus-type values and their implications. Typical power-flow classifications include:

- Slack or reference bus.
- PV bus, where active power and voltage magnitude are specified.
- PQ bus, where active and reactive power are specified.

The precise supported values must match the Python implementation. A value should not be assumed valid merely because it is a conventional power-system label.

**Voltage magnitude and angle**

`vm_pu` and `va_deg` represent voltage magnitude and angle. Their interpretation depends on the study being performed. In a power-flow study, they may be specified inputs for particular bus types or calculated outputs for other buses.

**Load demand**

Positive `p_load_mw` and `q_load_mvar` values conventionally represent active and reactive consumption. The implementation must consistently apply this sign convention.

Load fields assigned to a bus must not be counted again as separate loads unless the model explicitly represents them as separate network elements.

## 5. File: `generator_data.csv`

**Purpose:** Defines generators and other supported voltage-source representations connected to network buses.

| Field | Intended meaning | Unit / type |
|---|---|---|
| `generator_id` | Unique identifier for the generator | Text or identifier |
| `bus_id` | Bus to which the generator is connected | Bus identifier |
| `name` | Human-readable generator name | Text |
| `generator_type` | Generator or source classification | Text or enumeration |
| `vm_pu` | Voltage-magnitude setpoint, where applicable | p.u. |
| `p_min_mw` | Minimum active-power limit | MW |
| `p_max_mw` | Maximum active-power limit | MW |
| `q_min_mvar` | Minimum reactive-power limit | MVAr |
| `q_max_mvar` | Maximum reactive-power limit | MVAr |
| `in_service` | Whether the generator is in service | Boolean |

### Interpretation

Generator data describe source capabilities and operating constraints. They do not, by themselves, establish the complete power-flow control behaviour of the connected bus.

The model must distinguish between a generator's physical limits, its specified operating values, and quantities calculated by a study.

Where the external grid is represented as a generator or equivalent source, its treatment as the reference source must be consistent with the bus classification and power-flow implementation.

The accepted `generator_type` values and the treatment of the external grid must be documented alongside the corresponding model implementation.

## 6. File: `transformer_data.csv`

**Purpose:** Defines transformers connecting buses at different nominal voltage levels.

| Field | Intended meaning | Unit / type |
|---|---|---|
| `transformer_id` | Unique transformer identifier | Text or identifier |
| `from_bus` | Identifier of the first connected bus | Bus identifier |
| `to_bus` | Identifier of the second connected bus | Bus identifier |
| `rated_mva` | Transformer rated apparent power | MVA |
| `hv_kv` | Nominal high-voltage winding rating | kV |
| `lv_kv` | Nominal low-voltage winding rating | kV |
| `r_pu` | Transformer resistance in per unit | p.u. |
| `x_pu` | Transformer reactance in per unit | p.u. |
| `tap_ratio` | Model-defined transformer tap ratio | p.u. or ratio |
| `in_service` | Whether the transformer is in service | Boolean |

### Interpretation

Transformer T1 connects the 132 kV side at Bus 1 to the 33 kV side at Bus 2.

The equipment rating and voltage ratings describe the transformer's nominal characteristics. The per-unit resistance and reactance describe its electrical impedance on a specified base.

**Per-unit base requirement**

A per-unit impedance is meaningful only when its base is known. The equipment MVA rating does not automatically establish the base on which `r_pu` and `x_pu` were entered.

The model documentation must therefore establish whether these values are stored on:

1. The transformer's own rated MVA and voltage base; or
2. The project's system MVA and corresponding bus voltage bases.

If conversion is required, the bases must be identified explicitly. For compatible voltage bases:

\[
Z_{\text{pu,new}} =
Z_{\text{pu,old}}
\frac{S_{\text{base,new}}}{S_{\text{base,old}}}
\]

More generally, the voltage-base ratio must also be included.

For the educational system, the agreed example is a transformer reactance of 0.2 p.u. on a 50 MVA equipment base. On a 100 MVA system base, with consistent voltage bases, the reactance becomes 0.4 p.u.

This example describes the conversion method; it does not establish that the CSV value is stored on that equipment base. That must be confirmed from the actual data convention.

**Tap ratio**

The definition of `tap_ratio` must specify the direction of the ratio, its nominal value, and whether the implementation supports off-nominal tap effects. A stored tap ratio must not be assumed to affect calculations if the model does not implement it.

## 7. File: `line_data.csv`

**Purpose:** Defines transmission or distribution line branches between buses.

| Field | Intended meaning | Unit / type |
|---|---|---|
| `line_id` | Unique line identifier | Text or identifier |
| `from_bus` | Identifier of the sending-end bus | Bus identifier |
| `to_bus` | Identifier of the receiving-end bus | Bus identifier |
| `length_km` | Line length | km |
| `r_ohm_per_km` | Series resistance per unit length | Ω/km |
| `x_ohm_per_km` | Series reactance per unit length | Ω/km |
| `in_service` | Whether the line is in service | Boolean |

### Interpretation

For a uniform line represented by a series impedance, the total series impedance is calculated from the line length and the per-kilometre impedance parameters:

\[
Z_{\text{line}} =
L(r+jx)
\]

where:

- \(L\) is the line length in kilometres.
- \(r\) is the resistance per kilometre.
- \(x\) is the reactance per kilometre.
- \(j=\sqrt{-1}\).

Therefore,

\[
R_{\text{line}}=Lr
\]

\[
X_{\text{line}}=Lx
\]

and

\[
Z_{\text{line}}=R_{\text{line}}+jX_{\text{line}}
\]

The resulting impedance is expressed in ohms.

The line model must specify whether shunt capacitance, charging susceptance, and other distributed or lumped line effects are included. The initial series-impedance model should not imply that these effects have been implemented.

## 8. Data validation requirements

The CSV loader and network validation tests should progressively enforce the following requirements.

### 8.1 General requirements

- Required columns are present.
- Identifiers are unique within the appropriate element type.
- Referenced buses exist.
- Numeric fields contain valid numeric values.
- Boolean fields are interpreted consistently.
- Physical quantities use the units defined in this document.
- Invalid or missing data produce clear, actionable validation messages.

### 8.2 Bus requirements

- Bus identifiers are unique.
- Nominal voltage bases are positive.
- Bus classifications belong to the supported set.
- Load and voltage fields satisfy the model's defined constraints.
- The reference bus requirement is satisfied for studies that require a slack bus.

### 8.3 Generator requirements

- Generator identifiers are unique.
- Each generator references an existing bus.
- Minimum active power does not exceed maximum active power.
- Minimum reactive power does not exceed maximum reactive power.
- Generator-type values are supported by the model.

### 8.4 Transformer requirements

- Transformer identifiers are unique.
- Both connected buses exist.
- Connected buses are different.
- Rated MVA and nominal voltage ratings are positive.
- The high- and low-voltage ratings are consistent with the connected bus voltage levels.
- Per-unit impedance bases are known before conversion or calculation.
- Tap-ratio conventions are defined if taps are modelled.

### 8.5 Line requirements

- Line identifiers are unique.
- Both connected buses exist.
- Connected buses are different.
- Line length is positive unless the model explicitly supports zero-length branches.
- Resistance and reactance values use the specified units.
- Branch connectivity is consistent with the intended network topology.

### 8.6 Network-level requirements

- All branch references resolve to valid buses.
- The intended five-bus network is represented.
- Bus 1 is the external-grid reference bus under the agreed baseline.
- Transformer T1 connects Bus 1 and Bus 2.
- Feeder L1 connects Bus 2 and Bus 3.
- Feeder L2 connects Bus 2 and Bus 4.
- Feeder L3 connects Bus 2 and Bus 5.
- Each in-service bus is reachable from the reference bus for a connected-network study.

Validation rules should distinguish malformed input data from legitimate but unsupported modelling features.

## 9. Relationship to other project documents

This document should be used together with:

- `study_basis.md` — defines the study scope, system bases, topology and assumptions.
- `worked_examples.md` — demonstrates calculations using explicitly identified inputs.
- `verification_checklist.md` — records the checks required before accepting model results.
- `engineering_decisions.md` — records decisions about conventions, simplifications and future extensions.

The Python implementation remains responsible for enforcing supported input formats and performing the calculations defined by the study scope.

## 10. Open items

The following conventions must be confirmed against the implementation and actual data before the model is treated as fully specified:

1. The exact set of accepted bus and generator types.
2. The per-unit bases used for transformer resistance and reactance in the CSV data.
3. The precise tap-ratio convention and whether taps affect calculations.
4. Whether line shunt effects are excluded or represented elsewhere.
5. The handling of blank values, defaults, and invalid Boolean representations.
6. Whether load data are represented exclusively through bus fields or through additional model elements.
7. The precise validation rules applied when an element is out of service.

These items should be resolved through inspection of the existing loader, model classes, tests and CSV values, rather than by changing input data to match an undocumented assumption.

---

**Document maintenance rule:** When the model's supported fields, units, conventions or validation rules change, update this document and the associated tests together.