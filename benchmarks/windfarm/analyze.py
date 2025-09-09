#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} RESULTS_DIR")
    sys.exit(1)

results_dir = Path(sys.argv[1])
csv_files = list(results_dir.glob("*.csv"))

if not csv_files:
    print(f"No CSV files found in {results_dir}")
    sys.exit(1)

# Load and label each CSV by filename
dfs = []
for csv_file in csv_files:
    label = csv_file.stem  # engine name from filename
    df = pd.read_csv(csv_file)
    df["engine"] = label
    dfs.append(df)

# Combine all into one DataFrame
df_all = pd.concat(dfs, ignore_index=True)

# Ensure duration is numeric
df_all["duration_seconds"] = pd.to_numeric(df_all["duration_seconds"], errors="coerce")

# Pivot for plotting (duration)
pivot_duration = df_all.pivot(index="query_file", columns="engine", values="duration_seconds")

# Plot durations
pivot_duration.plot(kind="bar", figsize=(12, 6))
plt.ylabel("Duration (seconds)")
plt.yscale('log')
plt.ylim(bottom=0)
plt.title("Query Execution Time")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(results_dir / "duration_comparison.png")
plt.close()
