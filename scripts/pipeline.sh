#!/bin/bash

namespace=${1:-default}

mkdir -p metrics

kubectl top pods --all-namespaces --no-headers > "metrics/metric.csv"

python src/plugin.py

echo "Convirtiendo archivo json en csv"

cd fixtures

cat metrics.json | jq '.[] | join(",")' > metrics.csv
