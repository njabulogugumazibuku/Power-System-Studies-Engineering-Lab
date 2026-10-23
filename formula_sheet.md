# Power System Studies Formula Sheet

**Project:** Power System Studies Engineering Lab  
**Status:** Learning reference — educational use only  
**System convention:** Balanced three-phase AC system unless stated otherwise  
**Default project bases:** $S_\text{base}=100\ \text{MVA}$, $f=50\ \text{Hz}$

> **Scope note:** This sheet collects formulas introduced in the early system-modelling and network-analysis milestones. All examples are synthetic. Verify assumptions and data bases before using any formula in a study. This is not a utility-grade design or operating document.

## 1. Symbols and conventions

| Symbol | Meaning | Typical unit |
|---|---|---|
| $V_{LL}$ | Line-to-line RMS voltage | V or kV |
| $V_{ph}$ | Phase-to-neutral RMS voltage | V |
| $I_L$ | Line current | A |
| $S=P+jQ$ | Complex power | VA, MVA |
| $P$ | Active power | W, MW |
| $Q$ | Reactive power | var, Mvar |
| $R$ | Resistance | $\Omega$ |
| $X$ | Reactance | $\Omega$ |
| $Z=R+jX$ | Complex impedance | $\Omega$ |
| $Y=G+jB$ | Complex admittance | S |
| $j$ | Imaginary unit, $j^2=-1$ | — |
| $S_\text{base}$ | Three-phase apparent-power base | MVA |
| $V_\text{base}$ | Line-to-line voltage base | kV |
| $Z_\text{base}$ | Impedance base | $\Omega$ |
| $Y_\text{base}$ | Admittance base | S |

**Sign convention:** $S=P+jQ$. Inductive loads usually consume positive reactive power $Q>0$; capacitive injection is often represented by $Q<0$ under the load convention. Always state the convention used by a model or software package.

## 2. Complex numbers and impedance

### 2.1 Complex impedance

$$
Z=R+jX
$$

- $R$: real part (resistance).
- $X$: imaginary part (reactance); positive $X$ is inductive under the usual passive sign convention.

Magnitude and phase angle:

$$
|Z|=\sqrt{R^2+X^2}
$$

$$
\theta_Z=\operatorname{atan2}(X,R)
$$

**Example:** If $Z=3+j4\ \Omega$,

$$
|Z|=\sqrt{3^2+4^2}=5\ \Omega
$$

$$
\theta_Z=\operatorname{atan2}(4,3)\approx53.13^\circ
$$

### 2.2 Series impedances

For impedances in series, add complex impedances:

$$
Z_\text{eq}=\sum_{k=1}^{n} Z_k
=\sum_{k=1}^{n}R_k+j\sum_{k=1}^{n}X_k
$$

Do not add impedance magnitudes unless a special approximation is explicitly justified.

### 2.3 Ohm's law in AC phasor form

$$
\underline V=\underline Z\,\underline I
\qquad
\underline I=\frac{\underline V}{\underline Z}
$$

Phasors are complex RMS quantities. Use consistent phase/line quantities and units.

## 3. Balanced three-phase relationships

For a balanced three-phase system, using RMS values:

$$
|S|=\sqrt{3}\,V_{LL}I_L
$$

$$
P=\sqrt{3}\,V_{LL}I_L\cos\phi
$$

$$
Q=\sqrt{3}\,V_{LL}I_L\sin\phi
$$

$$
S=P+jQ
$$

$$
|S|=\sqrt{P^2+Q^2}
$$

Power factor:

$$
\mathrm{pf}=\frac{P}{|S|}=\cos\phi
$$

Current magnitude from three-phase apparent power:

$$
I_L=\frac{|S|}{\sqrt{3}\,V_{LL}}
$$

**Unit check:** If $S$ is in MVA and $V_{LL}$ is in kV, the current formula gives kA:

$$
I_L[\mathrm{kA}]=\frac{|S|[\mathrm{MVA}]}{\sqrt{3}\,V_{LL}[\mathrm{kV}]}
$$

For a balanced star (wye) connection:

$$
V_{LL}=\sqrt{3}\,V_{ph},\qquad I_L=I_{ph}
$$

For a balanced delta connection:

$$
V_{LL}=V_{ph},\qquad I_L=\sqrt{3}\,I_{ph}
$$

These connection relationships should not be applied blindly to unbalanced systems.

## 4. Per-unit system

Per-unit (pu) expresses a quantity as a ratio to a chosen base:

$$
x_{pu}=\frac{x_\text{actual}}{x_\text{base}}
$$

For impedance:

$$
Z_{pu}=\frac{Z_\text{actual}}{Z_\text{base}}
\qquad
Z_\text{actual}=Z_{pu}Z_\text{base}
$$

For voltage and current:

$$
V_{pu}=\frac{V_\text{actual}}{V_\text{base}}
\qquad
I_{pu}=\frac{I_\text{actual}}{I_\text{base}}
$$

For power:

$$
S_{pu}=\frac{S_\text{actual}}{S_\text{base}}
$$

Use compatible quantities: three-phase MVA with line-to-line kV for the common three-phase base system.

### 4.1 Three-phase base quantities

Choose $S_\text{base}$ as three-phase apparent power and $V_\text{base}$ as line-to-line voltage. Then:

$$
I_\text{base}=\frac{S_\text{base}}{\sqrt{3}\,V_\text{base}}
$$

$$
Z_\text{base}=\frac{V_\text{base}^2}{S_\text{base}}
$$

$$
Y_\text{base}=\frac{1}{Z_\text{base}}
=\frac{S_\text{base}}{V_\text{base}^2}
$$

**Convenient engineering units:** with $V_\text{base}$ in kV and $S_\text{base}$ in MVA,

$$
Z_\text{base}[\Omega]=\frac{V_\text{base}[\mathrm{kV}]^2}{S_\text{base}[\mathrm{MVA}]}
$$

$$
I_\text{base}[\mathrm{kA}]
=\frac{S_\text{base}[\mathrm{MVA}]}{\sqrt{3}\,V_\text{base}[\mathrm{kV}]}
$$

### 4.2 Project base examples

Using the educational project base $S_\text{base}=100\ \mathrm{MVA}$:

At a 33 kV bus:

$$
Z_\text{base}=\frac{33^2}{100}=10.89\ \Omega
$$

$$
Y_\text{base}=\frac{1}{10.89}\approx0.09183\ \mathrm{S}
$$

$$
I_\text{base}=\frac{100}{\sqrt{3}\times33}
\approx1.7495\ \mathrm{kA}
$$

At a 132 kV bus:

$$
Z_\text{base}=\frac{132^2}{100}=174.24\ \Omega
$$

$$
I_\text{base}=\frac{100}{\sqrt{3}\times132}
\approx0.4374\ \mathrm{kA}
$$

Across an ideal transformer, voltage bases should follow the transformer rated voltage ratio if the same system MVA base is used. The base impedance changes with the square of the voltage base.

### 4.3 Converting per-unit impedance between bases

General formula:

$$
Z_{pu,\mathrm{new}}=
Z_{pu,\mathrm{old}}
\left(\frac{S_{\mathrm{base,new}}}{S_{\mathrm{base,old}}}\right)
\left(\frac{V_{\mathrm{base,old}}}{V_{\mathrm{base,new}}}\right)^2
$$

The voltage bases in this formula must refer to the same electrical side / voltage level.

If the voltage base is unchanged:

$$
Z_{pu,\mathrm{new}}=
Z_{pu,\mathrm{old}}
\frac{S_{\mathrm{base,new}}}{S_{\mathrm{base,old}}}
$$

**Example:** $Z_{pu,\mathrm{old}}=j0.15$ on 25 MVA, converted to 100 MVA with the same voltage base:

$$
Z_{pu,\mathrm{new}}=j0.15\frac{100}{25}=j0.60
$$

**Transformer-data warning:** A transformer impedance reported as $j0.20\ pu$ on its own 50 MVA rating is $j0.40\ pu$ on a 100 MVA system base if the corresponding voltage bases match. Do not convert it unless the original impedance base is known. A pu number without its base is incomplete data.

## 5. Line impedance

For a uniform line represented by series resistance and reactance per unit length:

$$
R_\text{line}=r\,\ell
\qquad
X_\text{line}=x\,\ell
$$

$$
Z_\text{line}=(r+jx)\ell
=R_\text{line}+jX_\text{line}
$$

where $r$ and $x$ are per-length parameters and $\ell$ is line length.

**Unit check:** $(\Omega/\mathrm{km})\times\mathrm{km}=\Omega$.

**Project example:** $\ell=8\ \mathrm{km}$, $r=0.40\ \Omega/\mathrm{km}$, $x=0.35\ \Omega/\mathrm{km}$:

$$
R_\text{line}=0.40\times8=3.2\ \Omega
$$

$$
X_\text{line}=0.35\times8=2.8\ \Omega
$$

$$
Z_\text{line}=3.2+j2.8\ \Omega
$$

On the 33 kV, 100 MVA base:

$$
Z_{\text{line},pu}=\frac{3.2+j2.8}{10.89}
\approx0.29385+j0.25712
$$

This is a simplified series-impedance model. It omits shunt capacitance, conductance, temperature effects, mutual coupling and other effects unless they are added explicitly.

## 6. Admittance

Admittance is the reciprocal of impedance:

$$
Y=\frac{1}{Z}
$$

For $Z=R+jX$:

$$
Y=\frac{1}{R+jX}
=\frac{R-jX}{R^2+X^2}
=G+jB
$$

Therefore:

$$
G=\frac{R}{R^2+X^2}
\qquad
B=-\frac{X}{R^2+X^2}
$$

Here $G$ is conductance and $B$ is susceptance. For a series inductive impedance with $X>0$, its series admittance has $B<0$.

**Important:** Do not calculate $1/R+j(1/X)$. The reciprocal applies to the complete complex number.

**Example:** $Z=3+j4\ \Omega$:

$$
Y=\frac{3-j4}{3^2+4^2}
=0.12-j0.16\ \mathrm{S}
$$

For per-unit values:

$$
Y_{pu}=\frac{1}{Z_{pu}}
$$

With compatible bases:

$$
Y_{pu}=Y_\text{actual}Z_\text{base}
$$

**Project example:** For $Z=3.2+j2.8\ \Omega$:

$$
Y=\frac{3.2-j2.8}{3.2^2+2.8^2}
\approx0.17699-j0.15487\ \mathrm{S}
$$

On a 33 kV, 100 MVA base:

$$
Y_{pu}\approx1.92743-j1.68650
$$

Values above are rounded.

## 7. Bus-admittance matrix (Y-bus)

The nodal network equation is:

$$
\mathbf I_\text{bus}=\mathbf Y_\text{bus}\mathbf V_\text{bus}
$$

For bus $i$:

$$
I_i=\sum_{k=1}^{n}Y_{ik}V_k
$$

### 7.1 Off-diagonal elements

For a simple branch directly connecting distinct buses $i$ and $k$, with series admittance $y_{ik}$, and no off-nominal tap or additional coupling:

$$
Y_{ik}=-y_{ik},\qquad i\ne k
$$

If there is no direct branch between buses $i$ and $k$, then $Y_{ik}=0$ in this simple model.

### 7.2 Diagonal elements

For a bus $i$:

$$
Y_{ii}=\sum_{k\ne i} y_{ik}+y_{i,\mathrm{shunt}}
$$

That is, sum the series admittances of branches incident on the bus and add any explicitly modelled shunt admittances at that bus. More complete models must account for line charging, transformer taps, phase shifts and other branch terms correctly.

### 7.3 Simple three-bus illustrative example

Suppose the per-unit series impedances are:

$$
Z_{12}=0.1+j0.2,\quad
Z_{13}=0.1+j0.3,\quad
Z_{23}=0.05+j0.25
$$

Their admittances are approximately:

$$
y_{12}=2-j4,\quad
y_{13}=1-j3,\quad
y_{23}=0.76923-j3.84615
$$

Using negative branch admittances off the diagonal and summing connected admittances on the diagonal:

$$
\mathbf Y_\text{bus}\approx
\begin{bmatrix}
3-j7 & -2+j4 & -1+j3\\
-2+j4 & 2.76923-j7.84615 & -0.76923+j3.84615\\
-1+j3 & -0.76923+j3.84615 & 1.76923-j6.84615
\end{bmatrix}
$$

This is a teaching example only; it is **not** the Y-bus matrix of the project's CSV network.

For a network containing only reciprocal series branches with no phase-shifting elements or asymmetric terms, the Y-bus is symmetric:

$$
Y_{ik}=Y_{ki}
$$

### 7.4 Useful Y-bus checks

- Each off-diagonal term should match the negative of the relevant branch admittance under the simple branch model.
- Each diagonal term should equal the sum of connected branch admittances plus modelled shunts.
- For a simple reciprocal network, check symmetry within numerical tolerance.
- Confirm bus ordering is consistent between the matrix and the bus list.
- Check units and per-unit bases are consistent before assembling the matrix.

## 8. Quick reference: common mistakes

1. **Mixing kV, V, MVA and VA.** Use consistent units; the kV/MVA base formulas above are convenient because they yield ohms and kA.
2. **Using phase voltage where line-to-line voltage is expected.** The common three-phase base formula here uses line-to-line voltage.
3. **Forgetting a transformer's original impedance base.** Always record the MVA and voltage bases attached to equipment pu data.
4. **Taking the reciprocal of $R$ and $X$ separately.** Calculate the reciprocal of the complex impedance.
5. **Confusing actual and per-unit quantities.** Label values with units or `pu`.
6. **Using a diagram as numerical truth.** The diagram, CSV files, model objects and tests must describe the same network.
7. **Treating the simplified line model as complete.** State whether shunt capacitance, taps and other effects are included.

## 9. Topics to add in later milestones

Add these sections when the project reaches them, rather than treating them as already implemented:

- Complex power from bus voltage and current: $S=VI^*$ per phase; for balanced three-phase totals, $S_{3\phi}=3V_{ph}I_{ph}^*=\sqrt{3}V_{LL}I_L^*$ with compatible phasor references.
- Power-flow equations and the distinction between slack, PV and PQ buses.
- Newton–Raphson power flow and mismatch equations.
- Transformer equivalent circuits and off-nominal tap modelling.
- Short-circuit calculations and sequence networks.
- Voltage drop, losses and branch-flow calculations.

---

**Maintenance rule:** When a new equation is introduced in a study, add its definition, assumptions, units, and at least one checked numerical example here. Keep examples labelled as illustrative unless they are calculated from the current, validated project data.
