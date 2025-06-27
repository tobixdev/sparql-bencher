#!/usr/bin/env bash

set -eu

usage() {
  echo "Usage: $0 {prepare | execute} <engine> {explore | explore-and-update | business-intelligence} <dataset_size> <parallelism> <query_url> <update_url> <upload_url>"
  echo "  <engine>: Identifier for the engine"
  echo "  <dataset_size>: Size of the dataset (e.g., 1000, 10000)"
  echo "  <parallelism>: Number of parallel clients/threads (e.g., 1, 4, 8)"
  echo "  <query_url>: URL of the query endpoint"
  echo "  <update_url>: URL of the update endpoint"
  echo "  <upload_url>: URL for uploading data"
  exit 1
}

if [[ $# -lt 2 ]]; then
  usage
fi

DATASET_SIZE=$(cat /bsbm/number_of_products.txt)

COMMAND="$1"

case "$COMMAND" in
  prepare)
    ENGINE="$2"
    USE_CASE="$3"
    PARALLELISM="$4"
    QUERY_URL="$5"
    UPDATE_URL="$6"
    UPLOAD_URL="$7"

    curl -X POST -T "./data/explore-${DATASET_SIZE}.nt" -H "content-type: application/n-triples" $UPLOAD_URL
    ;;
  execute)
    ENGINE="$2"
    USE_CASE="$3"
    PARALLELISM="$4"
    QUERY_URL="$5"
    UPDATE_URL="$6"
    UPLOAD_URL="$7"

    mkdir -p results
    cd bsbm-tools

    RESULTS_FILE_NAME="bsbm.${USE_CASE}.${ENGINE}.${DATASET_SIZE}.${PARALLELISM}.xml"
    RESULTS_FILE="../results/$RESULTS_FILE_NAME"

    case "$USE_CASE" in
      explore)
        ./testdriver -idir "../data" -mt "${PARALLELISM}" -ucf usecases/explore/sparql.txt -o $RESULTS_FILE $QUERY_URL
        ;;
      explore-and-update)
        ./testdriver -idir "../data" -mt "${PARALLELISM}" -ucf usecases/exploreAndUpdate/sparql.txt -o $RESULTS_FILE $QUERY_URL -u $UPDATE_URL -udataset "explore-update-${DATASET_SIZE}.nt"
        ;;
      business-intelligence)
        ./testdriver -idir "../data" -mt "${PARALLELISM}" -ucf usecases/businessIntelligence/sparql.txt -o $RESULTS_FILE $QUERY_URL
        ;;
      *)
        echo "Unknown usecase: $USE_CASE"
        usage
        ;;
    esac
    echo "finished"

    mkdir -p "/results/${USE_CASE}"
    cp $RESULTS_FILE "/results/${USE_CASE}/${ENGINE}.xml"

    ;;
  analyze)
    USE_CASE="$2"
    PARALLELISM="$3"

    # Assuming analyze.py is a script that processes the results XML file
    python3 /bsbm/analyze.py "/results" $USE_CASE
    ;;

  *)
    echo "Unknown command: $COMMAND"
    usage
    ;;
esac
