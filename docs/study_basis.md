# Study Basis — Power System Studies Engineering Lab

**Document ID:** PSL-SB-001  
**Version:** 0.2  
**Status:** Draft — corrected topology; parameter verification outstanding  
**Study type:** Educational steady-state power-system modelling  
**Frequency:** 50 Hz  
**System MVA base:** 100 MVA  
**Voltage bases:** 132 kV at Bus 1; 33 kV at Buses 2–5

---

## 1. Purpose

This document defines the network topology, electrical bases, modelling conventions, assumptions, limitations, and validation criteria for reproducible studies in the Power System Studies Engineering Lab.

The learning sequence is: define and validate the network; establish per-unit quantities; calculate branch impedances and admittances; form and verify the bus-admittance matrix (Y-bus); extend the model to power-flow studies; test, interpret, and document results.

This is a synthetic educational model. It is not suitable for operational network decisions, utility planning, protection settings, or equipment procurement.

## 2. Study scope

The initial study covers:
- Network topology and connectivity validation.
- Three-phase per-unit base calculations.
- Conversion of line impedances from ohms to per unit.
- Conversion of equipment impedance to the common system base.
- Series branch admittance calculations.
- Formation and verification of the Y-bus.
- Preparation of a consistent model for later power-flow analysis.

The initial Y-bus model excludes line charging, transformer magnetising branches and core losses, phase-shifting and off-nominal tap effects, unbalanced phase-domain modelling, dynamic/transient studies, protection studies, and short-circuit calculations unless explicitly added in a later revision.

## 3. Agreed network topology

### 3.1 Topology description

The target network has **five buses**. An external grid supplies Bus 1 at 132 kV. Transformer T1 connects Bus 1 to Bus 2, the common 33 kV bus. Three separate feeder branches connect Bus 2 to load buses Bus 3, Bus 4, and Bus 5.

The loads are connected at the ends of their respective feeders. The feeders branch in parallel from the common bus; they are **not connected in series with one another**.

```text
External Grid
     |
   Bus 1 (132 kV, slack/reference)
     |
 Transformer T1 (132/33 kV)
     |
   Bus 2 (33 kV, common bus)
     |
     +-------------+-------------+
     |             |             |
   Feeder L1     Feeder L2     Feeder L3
     |             |             |
   Bus 3         Bus 4         Bus 5
     |             |             |
   Load 1        Load 2        Load 3
```

### 3.2 Branch register

| Branch | From bus | To bus | Role | Parameter status |
|---|---|---|---|---|
| T1 | Bus 1 | Bus 2 | 132/33 kV transformer | Rating and reactance base specified; other details to confirm |
| L1 | Bus 2 | Bus 3 | Feeder to Load 1 | Length and impedance to confirm |
| L2 | Bus 2 | Bus 4 | Feeder to Load 2 | Length and impedance to confirm |
| L3 | Bus 2 | Bus 5 | Feeder to Load 3 | Length and impedance to confirm |

The SLD defines topology. Numeric values displayed only in generated illustrative artwork are not verified input data until separately confirmed and entered in the network data register.

### 3.3 Bus and load register

| Bus | Nominal voltage | Role | Load |
|---|---:|---|---|
| Bus 1 | 132 kV | External-grid/slack bus | None |
| Bus 2 | 33 kV | Common bus, transformer LV side | No load currently assigned |
| Bus 3 | 33 kV | Load bus | Load 1 |
| Bus 4 | 33 kV | Load bus | Load 2 |
| Bus 5 | 33 kV | Load bus | Load 3 |

The MW and Mvar demand for each load remains to be confirmed. Do not treat values that appear only in an illustrative generated diagram as authoritative.

## 4. Electrical bases and conventions

### 4.1 Base values

| Quantity | Study basis |
|---|---:|
| Three-phase apparent power base, $S_\text{base}$ | 100 MVA |
| Bus 1 voltage base, line-to-line RMS | 132 kV |
| Buses 2–5 voltage base, line-to-line RMS | 33 kV |
| Frequency | 50 Hz |
| Phase convention | Balanced three-phase system |
| Power convention | Total three-phase MW, Mvar, and MVA |
| Impedance convention | $Z=R+jX$ |
| Admittance convention | $Y=G+jB=1/Z$ |

The voltage bases are consistent with the nominal 132/33 kV transformer ratio.

### 4.2 Base impedance

For a balanced three-phase system using line-to-line kV and three-phase MVA:

$$
Z_\text{base}=\frac{V_\text{base}^{2}}{S_\text{base}}
$$

At 132 kV:

$$
Z_{\text{base},132}=\frac{132^2}{100}=174.24\ \Omega
$$

At 33 kV:

$$
Z_{\text{base},33}=\frac{33^2}{100}=10.89\ \Omega
$$

Base admittance is $Y_\text{base}=1/Z_\text{base}$. At 33 kV, $Y_{\text{base},33}\approx0.091827\ \text{S}$.

### 4.3 Per-unit quantities

$$
Z_\text{pu}=\frac{Z_\text{actual}}{Z_\text{base}}
$$

$$
Y_\text{pu}=\frac{Y_\text{actual}}{Y_\text{base}}
=Y_\text{actual}Z_\text{base}
$$

All branch impedances used together in the Y-bus must be expressed on the common 100 MVA system base and the appropriate voltage base.

### 4.4 Transformer impedance base conversion

Transformer T1 is specified as 50 MVA, 132/33 kV, with reactance $X=0.2$ pu on its 50 MVA equipment base. The intended system base is 100 MVA.

$$
Z_{\text{pu,new}} =
Z_{\text{pu,old}}
\left(\frac{S_{\text{base,new}}}{S_{\text{base,old}}}\right)
\left(\frac{V_{\text{base,old}}}{V_{\text{base,new}}}\right)^2
$$

Assuming the voltage bases match the transformer rated voltages, the voltage factor is 1:

$$
X_{\text{pu,system}}=0.2\left(\frac{100}{50}\right)=0.4\ \text{pu}
$$

The initial model assumes $R=0$ pu, so $Z_{T1}=j0.4$ pu and $y_{T1}=1/(j0.4)=-j2.5$ pu. Zero resistance is a simplifying assumption, not a claim that a real transformer has no losses. Record the original equipment base and ensure conversion occurs exactly once.

## 5. Feeder and load modelling

### 5.1 Feeder impedance

Each feeder is initially represented by a series impedance:

$$
Z_\text{line}=L(r+jx)
$$

where $L$ is length in kilometres, $r$ is resistance in ohms per kilometre, and $x$ is reactance in ohms per kilometre.

The lengths and per-kilometre impedance parameters for L1, L2, and L3 have not yet been verified. Do not approve final feeder per-unit impedances or admittances until those values are confirmed. Line charging and shunt admittances are excluded from the initial model.

### 5.2 Loads

Load 1 connects at Bus 3, Load 2 at Bus 4, and Load 3 at Bus 5. Loads are represented as positive active and reactive demand in MW and Mvar. For later power-flow analysis, the initial assumption is constant-PQ load unless the model scope changes.

Constant-PQ loads are not normally inserted as fixed series branch admittances in the Y-bus; their power terms enter the power-flow equations. Any explicit shunt elements must be represented separately. The numerical MW and Mvar values of all three loads remain to be confirmed.

## 6. External grid and bus conventions

Bus 1 is the intended slack/reference bus. It establishes the voltage-angle reference and balances the active and reactive power mismatch in a conventional power-flow formulation.

The slack-bus voltage magnitude and angle are not yet formally fixed. A common educational starting point is $V=1.0$ pu and $\theta=0^\circ$, but these values must be explicitly set in the model before a power-flow calculation.

Bus IDs and branch endpoints in the CSV files must match the IDs used by the Python model. Component IDs must be unique, and every branch endpoint must reference an existing bus.

## 7. Y-bus modelling rules

For the initial reciprocal series-branch model:
- Each off-diagonal entry $Y_{ij}$ is the negative of the total series admittance directly connecting buses $i$ and $j$.
- Each diagonal entry $Y_{ii}$ is the sum of admittances of branches incident on bus $i$, plus any explicitly modelled shunts.
- If no direct branch connects two buses, the corresponding off-diagonal entry is zero.
- With reciprocal branches and no phase-shifting transformer effects, the Y-bus should be symmetric: $Y_{ij}=Y_{ji}$.
- The bus ordering used for the matrix must be explicit and recorded.

The target model has five buses, so the expected Y-bus dimension is $5\times5$.

With the proposed topology, there are no direct branches between Bus 3, Bus 4, and Bus 5. Thus $Y_{34}=Y_{35}=Y_{45}=0$, and the symmetric counterpart entries are also zero, unless additional branches are added. Diagonal terms include only branches and shunts actually connected to each bus. Constant-PQ loads are handled in the power-flow equations rather than automatically added as series admittances.

## 8. Data provenance and units

All parameters are synthetic educational data unless a later revision explicitly identifies another source.

Each component record should include:
- Unique component ID and connected bus IDs.
- Parameter value and unit.
- Original base for per-unit values.
- Source/provenance (confirmed input, calculated value, illustrative diagram, or assumption).
- In-service status and verification status.

Do not mix ohms with per-unit values or line-to-line voltage with phase voltage without an explicit conversion. Do not infer an impedance base solely from an equipment MVA rating.

## 9. Validation and acceptance checks

### 9.1 Input and topology checks

- Exactly five unique buses are represented.
- Bus 1 is the intended slack/reference bus.
- Bus 2 is the common 33 kV bus on the transformer low-voltage side.
- T1 connects Bus 1 to Bus 2.
- L1 connects Bus 2 to Bus 3; L2 connects Bus 2 to Bus 4; L3 connects Bus 2 to Bus 5.
- Loads connect at Buses 3, 4, and 5 respectively.
- No direct branch exists between load buses unless the model is intentionally revised.
- All endpoints reference existing buses and all component IDs are unique.
- Voltage bases are positive and consistent with the transformer ratio.
- Required numeric values are finite and units are explicit.
- With all branches in service, all five buses are reachable from the slack bus.

### 9.2 Electrical calculation checks

- Base impedances use line-to-line kV and three-phase MVA.
- Transformer reactance converts from 0.2 pu on 50 MVA to 0.4 pu on 100 MVA, assuming consistent rated voltage bases.
- Each feeder impedance uses its verified length and per-kilometre parameters.
- Branch admittances are calculated as complex reciprocals of branch impedances.
- Off-diagonal entries have the negative-admittance sign.
- Diagonal entries equal the sum of connected branch admittances plus included shunts.
- The Y-bus is $5\times5$.
- The initial Y-bus is symmetric for this reciprocal, no-phase-shift model.
- Numerical tests use suitable floating-point tolerances.

### 9.3 Independent verification

At least one per-unit conversion, one branch admittance, and selected Y-bus entries should be checked independently by hand or using a separate calculation. Tests must validate engineering meaning as well as successful code execution.

## 10. Open decisions and assumptions register

| ID | Item | Current status | Required action |
|---|---|---|---|
| SB-01 | Five-bus topology | Agreed target | Update SLD and model to common bus with three parallel feeders |
| SB-02 | Feeder lengths and impedances | Unverified | Confirm L1, L2, and L3 values; do not treat generated-image labels as authoritative |
| SB-03 | Load MW and Mvar values | Unverified | Confirm demand at Buses 3, 4, and 5 |
| SB-04 | Transformer reactance | 0.2 pu on 50 MVA equipment base; 0.4 pu on 100 MVA system base | Preserve source base and test conversion |
| SB-05 | Transformer resistance | Assumed zero initially | Retain as stated simplification or choose a documented synthetic value |
| SB-06 | Transformer tap and phase shift | Nominal tap and no phase shift intended | Confirm CSV/model convention |
| SB-07 | Line shunt capacitance | Excluded | Add only if required and supported by parameters |
| SB-08 | Slack voltage magnitude and angle | Not fixed | Set explicitly before power-flow analysis |
| SB-09 | External-grid data model | Slack source intended at Bus 1 | Confirm model and CSV schema support reference-bus behaviour |
| SB-10 | Existing CSV and tests | Earlier fixtures describe a smaller network | Update fixtures, validation tests, and documentation to the five-bus target |
| SB-11 | Standards/references | Not specified | Add exact titles and editions if a formal standards basis is adopted |

## 11. Reproducibility and change control

- Keep this document under version control with the SLD, data files, code, and tests.
- Record changes to topology, bases, parameters, and assumptions in the engineering decision/change log.
- Update the SLD, CSV files, data dictionary, and tests together when the network changes.
- Keep the original equipment base and converted system-base value distinguishable.
- Do not silently change synthetic parameters to make tests pass; update the rationale and expected result.
- Treat values appearing only in generated illustrative artwork as provisional until confirmed.

## 12. Readiness criteria for Y-bus implementation

The network is ready for Y-bus implementation when:
1. The five-bus SLD and CSV data agree.
2. All five buses, one transformer, three feeders, one external-grid source, and three loads are represented in the Python model.
3. Feeder lengths, impedances, and load demands are confirmed and documented.
4. Transformer impedance base conversion is implemented and tested.
5. Voltage bases, units, connectivity, and in-service status pass validation.
6. Independent calculations are available for the transformer and each feeder.
7. Tests cover matrix dimension, branch admittances, off-diagonal signs, diagonal sums, zero entries between unconnected load buses, and symmetry.

**Current readiness status:** Not yet ready. The five-bus topology is defined, but feeder parameters and load demands must be confirmed and the existing CSV data, model, and tests updated before Y-bus results can be treated as results for this study.

---

## Revision history

| Version | Status | Description |
|---|---|---|
| 0.1 | Superseded draft | Described a four-bus series-chain topology |
| 0.2 | Draft | Corrects topology to five buses with three parallel feeders from a common 33 kV bus; flags feeder and load data for verification |
