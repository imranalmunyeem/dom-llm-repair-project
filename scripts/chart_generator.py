import pandas as pd
import matplotlib.pyplot as plt

# LOAD CSV
df = pd.read_csv("../results/experiments.csv")

# -----------------------------
# SUCCESS RATE CHART
# -----------------------------

success_counts = df["success"].value_counts()

plt.figure(figsize=(5,5))
success_counts.plot(kind="bar")

plt.title("Repair Success Rate")
plt.xlabel("Success")
plt.ylabel("Count")

plt.savefig("../charts/success_rate.png")

plt.close()

# -----------------------------
# CHANGE TYPE DISTRIBUTION
# -----------------------------

change_counts = df["change_type"].value_counts()

plt.figure(figsize=(6,5))
change_counts.plot(kind="bar")

plt.title("DOM Change Type Distribution")
plt.xlabel("Change Type")
plt.ylabel("Count")

plt.savefig("../charts/change_distribution.png")

plt.close()

# -----------------------------
# MAINTENANCE EFFORT
# -----------------------------

plt.figure(figsize=(6,5))

plt.bar(df["attempt_id"], df["regen_s"])

plt.title("Maintenance Effort (Repair Runtime)")
plt.xlabel("Attempt ID")
plt.ylabel("Repair Time (seconds)")

plt.savefig("../charts/maintenance_effort.png")

plt.close()

print("\nCharts generated successfully.")