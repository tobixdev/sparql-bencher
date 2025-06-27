"""
Configuration loader and validator for SPARQL Bencher using pydantic.
"""
import yaml
from pydantic import BaseModel, ValidationError, field_validator, model_validator
from typing import List, Optional

class BuildConfig(BaseModel):
    context: str
    args: Optional[List[str]] = None

class EngineRunConfig(BaseModel):
    args: Optional[List[str]] = None

class EngineConfig(BaseModel):
    name: str
    image: Optional[str] = None
    build: Optional[BuildConfig] = None
    run: Optional[EngineRunConfig] = None
    boot_time_s: int = 5
    query_url: str = None
    update_url: str = None
    upload_url: str = None
    port: Optional[int] = None

    @model_validator(mode="after")
    def check_image_or_build(self):
        if (self.image is None) == (self.build is None):
            raise ValueError('Exactly one of image or build can be specified for EngineConfig')
        return self

class UseCaseConfig(BaseModel):
    name: str
    command_args: List[str]

class BenchmarkConfig(BaseModel):
    name: str
    image: Optional[str] = None
    build: Optional[BuildConfig] = None
    use_cases: Optional[List[UseCaseConfig]] = None
    number_of_products: Optional[int] = None

    @model_validator(mode="after")
    def check_image_or_build(self):
        if (self.image is None) == (self.build is None):
            raise ValueError('Exactly one of image or build must be specified for BenchmarkConfig')
        return self

class BencherConfig(BaseModel):
    engines: List[EngineConfig]
    benchmarks: List[BenchmarkConfig]

    @model_validator(mode="after")
    def check_unique_names(self):
        names = set()
        duplicates = set()
        for engine in self.engines:
            if engine.name in names:
                duplicates.add(engine.name)
            names.add(engine.name)
        for benchmark in self.benchmarks:
            if benchmark.name in names:
                duplicates.add(benchmark.name)
            names.add(benchmark.name)
        if duplicates:
            raise ValueError(f"Duplicate engine/benchmark names found: {', '.join(duplicates)}")
        return self

def load_config(path: str) -> BencherConfig:
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    try:
        return BencherConfig(**data)
    except ValidationError as e:
        print("Configuration validation error:")
        print(e)
        raise
