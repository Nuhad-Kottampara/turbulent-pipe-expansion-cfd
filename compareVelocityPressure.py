
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# --------------------------------------------------
# 1. Project configuration
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

CASES = {
    "Baseline": PROJECT_DIR / "sudden-expansion" / "TurbulenceProfile_baseline.csv",
    "Refined": PROJECT_DIR / "sudden-expansion-refined" / "TurbulenceProfile_refined.csv",
    "Fine": PROJECT_DIR / "sudden-expansion-fine" / "TurbulenceProfile_fine.csv",
}

FIELDS = {
    "U:0": (
        "Streamwise velocity, Ux (m/s)",
        "Streamwise velocity profiles by mesh",
        "Ux",
    ),
    "p": (
        "Pressure, p (solver units)",
        "Pressure profiles by mesh",
        "p",
    ),
}

PAIRS = [
    ("Baseline", "Refined"),
    ("Refined", "Fine"),
    ("Baseline", "Fine"),
]


# --------------------------------------------------
# 2. Load and validate datasets
# --------------------------------------------------

raw_data = {}

for mesh, file_path in CASES.items():

    if not file_path.exists():
        raise FileNotFoundError(f"Missing CSV: {file_path}")

    df = pd.read_csv(file_path)

    required = {
        "Points:0",
        "U:0",
        "p",
        "vtkValidPointMask",
    }

    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"{file_path.name} is missing columns: {sorted(missing)}"
        )

    # Retain valid sampled internal points only.
    df = df.loc[df["vtkValidPointMask"] == 1].copy()

    raw_data[mesh] = df

    print(
        f"{mesh}: {len(df)} valid internal samples "
        f"loaded from {file_path.name}"
    )


# --------------------------------------------------
# 3. Process velocity and pressure
# --------------------------------------------------

for field, (ylabel, title, output_name) in FIELDS.items():

    field_data = {}

    for mesh, df in raw_data.items():

        clean = df[["Points:0", field]].copy()

        clean["Points:0"] = pd.to_numeric(
            clean["Points:0"], errors="coerce"
        )

        clean[field] = pd.to_numeric(
            clean[field], errors="coerce"
        )

        clean = clean.dropna()
        clean = clean.sort_values("Points:0")
        clean = clean.drop_duplicates(subset="Points:0")

        if len(clean) < 2:
            raise ValueError(
                f"{mesh} has insufficient valid points for {field}."
            )

        field_data[mesh] = clean

    # Determine common X-coordinate range.

    start = max(
        df["Points:0"].min()
        for df in field_data.values()
    )

    end = min(
        df["Points:0"].max()
        for df in field_data.values()
    )

    if start >= end:
        raise ValueError(
            f"No common X-coordinate range for {field}."
        )

    baseline = field_data["Baseline"]

    x = baseline.loc[
        baseline["Points:0"].between(start, end),
        "Points:0",
    ].to_numpy()

    if len(x) < 2:
        raise ValueError(
            f"Insufficient common sampling points for {field}."
        )

    # Interpolate all meshes onto common X positions.

    profiles = pd.DataFrame({"x": x})

    for mesh, df in field_data.items():

        profiles[mesh] = np.interp(
            x,
            df["Points:0"].to_numpy(),
            df[field].to_numpy(),
        )

    # --------------------------------------------------
    # 4. Profile statistics
    # --------------------------------------------------

    print(f"\n{output_name} profile statistics:")

    for mesh in ("Baseline", "Refined", "Fine"):

        values = profiles[mesh]

        max_index = values.idxmax()
        min_index = values.idxmin()

        print(f"\n{mesh}")

        print(
            f"Maximum: {values.max():.6g} "
            f"at x = {profiles.loc[max_index, 'x']:.6f} m"
        )

        print(
            f"Minimum: {values.min():.6g} "
            f"at x = {profiles.loc[min_index, 'x']:.6f} m"
        )

    # --------------------------------------------------
    # 5. Pairwise mesh comparison
    # --------------------------------------------------

    print(f"\nPairwise {output_name} differences:")

    for first, second in PAIRS:

        diff = profiles[second] - profiles[first]

        mae = np.mean(np.abs(diff))
        rmse = np.sqrt(np.mean(diff**2))
        max_diff = np.max(np.abs(diff))

        reference_range = (
            profiles[first].max() -
            profiles[first].min()
        )

        nrmse = (
            rmse / reference_range
            if reference_range != 0
            else float("nan")
        )

        print(
            f"{first} vs {second}: "
            f"MAE={mae:.6g}, "
            f"RMSE={rmse:.6g}, "
            f"Max difference={max_diff:.6g}, "
            f"NRMSE={nrmse:.3%}"
        )

        profiles[f"{second}_minus_{first}"] = diff

    # --------------------------------------------------
    # 6. Export comparison CSV
    # --------------------------------------------------

    csv_path = (
        PROJECT_DIR /
        f"{output_name}_profile_comparison.csv"
    )

    profiles.to_csv(csv_path, index=False)

    # --------------------------------------------------
    # 7. Generate comparison plot
    # --------------------------------------------------

    fig, ax = plt.subplots(figsize=(10, 5.5))

    for mesh in ("Baseline", "Refined", "Fine"):

        ax.plot(
            profiles["x"],
            profiles[mesh],
            label=mesh,
            linewidth=1.8,
        )

    ax.set_xlabel("Axial coordinate, x (m)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()

    plot_path = (
        PROJECT_DIR /
        f"{output_name}_profile_comparison.png"
    )

    fig.savefig(plot_path, dpi=300)
    plt.close(fig)

    print(f"\nSaved CSV: {csv_path}")
    print(f"Saved plot: {plot_path}")


print("\nVelocity and pressure post-processing completed.")
