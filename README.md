SPARQL Bencher
==============

A CLI tool for comparing the performance of SPARQL engines with the primary goal of benchmarking [RDF Fusion](https://github.com/tobixdev/rdf-fusion).

The goals of this tool is twofold:
- Allows creating and managing instances of different SPARQL engines
- Allows preparing and running SPARQL benchmarks

Supported SPARQL Engines:
- [RDF Fusion](https://github.com/tobixdev/rdf-fusion)
- [Oxigraph](https://oxigraph.org/)
- [Jena Fuseki](https://jena.apache.org/documentation/fuseki2/)
- [RDF4J](https://rdf4j.org/)

Benchmarks:
- [Berlin SPARQL Benchmark (BSBM)](http://wifo5-03.informatik.uni-mannheim.de/bizer/berlinsparqlbenchmark/)

## Installation and Basic Usage

To install all Python dependencies we recommend that you use [Poetry](https://python-poetry.org).
After cloning the repository you can create a new Python environment and install missing dependencies by running

```bash
poetry install
```

To get basic usage information call:

```bash
poetry run python sparql-bench.py -h
```

This will print the following lines:
```
usage: sparql-bench.py [-h] config_path

positional arguments:
  config_path  The path the YAML configuration file. If none is specified, 'default.yaml' is used.

options:
  -h, --help   show this help message and exit
```

## Run the Benchmarks

To run the benchmarks run with the default configuration (`default.yaml`) use the following command:

```bash
poetry run python sparql-bench.py
```
