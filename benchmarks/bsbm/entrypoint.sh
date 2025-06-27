#!/usr/bin/env bash

set -eu

usage() {
  echo "Usage: $0 {prepare|execute} {explore | explore-and-update | business-intelligence} <name_postfix> <dataset_size> <parallelism> <endpoint_url>"
  echo "  <name_postfix>: Custom string to identify the run (e.g., run1)"
  echo "  <dataset_size>: Size of the dataset (e.g., 1000, 10000)"
  echo "  <parallelism>: Number of parallel clients/threads (e.g., 1, 4, 8)"
  echo "  <endpoint_url>: URL of the SPARQL endpoint (e.g., http://127.0.0.1:7878)"
  exit 1
}

if [[ $# -lt 2 ]]; then
  usage
fi

COMMAND="$1"
USECASE="$2"
NAME_POSTFIX="$3"
DATASET_SIZE="$4"
PARALLELISM="$5"
ENDPOINT_URL="$6"

case "$COMMAND" in
  prepare)
    curl -X POST -T "./data/explore-${DATASET_SIZE}.nt" -H "content-type: application/n-triples" "${ENDPOINT_URL}/store?no_transaction"
    ;;
  execute)
    mkdir results
    cd bsbm-tools
    case "$USECASE" in
      explore)
        ./testdriver -idir "../data" -mt "${PARALLELISM}" -ucf usecases/explore/sparql.txt -o "../results/bsbm.explore.${NAME_POSTFIX}.${DATASET_SIZE}.${PARALLELISM}.xml" "${ENDPOINT_URL}/query"
        ;;
      explore-and-update)
        ./testdriver -idir "../data" -mt "${PARALLELISM}" -ucf usecases/exploreAndUpdate/sparql.txt -o "../results/bsbm.exploreAndUpdate.${NAME_POSTFIX}.${DATASET_SIZE}.${PARALLELISM}.xml" "${ENDPOINT_URL}/query" -u "${ENDPOINT_URL}/update" -udataset "explore-update-${DATASET_SIZE}.nt"
        ;;
      business-intelligence)
        ./testdriver -idir "../data" -mt "${PARALLELISM}" -ucf usecases/businessIntelligence/sparql.txt -o "../results/bsbm.businessIntelligence.${NAME_POSTFIX}.${DATASET_SIZE}.${PARALLELISM}.xml" "${ENDPOINT_URL}/query"
        ;;
      *)
        echo "Unknown usecase: $USECASE"
        usage
        ;;
    esac
    ;;
  *)
    echo "Unknown command: $COMMAND"
    usage
    ;;
esac
