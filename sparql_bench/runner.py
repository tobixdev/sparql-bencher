"""
Orchestrator for running SPARQL engine benchmarks using Podman.
"""

import logging
import os
import random
import time

from .command_runner import CommandRunner
from .config import BencherConfig
from .container_utils import run_container
from .image_utils import create_pod, obtain_image, remove_pod


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
    for benchmark in config.benchmarks:
        benchmark_image = benchmark_images[benchmark.name]
        pod_name = "sparql-bench"

        for use_case in benchmark.use_cases:
            logging.info(f"\n=== Running {benchmark.name} on {engine.name} ===")

            for engine in config.engines:
                logging.info(f"Running use case: {use_case.name}")
                engine_image = engine_images[engine.name]

                logging.info(
                    f"Creating pod '{pod_name}' for benchmark '{benchmark.name}'"
                )
                create_pod(pod_name, engine.port)

                try:
                    # Start engine container
                    logging.info(f"Starting engine container for {engine.name}")

                    run_container(
                        image=engine_image,
                        pod_name=pod_name,
                        name=f"{engine.name.lower()}-{random.randint(1000, 9999)}",
                        args=engine.run.args,
                        env=engine.run.env,
                        detach=True,
                    )
                    time.sleep(engine.boot_time_s)

                    # Engine-specific setup step
                    setup_script = os.path.join(
                        os.path.dirname(__file__), "..", "engines", "setup.sh"
                    )
                    if os.path.isfile(setup_script):
                        command_runner = CommandRunner()
                        command_runner.run([setup_script, engine.name], check=True)
                    else:
                        logging.warning(f"Setup script not found: {setup_script}")

                    # Run benchmark prepare step
                    logging.info(
                        f"Running prepare step for benchmark '{benchmark.name}'"
                    )
                    run_container(
                        image=benchmark_image,
                        pod_name=pod_name,
                        args=[
                            "prepare",
                            engine.name,
                            *use_case.command_args,
                            engine.query_url,
                            engine.update_url,
                            engine.upload_url,
                        ],
                    )

                    # Run benchmark execute step
                    logging.info(
                        f"Running execute step for benchmark '{benchmark.name}'"
                    )

                    # Define results directory for this benchmark/usecase/engine
                    results_dir = os.path.abspath(
                        os.path.join(
                            os.path.dirname(__file__),
                            "..",
                            "work",
                            "results",
                            use_case.name,
                        )
                    )
                    os.makedirs(results_dir, exist_ok=True)
                    run_container(
                        image=benchmark_image,
                        pod_name=pod_name,
                        volumes={results_dir: "/results"},
                        args=[
                            "execute",
                            engine.name,
                            *use_case.command_args,
                            engine.query_url,
                            engine.update_url,
                            engine.upload_url,
                        ],
                    )

                except Exception as e:
                    logging.error(f"Error running benchmark: {e}")
                    raise
                finally:
                    logging.info(f"Cleaning up pod '{pod_name}'")
                    remove_pod(pod_name)

            # Analyze results of the use case
            run_container(
                image=benchmark_image,
                volumes={results_dir: "/results"},
                args=[
                    "analyze",
                    *use_case.command_args,
                ],
            )


# Instantiate a global command runner for this module (if needed for future direct calls)
command_runner = CommandRunner()
