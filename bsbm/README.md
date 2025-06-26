BSBM
====

The [Berlin SPARQL Benchmark (BSBM)](http://wbsg.informatik.uni-mannheim.de/bizer/berlinsparqlbenchmark/) is a simple SPARQL benchmark.

It provides a dataset generator and multiple sets of queries grouped by "use cases".

This part of the benchmark suite is based on [Oxigraph](https://github.com/oxigraph/oxigraph)'s benchmarks.

## Results

We compare here the current RDF Fusion version with existing SPARQL implementations.

The dataset used in the following charts is generated with 100k "products" (see [its spec](http://wbsg.informatik.uni-mannheim.de/bizer/berlinsparqlbenchmark/spec/Dataset/index.html)).
It leads to the creation of 35M triples.
The tests have been executed with a concurrency factor of 16 (i.e. at most 16 queries are sent at the same time to the server).

Beware, the graph *y* axis is in log scale to properly display on the same graph systems with very different speed behaviors.

### Explore
The [explore use case](http://wbsg.informatik.uni-mannheim.de/bizer/berlinsparqlbenchmark/spec/ExploreUseCase/index.html) is composed of 11 queries that do simple data retrieval.

Query 6 existed in previous versions of the benchmark but is now removed.

### Explore and Update
The [explore and update use case](http://wbsg.informatik.uni-mannheim.de/bizer/berlinsparqlbenchmark/spec/index.html#usecase_explore_and_update) is composed of the 2 operations of the [update use case](http://wbsg.informatik.uni-mannheim.de/bizer/berlinsparqlbenchmark/spec/UpdateUseCase/index.html) (`INSERT DATA` and `DELETE WHERE`) and the 11 queries of the [explore use case](http://wbsg.informatik.uni-mannheim.de/bizer/berlinsparqlbenchmark/spec/ExploreUseCase/index.html).

The first two elements (1 and 2) are the 2 updates and the others (3 to 14) are the 11 queries.

<!--
### Business Intelligence
The [business intelligence use case](http://wbsg.informatik.uni-mannheim.de/bizer/berlinsparqlbenchmark/spec/BusinessIntelligenceUseCase/index.html) is composed of 8 complex analytics queries.

Query 4 seems to be failing on Virtuoso and query 5 on Blazegraph and GraphDB.

Oxigraph is still too slow to evaluate most of the queries.
It will be added to the graph after enough optimizations are done.

![explore use case results](bsbm.businessIntelligence.svg)
-->

## How to reproduce the benchmark

The code of the benchmark is in the `bsbm-tools` submodule.
You should pull it with a `git submodule update` before running the benchmark.

To run the benchmark for RDF Fusion run `bash bsbm_rdf_fusion.sh`.
It will compile the current Oxigraph code and run the benchmark against it.
You can tweak the number of products in the dataset and the number of concurrent requests using the environment variables at the beginning of `bsbm_oxigraph.sh`.

To generate the plots run `python3 bsbsm-plot.py`.

Scripts are also provided for the other systems.
