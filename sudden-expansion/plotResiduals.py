import re
import matplotlib.pyplot as plt

log_file = "log.cleanRun"

fields = ["Ux", "Uy", "Uz", "p", "omega", "k"]
residuals = {field: [] for field in fields}

with open(log_file, "r") as file:
    for line in file:
        for field in fields:
            pattern = (
                rf"Solving for {field}, Initial residual = "
                rf"([0-9.eE+-]+)"
            )
            match = re.search(pattern, line)
            if match:
                residuals[field].append(float(match.group(1)))

plt.figure(figsize=(11, 7))

for field, values in residuals.items():
    if values:
        plt.semilogy(
            range(1, len(values) + 1),
            values,
            label=field,
            linewidth=1.2
        )

plt.xlabel("Outer iteration")
plt.ylabel("Initial residual")
plt.title("Residual History — Sudden Expansion CFD")

plt.grid(True, which="both", linestyle="--", alpha=0.4)
plt.legend()
plt.tight_layout()

plt.savefig("residualHistory.png", dpi=200)
plt.show()