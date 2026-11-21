# 3D Turbulent Flow Through a Sudden Pipe Expansion Using OpenFOAM

## 1. Project Overview

This project investigates turbulent flow through a three-dimensional circular pipe with a sudden expansion using OpenFOAM. The study focuses on the flow physics associated with sudden expansion, including flow separation, recirculation, pressure recovery, and turbulence development.

A steady Reynolds-Averaged Navier–Stokes (RANS) approach with the SST \(k\)-\(\omega\) turbulence model is employed. Three mesh resolutions are investigated to assess mesh sensitivity and establish a suitable computational mesh for detailed flow-field analysis.

### Objectives

- Simulate turbulent flow through a sudden pipe expansion.
- Investigate velocity redistribution and pressure recovery.
- Identify flow separation and reverse-flow regions.
- Analyse turbulence quantities, including \(k\), \(\omega\), and turbulent eddy viscosity.
- Assess mesh sensitivity using three mesh resolutions.
- Examine numerical convergence and mass conservation.

## 2. Geometry and Operating Conditions

The computational domain consists of a smaller upstream pipe connected to a larger downstream pipe through an abrupt expansion.

| Parameter | Value |
|---|---:|
| Upstream pipe diameter | 0.05 m |
| Downstream pipe diameter | 0.10 m |
| Diameter expansion ratio | 2:1 |
| Cross-sectional area ratio | 4:1 |
| Expansion location | x = 0.5 m |
| Total domain length | 1.5 m |
| Reynolds number | 50,000 |

The sudden expansion produces an adverse pressure gradient and flow separation, resulting in recirculation regions and developing shear layers downstream of the expansion.

## 3. CFD Methodology

### Governing Equations

The simulation is based on the incompressible continuity and Reynolds-averaged momentum equations.

**Continuity:**

\[
\nabla \cdot \mathbf{U}=0
\]

**Momentum:**

\[
\nabla \cdot (\mathbf{U}\mathbf{U})
=
-\nabla p
+
\nabla \cdot
\left[
\nu_{\mathrm{eff}}
\left(\nabla \mathbf{U}+\nabla \mathbf{U}^{T}\right)
\right]
\]

where \(\mathbf{U}\) is the mean velocity, \(p\) is kinematic pressure, and \(\nu_{\mathrm{eff}}\) represents the effective kinematic viscosity.

### Turbulence Modelling

The SST \(k\)-\(\omega\) turbulence model is used to represent turbulent transport and dissipation.

The principal turbulence quantities analysed are:

- \(k\): turbulent kinetic energy.
- \(\omega\): specific dissipation rate.
- \(\nu_t\): turbulent eddy viscosity.

### Numerical Setup

- CFD solver: OpenFOAM 13
- Simulation approach: Steady RANS
- Turbulence model: SST \(k\)-\(\omega\)
- Mesh generation: blockMesh
- Post-processing: ParaView and Python
- Computational environment: Ubuntu on WSL

## 4. Mesh Generation and Mesh Sensitivity

Three mesh resolutions were generated and investigated.

| Mesh | Approximate cell count |
|---|---:|
| Baseline | 130,000 |
| Refined | 180,000 |
| Fine | 230,000 |

All three meshes were checked using `checkMesh`.

The mesh-sensitivity assessment considered the following quantities:

- Streamwise velocity (\(U_x\))
- Static pressure (\(p\))
- Turbulent kinetic energy (\(k\))
- Specific dissipation rate (\(\omega\))
- Turbulent eddy viscosity (\(\nu_t\))

The comparison demonstrated close agreement between the Refined and Fine mesh results for the principal flow quantities. The Baseline mesh exhibited more noticeable deviations, particularly in regions close to the expansion.

The Fine mesh was therefore selected for detailed flow-field analysis.

## 5. Numerical Convergence and Verification

The Fine-mesh simulation was completed at 3,000 iterations.

The final residuals were:

| Equation | Final residual |
|---|---:|
| \(U_x\) | \(2.68 \times 10^{-9}\) |
| \(U_y\) | \(1.80 \times 10^{-8}\) |
| \(U_z\) | \(1.99 \times 10^{-8}\) |
| \(p\) | \(3.49 \times 10^{-7}\) |
| \(\omega\) | \(6.08 \times 10^{-8}\) |
| \(k\) | \(5.05 \times 10^{-9}\) |

The final global continuity error was approximately \(-5.51 \times 10^{-9}\), while the cumulative continuity error was approximately \(-2.02 \times 10^{-7}\).

These results support the numerical convergence of the computed steady RANS solution.

Mass-flow conservation was also checked. The Refined and Fine meshes showed matching inlet and outlet volume-flow-rate magnitudes of approximately 0.0196148 m³/s.

## 6. Results and Discussion

### 6.1 Streamwise Velocity

The streamwise velocity distribution shows a pronounced increase in centreline velocity immediately downstream of the expansion, followed by gradual velocity redistribution along the enlarged pipe.

The Refined and Fine mesh profiles show close agreement, while the Baseline mesh exhibits larger deviations near the expansion.

### 6.2 Static Pressure

The pressure distribution exhibits a pronounced pressure recovery downstream of the expansion. The Refined and Fine mesh profiles are in close agreement, supporting the selection of the Fine mesh.

Pressure values are presented in the solver's pressure units.

### 6.3 Flow Separation and Reverse Flow

The streamwise velocity contour identifies negative velocity regions adjacent to the expanded walls. These regions correspond to flow reversal and recirculation following separation at the expansion step.

The reverse-flow regions are strongest near the expansion and progressively weaken downstream.

### 6.4 Turbulent Kinetic Energy

The turbulent kinetic energy distribution shows elevated values in the shear layers downstream of the expansion. These regions correspond to strong velocity gradients between the main flow and the recirculating regions.

The turbulence intensity decreases progressively farther downstream.

### 6.5 Specific Dissipation Rate

The specific dissipation rate exhibits a pronounced peak immediately downstream of the expansion. The comparison indicates greater mesh sensitivity in the local peak value than in the downstream distribution.

### 6.6 Turbulent Eddy Viscosity

The turbulent eddy viscosity increases in the developing shear-layer region. The Refined and Fine mesh profiles show close agreement, indicating relatively low sensitivity to further refinement for this quantity.

### 6.7 Near-Wall Resolution

The dimensionless wall distance \(y^+\) was exported from the Fine-mesh solution and visualised on the pipe wall.

The distribution provides a diagnostic of near-wall mesh resolution and should be interpreted in relation to the near-wall treatment used by the SST \(k\)-\(\omega\) model.

## 7. Fine-Mesh Visualisations

The following visualisations are generated from the Fine-mesh solution at the final simulation time.

| Field | Visualisation |
|---|---|
| Streamwise velocity | `Fine_Ux_Contour.png` |
| Static pressure | `Fine_Pressure_Contour.png` |
| Turbulent kinetic energy | `Fine_k_Contour.png` |
| Specific dissipation rate | `Fine_omega_Contour.png` |
| Turbulent eddy viscosity | `Fine_nut_Contour.png` |
| Dimensionless wall distance | `Fine_yPlus_Contour.png` |

The reverse-flow and TKE visualisations are also retained in the Fine-mesh case directory.

## 8. Conclusion

The numerical investigation demonstrates the characteristic flow behaviour associated with a turbulent sudden pipe expansion.

The results identify flow separation, downstream recirculation, pressure recovery, and turbulence production in the developing shear layers.

The mesh-sensitivity assessment shows close agreement between the Refined and Fine meshes for the principal flow quantities. The Fine mesh was selected for detailed flow-field analysis.

The study also demonstrates the importance of mesh resolution in capturing local turbulence behaviour near geometric discontinuities.

## 9. Limitations and Future Work

Potential extensions of this investigation include:

- Quantitative determination of the reattachment length.
- Further analysis of wall shear stress and near-wall resolution.
- Comparison with experimental or published benchmark data.
- Investigation of alternative turbulence models.
- Transient simulations to examine unsteady flow structures.
- Higher-resolution simulations with additional computational resources.

---

## Tools and Technologies

- OpenFOAM 13
- ParaView
- Python
- NumPy
- Pandas
- Matplotlib
- Linux / Ubuntu (WSL)

**Project focus:** Computational Fluid Dynamics | Turbulent Flow | RANS Modelling | Mesh Sensitivity | Flow Separation