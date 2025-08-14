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

DATASET_SIZE=16

COMMAND="$1"

case "$COMMAND" in
  prepare)
    ENGINE="$2"
    USE_CASE="$3"
    QUERY_URL="$4"
    UPDATE_URL="$5"
    UPLOAD_URL="$6"

    curl -X POST -T "./windfarm.n3" -H "content-type: application/n3" $UPLOAD_URL
    curl -X POST -T "./timeseries.n3" -H "content-type: application/n3" $UPLOAD_URL

    ;;
  execute)
    ENGINE="$2"
    USE_CASE="$3"
    QUERY_URL="$4"
    UPDATE_URL="$5"
    UPLOAD_URL="$6"

    RESULTS_FILE_NAME="wind_farm.${ENGINE}.${DATASET_SIZE}.txt"
    RESULTS_FILE="../results/$RESULTS_FILE_NAME"

    ./runner.sh $RESULTS_FILE $QUERY_URL

    echo "finished"

    mkdir -p "/results/${USE_CASE}"
    cp $RESULTS_FILE "/results/${USE_CASE}/${ENGINE}.xml"

    ;;
  analyze)
    USE_CASE="$2"

    python3 /windfarm/analyze.py "/results/${USE_CASE}"

    ;;

  *)
    echo "Unknown command: $COMMAND"
    usage
    ;;
esac
