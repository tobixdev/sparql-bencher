"""
Orchestrator for running SPARQL engine benchmarks using Podman.
"""

import logging
import random
from .config import BencherConfig
from .image_utils import create_pod, obtain_image, remove_pod
from .container_utils import run_container_in_pod
import time
import subprocess


def run_benchmarks(config: BencherConfig):
    logging.basicConfig(level=logging.INFO)
    engine_images = {}
    benchmark_images = {}

    # Build or pull engine images
    for engine in config.engines:
        engine_images[engine.name] = obtain_image(engine.name, engine)

    # Build or pull benchmark images
    for benchmark in config.benchmarks:
        benchmark_images[benchmark.name] = obtain_image(benchmark.name, benchmark)

    # For each combination, create and run containers
    for engine in config.engines:
        for benchmark in config.benchmarks:
            logging.info(f"\n=== Running {benchmark.name} on {engine.name} ===")
            engine_image = engine_images[engine.name]
            benchmark_image = benchmark_images[benchmark.name]

            pod_name = "sparql-bench"

            for use_case in benchmark.use_cases:
                logging.info(f"Running use case: {use_case.name}")
                
                logging.info(f"Creating pod '{pod_name}' for benchmark '{benchmark.name}'")
                create_pod(pod_name)

                try:    
                    # Start engine container
                    logging.info(f"Starting engine container for {engine.name}")
                    engine_container = run_container_in_pod(
                        pod_name=pod_name,
                        image=engine_image,
                        name=f"{engine.name.lower()}-{random.randint(1000, 9999)}",
                        detach=True,
                    )
                    time.sleep(2)  # Give engine time to start

                    # Run benchmark prepare step
                    logging.info(
                        f"Running prepare step for benchmark '{benchmark.name}'"
                    )
                    run_container_in_pod(
                        pod_name=pod_name,
                        image=benchmark_image,
                        args=[
                            "prepare",
                            *use_case.command_args,
                        ],
                    )

                    # Run benchmark execute step
                    logging.info(
                        f"Running execute step for benchmark '{benchmark.name}'"
                    )
                    run_container_in_pod(
                        pod_name=pod_name,
                        image=benchmark_image,
                        args=[
                            "execute",
                            *use_case.command_args,
                        ],
                    )
                    
                except Exception as e:
                    logging.error(f"Error running benchmark: {e}")
                    raise
                finally: 
                    logging.info(f"Cleaning up pod '{pod_name}'")
                    remove_pod(pod_name)
