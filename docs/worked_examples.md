# Power System Studies Engineering Lab — Worked Examples

**Document ID:** PSL-WE-001  
**Version:** 0.1  
**Status:** Draft  
**Applies to:** Five-bus educational network  
**Related documents:** `study_basis.md`, `data_dictionary.md`, `verification_checklist.md`, `engineering_decisions.md`

---

## 1. Purpose and method

This document records repeatable engineering calculations used to understand and verify the power-system model.

Each worked example follows the same sequence:

1. State the objective.
2. Identify the inputs and their provenance.
3. State the assumptions and applicable equations.
4. Show the calculation.
5. Interpret the result physically.
6. Identify checks that can later be automated in Python.

The examples distinguish between **project base values**, **symbolic calculations requiring actual CSV inputs**, and **illustrative numerical values**. Illustrative values are for teaching only and must not be treated as the actual network data.

The existing CSV files remain the source of the network's input values. This document does not require changing them.

## 2. Baseline network and conventions

The network has five buses:

- Bus 1: external grid / reference bus, 132 kV.
- Transformer T1: Bus 1 to Bus 2, 132/33 kV.
- Bus 2: common 33 kV bus.
- Feeder L1: Bus 2 to Bus 3.
- Feeder L2: Bus 2 to Bus 4.
- Feeder L3: Bus 2 to Bus 5.
- Buses 3, 4 and 5: separate load buses.

The three feeders are separate branches connected to Bus 2. The loads are not connected in series.

### Agreed system bases

| Quantity | Value |
|---|---:|
| Three-phase apparent-power base, \(S_\text{base}\) | 100 MVA |
| Bus 1 voltage base, \(V_{\text{base},1}\) | 132 kV |
| Bus 2 voltage base, \(V_{\text{base},2}\) | 33 kV |
| Bus 3 voltage base, \(V_{\text{base},3}\) | 33 kV |
| Bus 4 voltage base, \(V_{\text{base},4}\) | 33 kV |
| Bus 5 voltage base, \(V_{\text{base},5}\) | 33 kV |
| System frequency | 50 Hz |

For the three-phase per-unit system, voltage bases are line-to-line RMS values and the apparent-power base is the three-phase total.

---

## Example 1 — Calculate base impedance

### Objective

Calculate the impedance base at the 132 kV and 33 kV voltage levels.

### Formula

For a balanced three-phase system using line-to-line voltage and three-phase apparent power:

\[
Z_\text{base} = \frac{V_\text{base}^2}{S_\text{base}}
\]

When voltage is in kV and apparent power is in MVA, the result is in ohms.

### Calculation at 132 kV

Inputs:

\[
V_\text{base}=132\text{ kV}, \qquad
S_\text{base}=100\text{ MVA}
\]

Therefore:

\[
Z_{\text{base},132}=\frac{132^2}{100}
=\frac{17424}{100}
=174.24\ \Omega
\]

### Calculation at 33 kV

Inputs:

\[
V_\text{base}=33\text{ kV}, \qquad
S_\text{base}=100\text{ MVA}
\]

Therefore:

\[
Z_{\text{base},33}=\frac{33^2}{100}
=\frac{1089}{100}
=10.89\ \Omega
\]

### Results

| Voltage level | Impedance base |
|---|---:|
| 132 kV | 174.24 Ω |
| 33 kV | 10.89 Ω |

### Interpretation

The impedance base depends on both the selected voltage base and the system apparent-power base. With the same 100 MVA base, the 132 kV impedance base is sixteen times the 33 kV impedance base because:

\[
\left(\frac{132}{33}\right)^2=16
\]

### Verification checks

- The impedance base is positive.
- The units are ohms.
- Recalculate using the formula and confirm the values above.
- Do not use the 132 kV impedance base for a 33 kV branch when converting its physical impedance to per unit.

---

## Example 2 — Calculate the admittance base

### Objective

Calculate the admittance base at 33 kV.

### Formula

Admittance is the reciprocal of impedance:

\[
Y_\text{base}=\frac{1}{Z_\text{base}}
\]

From Example 1:

\[
Z_{\text{base},33}=10.89\ \Omega
\]

Therefore:

\[
Y_{\text{base},33}=\frac{1}{10.89}
\approx 0.091827\text{ S}
\]

### Result

\[
\boxed{Y_{\text{base},33}\approx0.091827\text{ S}}
\]

### Interpretation

The admittance base is useful for converting a physical branch admittance in siemens into per unit. It is not necessary to calculate admittance in siemens first if the branch impedance is already expressed in per unit; in that case, per-unit admittance is simply the reciprocal of per-unit impedance.

### Verification checks

- \(Y_\text{base}\) has units of siemens (S).
- \(Z_\text{base}Y_\text{base}=1\), within numerical precision.

---

## Example 3 — Convert transformer impedance to the system base

### Objective

Convert a transformer reactance from an equipment base to the project's system base.

### Inputs and provenance

This is the agreed **illustrative transformer-base example**:

- Transformer rating: 50 MVA.
- Reactance: 0.2 p.u. on the 50 MVA equipment base.
- System apparent-power base: 100 MVA.
- Voltage bases are assumed consistent with the transformer's nominal ratio.

The example establishes the conversion method. The actual base used by the value stored in `transformer_data.csv` must be confirmed from the project's data convention before applying the conversion to the real model.

### Formula

The general impedance base-conversion equation is:

\[
Z_{\text{pu,new}} =
Z_{\text{pu,old}}
\left(\frac{S_{\text{base,new}}}{S_{\text{base,old}}}\right)
\left(\frac{V_{\text{base,old}}}{V_{\text{base,new}}}\right)^2
\]

Here, the voltage bases are consistent, so the voltage ratio is 1.

### Calculation

\[
X_{\text{pu,new}}
=0.2\left(\frac{100}{50}\right)
=0.2(2)
=0.4\text{ p.u.}
\]

If resistance is assumed to be zero for this simplified example:

\[
Z_{T1,\text{pu}}=j0.4\text{ p.u.}
\]

### Result

\[
\boxed{Z_{T1,\text{pu}}=j0.4\text{ p.u.}}
\]

### Interpretation

The physical transformer has not changed. Only the reference base used to express its impedance has changed.

A per-unit value must always be interpreted with its base. Applying the conversion twice would produce an incorrect result.

### Verification checks

- Confirm the old MVA base and new MVA base.
- Confirm the voltage bases refer to corresponding sides of the transformer.
- Confirm whether the CSV impedance is on the equipment base or system base.
- Ensure conversion occurs exactly once.

---

## Example 4 — Calculate a feeder's series impedance

### Objective

Calculate the total series resistance, reactance and complex impedance of a feeder from its length and per-kilometre parameters.

### General method

For a uniform line:

\[
Z_\text{line}=L(r+jx)
\]

where:

- \(L\) is line length in km.
- \(r\) is resistance in Ω/km.
- \(x\) is reactance in Ω/km.

Therefore:

\[
R_\text{line}=Lr
\]

\[
X_\text{line}=Lx
\]

\[
Z_\text{line}=R_\text{line}+jX_\text{line}
\]

### Project application

Apply these equations separately to the actual CSV rows for L1, L2 and L3:

\[
Z_{L1}=L_1(r_1+jx_1)
\]

\[
Z_{L2}=L_2(r_2+jx_2)
\]

\[
Z_{L3}=L_3(r_3+jx_3)
\]

Use each feeder's own stored length and impedance parameters. Do not assume all three feeders have the same length or impedance.

### Illustrative numerical calculation — not project data

For a teaching example only, suppose a feeder has:

- Length \(L=8\text{ km}\)
- Resistance \(r=0.40\ \Omega/\text{km}\)
- Reactance \(x=0.35\ \Omega/\text{km}\)

Then:

\[
R_\text{line}=8(0.40)=3.2\ \Omega
\]

\[
X_\text{line}=8(0.35)=2.8\ \Omega
\]

Thus:

\[
\boxed{Z_\text{line}=3.2+j2.8\ \Omega}
\]

These illustrative values must not be attributed to L1 or any other actual feeder unless confirmed by the current CSV data.

### Interpretation

Resistance represents the real component of series impedance and is associated with active-power losses. Reactance represents the imaginary component and influences the relationship between voltage, current and reactive power.

### Verification checks

- Length is in kilometres.
- Per-kilometre parameters are in Ω/km.
- Total resistance and reactance are in ohms.
- The calculated impedance is associated with the correct pair of buses.
- The branch is not inadvertently duplicated.

---

## Example 5 — Convert feeder impedance to per unit

### Objective

Convert a feeder's physical series impedance to per unit using the appropriate bus voltage base and system MVA base.

### Formula

\[
Z_\text{pu}=\frac{Z_\text{actual}}{Z_\text{base}}
\]

At the 33 kV level, the project impedance base is:

\[
Z_{\text{base},33}=10.89\ \Omega
\]

For any feeder connecting Bus 2 to one of the load buses:

\[
Z_{Lk,\text{pu}}=
\frac{R_{Lk}+jX_{Lk}}{10.89}
\]

where \(k\) is 1, 2 or 3.

### Illustrative numerical calculation — based on Example 4 only

Using the teaching example:

\[
Z_\text{line}=3.2+j2.8\ \Omega
\]

Then:

\[
Z_{\text{line,pu}}=
\frac{3.2+j2.8}{10.89}
\]

Divide the real and imaginary components by the same impedance base:

\[
Z_{\text{line,pu}}\approx
0.29385+j0.25712
\]

This result is illustrative only; it is not a confirmed per-unit impedance for any actual feeder in the CSV files.

### Interpretation

Per-unit values express electrical quantities relative to chosen bases. They make quantities at different voltage levels easier to compare and are widely used in power-system calculations.

The correct voltage base is essential. Using 174.24 Ω instead of 10.89 Ω for a 33 kV feeder would produce an incorrect result.

### Verification checks

- The branch voltage base matches its electrical location.
- The same system MVA base is used consistently.
- The physical impedance is in ohms.
- The resulting per-unit impedance is dimensionless.

---

## Example 6 — Calculate branch admittance

### Objective

Calculate the complex series admittance of a branch.

### Formula

Admittance is the reciprocal of complex impedance:

\[
Y=\frac{1}{Z}
\]

For:

\[
Z=R+jX
\]

multiply numerator and denominator by the complex conjugate:

\[
Y=\frac{1}{R+jX}
=\frac{R-jX}{R^2+X^2}
\]

Therefore:

\[
\boxed{Y=\frac{R}{R^2+X^2}
-j\frac{X}{R^2+X^2}}
\]

This shows why the real and imaginary components cannot be inverted independently.

### Illustrative numerical calculation — based on Example 4 only

For:

\[
Z=3.2+j2.8\ \Omega
\]

the squared magnitude is:

\[
R^2+X^2=3.2^2+2.8^2
=10.24+7.84=18.08
\]

Thus:

\[
Y=\frac{3.2-j2.8}{18.08}
\]

\[
\boxed{Y\approx0.17699-j0.15487\text{ S}}
\]

This is the admittance in siemens for the illustrative physical impedance.

If the impedance is already in per unit, its per-unit admittance is:

\[
Y_\text{pu}=\frac{1}{Z_\text{pu}}
\]

Using the rounded per-unit impedance from Example 5 gives approximately:

\[
Y_\text{pu}\approx1.92743-j1.68650
\]

Small differences can occur due to rounding.

### Interpretation

For a passive series branch with positive resistance and positive inductive reactance, the series admittance has a positive real component and a negative imaginary component under the \(R+jX\) impedance convention.

### Verification checks

- Confirm \(ZY=1\) within numerical tolerance.
- Confirm that admittance is in siemens when impedance is in ohms.
- Confirm that per-unit admittance is dimensionless.
- Do not mix physical and per-unit values in the same matrix.

---

## Example 7 — Assemble the five-bus Y-bus matrix

### Objective

Understand how the agreed topology determines the structure of the bus-admittance matrix.

### Governing equation

\[
\mathbf I_\text{bus}=\mathbf Y_\text{bus}\mathbf V_\text{bus}
\]

For a network with five buses, the bus-admittance matrix has five rows and five columns:

\[
\mathbf Y_\text{bus}\in\mathbb C^{5\times5}
\]

The matrix relates the vector of bus current injections to the vector of bus voltages, under the selected sign conventions and network model.

### Branch admittances

Let:

- \(y_{12}\) be the series admittance of transformer T1 between Buses 1 and 2.
- \(y_{23}\) be the series admittance of feeder L1 between Buses 2 and 3.
- \(y_{24}\) be the series admittance of feeder L2 between Buses 2 and 4.
- \(y_{25}\) be the series admittance of feeder L3 between Buses 2 and 5.

For this example, assume:

- Only these four series branches are represented.
- There are no branch shunt admittances.
- There are no additional direct connections between the load buses.
- Transformer tap effects are ignored.
- All branch admittances have already been expressed on a consistent per-unit basis.

These are simplifying assumptions for the matrix construction example, not claims that every possible transformer or line effect is implemented.

### Off-diagonal elements

An off-diagonal element is the negative of the direct branch admittance between the corresponding buses:

\[
Y_{12}=Y_{21}=-y_{12}
\]

\[
Y_{23}=Y_{32}=-y_{23}
\]

\[
Y_{24}=Y_{42}=-y_{24}
\]

\[
Y_{25}=Y_{52}=-y_{25}
\]

There are no direct branches between Buses 3 and 4, 3 and 5, or 4 and 5 in the agreed topology. Therefore:

\[
Y_{34}=Y_{43}=0
\]

\[
Y_{35}=Y_{53}=0
\]

\[
Y_{45}=Y_{54}=0
\]

### Diagonal elements

Each diagonal element is the sum of the admittances connected directly to that bus:

\[
Y_{11}=y_{12}
\]

\[
Y_{22}=y_{12}+y_{23}+y_{24}+y_{25}
\]

\[
Y_{33}=y_{23}
\]

\[
Y_{44}=y_{24}
\]

\[
Y_{55}=y_{25}
\]

This example excludes shunt elements and other device models. If those are added later, their admittances must be included according to the adopted model.

### Matrix structure

The resulting matrix is:

\[
\mathbf Y_\text{bus}=
\begin{bmatrix}
y_{12} & -y_{12} & 0 & 0 & 0\\
-y_{12} & y_{12}+y_{23}+y_{24}+y_{25} & -y_{23} & -y_{24} & -y_{25}\\
0 & -y_{23} & y_{23} & 0 & 0\\
0 & -y_{24} & 0 & y_{24} & 0\\
0 & -y_{25} & 0 & 0 & y_{25}
\end{bmatrix}
\]

The zeros express the absence of direct branches between those bus pairs in this simplified network model. They do not mean that the buses are electrically isolated from one another: Buses 3, 4 and 5 are each connected to Bus 2.

### Interpretation

The matrix structure is a direct mathematical reflection of the SLD. If the topology is entered incorrectly—for example, by connecting the three feeders in series—the nonzero pattern of the matrix will also be wrong.

The matrix should be built from the branch list and connectivity data, rather than manually hard-coding this specific pattern into the calculation function.

### Verification checks

- Matrix dimensions are \(5\times5\).
- Every in-service branch contributes to the correct diagonal elements.
- Each represented series branch contributes negative off-diagonal terms at its two terminal buses.
- Bus pairs without direct branches have zero off-diagonal elements under this model.
- For reciprocal branches without phase-shifting or asymmetric tap effects, the matrix is symmetric.
- With only the series branches shown, each row sums to zero. Shunt admittances or other modelled elements can change this check.

---

## Example 8 — Distinguish bus loads from branch admittances

### Objective

Understand why a constant-power load should not automatically be inserted into Y-bus as though it were a fixed series impedance.

### Constant-power load

A constant-power load is commonly described by active and reactive power:

\[
S_\text{load}=P_\text{load}+jQ_\text{load}
\]

Under a load convention, positive \(P_\text{load}\) and \(Q_\text{load}\) represent consumption.

For a constant-power model, current depends on the bus voltage. In complex form, using load power \(S=VI^*\):

\[
I_\text{load}=\left(\frac{S_\text{load}}{V}\right)^*
\]

where the star denotes complex conjugation.

This relationship is nonlinear with respect to voltage when power is fixed.

### Why this matters

The Y-bus matrix is commonly assembled from network branch admittances and any explicitly modelled shunt admittances. A constant-power load is not generally a fixed admittance because its current changes with voltage to maintain the specified power.

Therefore, the model must keep clear distinctions between:

- Series branch admittances.
- Explicit shunt admittances.
- Bus load specifications.
- Power-flow equations that use those load specifications.

Some studies may use an equivalent load admittance at a chosen operating point, but that is a specific approximation and must be documented.

### Verification checks

- Do not add \(P+jQ\) directly to a Y-bus matrix element.
- Do not silently convert a constant-power load to a fixed impedance.
- Confirm that the load sign convention is consistent between data, equations and reported results.

---

## 9. Engineering calculation record template

Use the following structure when adding a new worked example.

### Example title

**Objective:** What engineering question is being answered?

**Inputs:** List each value, its unit, and its source (CSV field, agreed system base, standard, or illustrative assumption).

**Assumptions:** State any simplifications or omitted effects.

**Equations:** Write the governing equations before substituting values.

**Calculation:** Show substitutions and intermediate steps with units.

**Result:** State the final result with suitable precision and units.

**Interpretation:** Explain what the result means physically and why it matters to the study.

**Verification:** Record independent checks, expected properties, or comparison results.

**Implementation link:** Identify the relevant Python function and test when one exists.

**Limitations:** State what the calculation does not include.

---

## 10. Open items before numerical examples are treated as project results

The following must be confirmed against the actual model before numerical outputs are presented as results for the five-bus system:

1. The base on which transformer `r_pu` and `x_pu` are stored.
2. The actual feeder lengths and per-kilometre resistance and reactance values in the CSV files.
3. The actual load values and their sign convention.
4. Whether line shunt effects or transformer tap effects are represented.
5. The precise source and slack-bus model used by the implementation.
6. Whether the current Python implementation applies each conversion once and only once.

Until those items are confirmed, the numerical values explicitly labelled illustrative remain teaching examples, not validated project results.

---

## 11. Suggested implementation sequence

Once the data conventions are confirmed, the calculations can be implemented and tested in this order:

1. Base impedance and admittance calculations.
2. Equipment-to-system per-unit base conversion.
3. Line series impedance calculation.
4. Physical-to-per-unit impedance conversion.
5. Complex branch admittance calculation.
6. Y-bus assembly from branch connectivity.
7. Matrix structure and numerical consistency checks.

Each calculation should have unit tests using small known examples, followed by integration tests using the existing five-bus CSV model.

**Document maintenance rule:** Update this document when equations, assumptions, input conventions or model capabilities change. Keep illustrative examples visibly separate from calculations based on actual project data.
