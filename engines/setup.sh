#!/usr/bin/env bash

# setup.sh: Engine-specific setup script for SPARQL engines
# This script is called before running the benchmark 'prepare' step.
# It performs engine-specific setup, such as creating repositories.

# We may improve upon this hack in the future :)

set -e

ENGINE_NAME="$1"

case "$ENGINE_NAME" in
  rdf4j-*)
    echo "Setting up RDF4J repository for engine: $ENGINE_NAME"
    curl -f -X PUT http://localhost:8080/rdf4j-server/repositories/bench \
      -H 'Content-Type:text/turtle' \
      -d '
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix rep: <http://www.openrdf.org/config/repository#>.
@prefix sr: <http://www.openrdf.org/config/repository/sail#>.
@prefix sail: <http://www.openrdf.org/config/sail#>.

[] a rep:Repository ;
  rep:repositoryID "bench" ;
  rdfs:label "BSBM" ;
  rep:repositoryImpl [
    rep:repositoryType "openrdf:SailRepository" ;
    sr:sailImpl [
      sail:sailType "rdf4j:MemoryStore"
    ]
  ] .
'
    sleep 5  # Wait for the repository to be created
    ;;
  *)
    echo "No setup defined for engine: $ENGINE_NAME. Skipping."
    ;;
esac
