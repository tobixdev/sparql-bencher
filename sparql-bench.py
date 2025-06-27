#!/usr/bin/env python3
"""
Main entry point for SPARQL Bencher.
Loads configuration, orchestrates Podman containers, and runs benchmarks.
"""
import os
import sys
from sparql_bench.config import load_config
from sparql_bench.runner import run_benchmarks

def main():
    if len(sys.argv) < 2:
        config_path = "default.yaml"
        print("No config file specified, using 'default.yaml'.")
    else:
        config_path = sys.argv[1]
    config = load_config(config_path)
    
    if not os.path.exists("work"):
        os.mkdir("work")
    
    if os.path.exists("work/command.log"):
        os.remove("work/command.log")
        
    run_benchmarks(config)

if __name__ == "__main__":
    main()
