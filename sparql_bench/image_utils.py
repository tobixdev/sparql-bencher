import subprocess
import logging
from typing import Optional
from .config import BuildConfig
import os
import yaml
import hashlib
from .command_runner import CommandRunner

CACHE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "work", "cache.yml"
)

# Instantiate a global command runner for this module
command_runner = CommandRunner()


def _load_cache():
    if not os.path.exists(CACHE_PATH):
        return {}
    with open(CACHE_PATH, "r") as f:
        try:
            return yaml.safe_load(f) or {}
        except Exception:
            return {}


def _save_cache(cache):
    try:
        with open(CACHE_PATH, "w") as f:
            yaml.safe_dump(cache, f)
        logging.info(f"Cache saved to {CACHE_PATH} with keys: {list(cache.keys())}")
    except Exception as e:
        logging.error(f"Failed to save cache to {CACHE_PATH}: {e}")


def _config_hash(config) -> str:
    # Deterministically hash the config dict
    config_bytes = yaml.safe_dump(config, sort_keys=True).encode("utf-8")
    return hashlib.sha256(config_bytes).hexdigest()


def clear_image_cache():
    """
    Clears the image cache file.
    """
    if os.path.exists(CACHE_PATH):
        os.remove(CACHE_PATH)
        logging.info(f"Cache cleared: {CACHE_PATH}")
    else:
        logging.info("No cache file to clear.")


def get_cached_image_id(name, config):
    """
    Returns the cached image id for the given name and config, or None if not cached or hash mismatch.
    """
    cache = _load_cache()
    h = _config_hash(config)
    entry = cache.get(name)
    if entry and entry.get("hash") == h:
        return entry.get("image_id")
    return None


def set_cached_image_id(name, config, image_id):
    cache = _load_cache()
    h = _config_hash(config)
    cache[name] = {"hash": h, "image_id": image_id}
    logging.info(f"Setting cache for {name}: hash={h}, image_id={image_id}")
    _save_cache(cache)


def pull_image(name: str, image: str) -> str:
    """
    Pull a container image using Podman.
    Returns the image name.
    """

    cached_id = get_cached_image_id(name, {image: image})
    if cached_id:
        logging.info(f"Using cached image id for {name}: {cached_id}")
        return cached_id

    cmd = ["podman"]
    cmd += ["pull", image]
    logging.info(f"Pulling image with command: {' '.join(cmd)}")
    try:
        command_runner.run(cmd, check=True)
        logging.info("Image pulled successfully.")
        set_cached_image_id(name, {image: image}, image)
        return image
    except subprocess.CalledProcessError as e:
        logging.error(f"Image pull failed: {e}")
        raise


def build_image(name: str, build_config: BuildConfig) -> str:
    """
    Build a container image using Podman from the given BuildConfig.
    Uses a cache to avoid rebuilding if possible.
    Returns the image tag or ID.
    """
    config_dict = (
        build_config.model_dump()
        if hasattr(build_config, "model_dump")
        else build_config.__dict__
    )

    cached_id = get_cached_image_id(name, config_dict)
    if cached_id:
        logging.info(f"Using cached image id for {name}: {cached_id}")
        return cached_id

    cmd = ["podman"]
    cmd += ["build"]
    cmd += ["--no-cache"]

    if build_config.args:
        for arg in build_config.args:
            cmd += ["--build-arg", arg]
    cmd += [build_config.context]
    logging.info(f"Building image with command: {' '.join(cmd)}")
    try:
        result = command_runner.run(cmd, check=True, capture_output=True, text=True)
        logging.info("Image built successfully.")

        image_id = result.stdout.splitlines()[-1].strip()
        set_cached_image_id(name, config_dict, image_id)
        return image_id
    except subprocess.CalledProcessError as e:
        logging.error(f"Image build failed: {e}\n{e.stderr}")
        raise


def obtain_image(name, image_config):
    if image_config.image:
        return pull_image(name, image_config.image)
    elif image_config.build:
        return build_image(name, image_config.build)
    else:
        raise ValueError(f"'{image_config.name}' has neither image nor build config.")


def check_unique_names(config):
    """
    Checks that all engine and benchmark names are unique in the config.
    Raises ValueError if duplicates are found.
    """
    names = set()
    duplicates = set()
    for section in (getattr(config, "engines", []), getattr(config, "benchmarks", [])):
        for item in section:
            name = getattr(item, "name", None)
            if name:
                if name in names:
                    duplicates.add(name)
                names.add(name)
    if duplicates:
        raise ValueError(
            f"Duplicate engine/benchmark names found: {', '.join(duplicates)}"
        )


def create_pod(pod_name: str, port: Optional[int] = None) -> None:
    """
    Create a pod with the given name and optional port mappings.
    """
    cmd = ["podman", "pod", "create", "--name", pod_name]
    if port:
        cmd += ["-p", f"{port}:{port}"]
    logging.info(f"Creating pod with command: {' '.join(cmd)}")
    try:
        command_runner.run(cmd, check=True)
        logging.info(f"Pod '{pod_name}' created.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Pod creation failed: {e}")
        raise


def remove_pod(pod_name: str) -> None:
    """
    Remove the specified pod and all its containers.
    """
    try:
        command_runner.run(["podman", "pod", "rm", "-f", pod_name], check=True)
        logging.info(f"Pod '{pod_name}' removed.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Pod removal failed: {e}")
        raise
