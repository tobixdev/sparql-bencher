#!/usr/bin/env python3
import csv
import glob
import json
import sys
import time
from pathlib import Path

import requests

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} RESULTS_FILE QUERY_URL")
    sys.exit(1)

results_file = Path(sys.argv[1])
query_url = sys.argv[2]

# Ensure results directory exists
results_file.parent.mkdir(parents=True, exist_ok=True)

# Warmup phase
print("Starting warmup for 60 seconds...")
warmup_end = time.time() + 60
query_files = sorted(glob.glob("./queries/*.sparql"))

while time.time() < warmup_end:
    for qf in query_files:
        with open(qf, "r") as f:
            query = f.read()
        params = {"query": query}
        requests.get(
            query_url,
            params=params,
            headers={"Accept": "application/sparql-results+json"},
            timeout=60,
        )
        if time.time() >= warmup_end:
            break
print("Warmup complete.")

# Timed execution phase
all_query_files = sorted(glob.glob("./queries/*.sparql"))
with open(results_file, "w", newline="") as rf:
    writer = csv.writer(rf)
    writer.writerow(["query_file", "duration_seconds", "num_results"])
    for qf in all_query_files:
        print(f"Running query: {qf}")

        with open(qf, "r") as f:
            query = f.read()

        params = {"query": query}

        start_time = time.time()
        response = requests.get(
            query_url,
            params=params,
            headers={"Accept": "application/sparql-results+json"},
            timeout=300,
        )
        elapsed = time.time() - start_time

        try:
            data = response.json()
            num_results = len(data.get("results", {}).get("bindings", []))
        except json.JSONDecodeError:
            num_results = 0

        writer.writerow(
            [Path(qf).name.replace(".sparql", ""), f"{elapsed:.3f}", num_results]
        )
        print(f"Total: {elapsed:.3f}s | Results: {num_results}")
