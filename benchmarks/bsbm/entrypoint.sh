#!/usr/bin/env bash

set -eu

usage() {
  echo "Usage: $0 {prepare | execute} <engine> {explore | explore-and-update | business-intelligence} <dataset_size> <parallelism> <endpoint_url>"
  echo "  <engine>: Identifier for the engine"
  echo "  <dataset_size>: Size of the dataset (e.g., 1000, 10000)"
  echo "  <parallelism>: Number of parallel clients/threads (e.g., 1, 4, 8)"
  echo "  <endpoint_url>: URL of the SPARQL endpoint (e.g., http://127.0.0.1:7878)"
  exit 1
}

if [[ $# -lt 2 ]]; then
  usage
fi

COMMAND="$1"
ENGINE="$2"
USECASE="$3"
DATASET_SIZE="$4"
PARALLELISM="$5"
ENDPOINT_URL="$6"

case "$COMMAND" in
  prepare)
    curl -X POST -T "./data/explore-${DATASET_SIZE}.nt" -H "content-type: application/n-triples" "${ENDPOINT_URL}/store?no_transaction"
    ;;
  execute)
    mkdir -p results
    cd bsbm-tools

    RESULTS_FILE_NAME="bsbm.${USECASE}.${ENGINE}.${DATASET_SIZE}.${PARALLELISM}.xml"
    RESULTS_FILE="../results/$RESULTS_FILE_NAME"

    case "$USECASE" in
      explore)
        ./testdriver -idir "../data" -mt "${PARALLELISM}" -ucf usecases/explore/sparql.txt -o $RESULTS_FILE "${ENDPOINT_URL}/query"
        ;;
      explore-and-update)
        ./testdriver -idir "../data" -mt "${PARALLELISM}" -ucf usecases/exploreAndUpdate/sparql.txt -o $RESULTS_FILE "${ENDPOINT_URL}/query" -u "${ENDPOINT_URL}/update" -udataset "explore-update-${DATASET_SIZE}.nt"
        ;;
      business-intelligence)
        ./testdriver -idir "../data" -mt "${PARALLELISM}" -ucf usecases/businessIntelligence/sparql.txt -o $RESULTS_FILE "${ENDPOINT_URL}/query"
        ;;
      *)
        echo "Unknown usecase: $USECASE"
        usage
        ;;
    esac
    echo "finished"
    cp $RESULTS_FILE "/results/$RESULTS_FILE_NAME"
    ;;
  *)
    echo "Unknown command: $COMMAND"
    usage
    ;;
esac
