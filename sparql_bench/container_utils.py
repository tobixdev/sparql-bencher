import subprocess
import logging
from typing import Optional, Dict
from .command_runner import CommandRunner

command_runner = CommandRunner()


def run_container_in_pod(
    pod_name: str,
    image: str,
    name: Optional[str] = None,
    volumes: Optional[Dict[str, str]] = None,
    args: list = None,
    detach: bool = False,
) -> str:
    """
    Run a container in the specified pod.
    """
    cmd = ["podman", "run", "--rm", "--pod", pod_name]

    if name:
        cmd += ["--name", name]
    else:
        name = f"{image}-container"
    
    if volumes:
        for host_path, container_path in volumes.items():
            cmd += ["--volume", f"{host_path}:{container_path}"]

    if detach:
        cmd.append("-d")

    cmd.append(image)

    if args:
        cmd += args

    logging.info(f"Running container with command: {' '.join(cmd)}")
    try:
        result = command_runner.run(cmd, stdout=subprocess.PIPE, check=True)
        logging.info(f"Container '{name}' started in pod '{pod_name}'.")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Container run failed: {e}")
        raise
