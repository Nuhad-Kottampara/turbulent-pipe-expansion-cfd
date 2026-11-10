from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent

CASES = {
    "Baseline": PROJECT_DIR / "sudden-expansion" / "TurbulenceProfile_baseline.csv",
    "Refined": PROJECT_DIR / "sudden-expansion-refined" / "TurbulenceProfile_refined.csv",
    "Fine": PROJECT_DIR / "sudden-expansion-fine" / "TurbulenceProfile_fine.csv",
}

FIELDS = {
    "k": (
        "Turbulent kinetic energy, k",
        "Turbulent kinetic energy profiles by mesh",
    ),
    "omega": (
        "Specific dissipation rate, omega",
        "Specific dissipation rate profiles by mesh",
    ),
    "nut": (
        "Eddy viscosity, nut",
        "Eddy viscosity profiles by mesh",
    ),
}

PAIRS = [
    ("Baseline", "Refined"),
    ("Refined", "Fine"),
    ("Baseline", "Fine"),
]


# Load each CSV once.
raw_data = {}

for mesh, file_path in CASES.items():
    if not file_path.exists():
        raise FileNotFoundError(f"Missing CSV: {file_path}")

    df = pd.read_csv(file_path)
    required = {"arc_length", *FIELDS.keys()}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"{file_path.name} is missing columns: {sorted(missing)}"
        )

    raw_data[mesh] = df
    print(f"{mesh}: loaded {len(df)} rows from {file_path.name}")


# Process each field separately.
for field, (ylabel, title) in FIELDS.items():
    field_data = {}

    # Keep valid numeric data, sort it, and remove duplicate sample locations.
    for mesh, df in raw_data.items():
        clean = df[["arc_length", field]].copy()
        clean["arc_length"] = pd.to_numeric(clean["arc_length"], errors="coerce")
        clean[field] = pd.to_numeric(clean[field], errors="coerce")
        clean = clean.dropna().sort_values("arc_length")
        clean = clean.drop_duplicates(subset="arc_length")

        if len(clean) < 2:
            raise ValueError(
                f"{mesh} has fewer than two valid points for {field}."
            )

        field_data[mesh] = clean
        print(f"{mesh}: {len(clean)} valid points for {field}")

    # Use baseline sample locations over the range shared by all three meshes.
    start = max(df["arc_length"].min() for df in field_data.values())
    end = min(df["arc_length"].max() for df in field_data.values())

    if start >= end:
        raise ValueError(
            f"The {field} profiles do not have an overlapping arc_length range."
        )

    baseline = field_data["Baseline"]
    x = baseline.loc[
        baseline["arc_length"].between(start, end), "arc_length"
    ].to_numpy()

    if len(x) < 2:
        raise ValueError(
            f"Fewer than two baseline points fall in the shared range for {field}."
        )

    # Interpolate each mesh onto the same arc_length locations.
    profiles = pd.DataFrame({"arc_length": x})

    for mesh, df in field_data.items():
        profiles[mesh] = np.interp(
            x,
            df["arc_length"].to_numpy(),
            df[field].to_numpy(),
        )

    # Report the peak value and location for each mesh.
    print(f"\n{field} profile peaks:")

    for mesh in ("Baseline", "Refined", "Fine"):
        peak_index = profiles[mesh].idxmax()
        print(
            f"{mesh}: peak={profiles.loc[peak_index, mesh]:.6g} "
            f"at arc_length={profiles.loc[peak_index, 'arc_length']:.6g}"
        )

    # Locate the largest pointwise Fine–Refined difference.
    fine_refined_diff = profiles["Fine"] - profiles["Refined"]
    max_diff_index = fine_refined_diff.abs().idxmax()
    max_diff = abs(fine_refined_diff.loc[max_diff_index])
    fine_value = abs(profiles.loc[max_diff_index, "Fine"])
    relative_diff = (
        100 * max_diff / fine_value if fine_value else float("nan")
    )

    print(
        f"Fine–Refined largest difference: {max_diff:.6g} "
        f"at arc_length={profiles.loc[max_diff_index, 'arc_length']:.6g} "
        f"(Refined={profiles.loc[max_diff_index, 'Refined']:.6g}, "
        f"Fine={profiles.loc[max_diff_index, 'Fine']:.6g}, "
        f"{relative_diff:.2f}% of Fine)"
    )

    # Report pairwise profile differences and add them to the output CSV.
    print(f"\nPairwise {field}-profile differences:")

    for first, second in PAIRS:
        diff = profiles[second] - profiles[first]
        rmse = np.sqrt(np.mean(diff**2))
        mae = np.mean(np.abs(diff))
        max_abs_diff = np.max(np.abs(diff))

        reference_range = profiles[first].max() - profiles[first].min()
        normalized_rmse = (
            rmse / reference_range if reference_range else float("nan")
        )

        print(
            f"{first} vs {second}: "
            f"MAE={mae:.6g}, RMSE={rmse:.6g}, "
            f"max |difference|={max_abs_diff:.6g}, "
            f"normalized RMSE={normalized_rmse:.3%}"
        )

        profiles[f"{second}_minus_{first}"] = diff

    # Save the sampled values and pairwise differences.
    csv_path = PROJECT_DIR / f"{field}_profile_comparison.csv"
    profiles.to_csv(csv_path, index=False)

    # Plot the three mesh profiles.
    fig, ax = plt.subplots(figsize=(9, 5.5))

    for mesh in ("Baseline", "Refined", "Fine"):
        ax.plot(profiles["arc_length"], profiles[mesh], label=mesh)

    ax.set_xlabel("Arc length")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

    plot_path = PROJECT_DIR / f"{field}_profile_comparison.png"
    fig.savefig(plot_path, dpi=200)
    plt.close(fig)

    print(f"Saved comparison data: {csv_path}")
    print(f"Saved profile plot: {plot_path}")