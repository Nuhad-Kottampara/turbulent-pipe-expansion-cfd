# 3D Turbulent Flow Through a Sudden Pipe Expansion

**CFD Engineering Portfolio Project | OpenFOAM 13 | 3D RANS Simulation**

## Project Overview

This project investigates turbulent incompressible flow through a three-dimensional circular pipe with a sudden expansion. The objective is to analyse flow separation, recirculation, pressure and velocity development, and turbulence behaviour, while evaluating mesh sensitivity.

## Simulation Results

**Streamwise velocity**

![Fine mesh streamwise velocity contour](./sudden-expansion-fine/Fine_Ux_Contour.png)

**Pressure distribution**

![Fine mesh pressure contour](./sudden-expansion-fine/Fine_Pressure_Contour.png)

## Geometry and Operating Conditions

| Parameter | Value |
|---|---:|
| Upstream diameter | 0.05 m |
| Downstream diameter | 0.10 m |
| Expansion location | 0.50 m |
| Domain length | 1.50 m |
| Reynolds number | 50,000 |
| Flow regime | Turbulent |

## CFD Methodology

- **Solver:** OpenFOAM 13 – `simpleFoam`
- **Approach:** Steady incompressible RANS
- **Turbulence model:** SST k–ω
- **Mesh generation:** `blockMesh`
- **Mesh validation:** `checkMesh`
- **Parallelisation:** Two-subdomain MPI
- **Post-processing:** ParaView and Python

Three mesh resolutions were investigated:

| Mesh | Approximate cells |
|---|---:|
| Baseline | 130,000 |
| Refined | 180,000 |
| Fine | 230,000 |

## Key Findings

| Metric | Result |
|---|---:|
| Maximum sampled centreline velocity (Fine) | 5.39 m/s |
| Maximum sampled turbulent kinetic energy (Fine) | 4.69 m²/s² |
| Maximum sampled specific dissipation rate (Fine) | 3,887 s⁻¹ |
| Ux MAE, Refined vs Fine | 0.0061 m/s |
| Ux RMSE, Refined vs Fine | 0.0446 m/s |
| Pressure MAE, Refined vs Fine | 0.0226 m²/s² |
| Pressure RMSE, Refined vs Fine | 0.0357 m²/s² |

The results indicate close agreement between the Refined and Fine mesh velocity and pressure profiles. Turbulence quantities, particularly the peak specific dissipation rate, remain locally sensitive to mesh refinement.

## Repository Structure

| Directory / Files | Contents |
|---|---|
| `sudden-expansion/` | Baseline mesh case |
| `sudden-expansion-refined/` | Refined mesh case |
| `sudden-expansion-fine/` | Fine mesh case, visualisations and post-processing data |
| `baseline-straight-pipe/` | Additional straight-pipe case |
| `compareVelocityPressure.py` | Velocity and pressure comparison |
| `compareTurbulenceProfiles.py` | Turbulence profile comparison |
| `*_profile_comparison.csv` | Extracted comparison datasets |
| `*_profile_comparison.png` | Mesh-comparison plots |

Each simulation directory contains its relevant OpenFOAM case files and supporting outputs.

## Limitations and Future Work

- Quantitative determination of the reattachment length.
- Further near-wall resolution and y-plus assessment.
- Additional mesh refinement around the expansion.
- Validation against experimental or published benchmark data.
- Comparison with alternative turbulence models.

## Tools and Technologies

**OpenFOAM 13 · ParaView · Python · NumPy · Pandas · Matplotlib · Ubuntu 24.04 · WSL**

---

*CFD portfolio project demonstrating practical experience in turbulence modelling, mesh sensitivity analysis, numerical convergence assessment and CFD post-processing.*