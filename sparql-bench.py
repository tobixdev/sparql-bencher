#!/usr/bin/env python3
"""
Main entry point for SPARQL Bencher.
Loads configuration, orchestrates Podman containers, and runs benchmarks.
"""
import os
import shutil
from argparse import ArgumentParser

from sparql_bench.config import load_config
from sparql_bench.runner import run_benchmarks


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "config_path",
        help="The path the YAML configuration file. If none is specified, 'default.yaml' is used.",
        type=str,
        default="default.yaml",
        nargs="?",
    )
    args = parser.parse_args()
    config = load_config(args.config_path)

    if not os.path.exists("work"):
        os.mkdir("work")

    if os.path.exists("work/command.log"):
        os.remove("work/command.log")

    if os.path.exists("work/results"):
        shutil.rmtree("work/results")

    run_benchmarks(config)


if __name__ == "__main__":
    main()
