import pandas as pd

df = pd.read_csv("../results/experiments.csv")

print("\n===== FINAL STATISTICS =====\n")

print("SUCCESS RATE")
success_rate = (df["success"].sum() / len(df)) * 100
print(f"{success_rate:.1f}%")

print("\nDOM DIFF TIMES (ms)")
print(f"Mean: {df['diff_ms'].mean():.2f}")
print(f"Min : {df['diff_ms'].min():.2f}")
print(f"Max : {df['diff_ms'].max():.2f}")

print("\nREGENERATION TIMES (s)")
print(f"Mean: {df['regen_s'].mean():.2f}")
print(f"Min : {df['regen_s'].min():.2f}")
print(f"Max : {df['regen_s'].max():.2f}")

print("\nDOM OPERATIONS")
print(f"Min : {df['dom_ops'].min()}")
print(f"Max : {df['dom_ops'].max()}")

print("\nFAILURE COUNT")
failures = len(df[df["success"] == 0])
print(f"{failures}")