#!/bin/bash

namespace=${1:-default}

mkdir -p metrics

kubectl top pods --all-namespaces --no-headers > "metrics/metric.csv"

python src/plugin.py

echo "Convirtiendo archivo json en csv"

# Ubicandonos a la carptea fixtures para aplicar directamente en esa carpeta los comandos de formateo
cd fixtures

cat metrics.json | jq -r '(map(keys_unsorted) | add | unique) as $cols | $cols, map(. as $row | $cols | map($row[.]))[] | @csv' > metrics.csv

# Aplicando los test con csvkit

echo "Aplicando tests"
echo "Quitando encabezado"

csvformat -K 1 metrics.csv > out.csv
csvformat -T metrics.csv > metrics_format.csv


rows_header=$(wc -l < metrics.csv)
rows_without_header=$(wc -l < out.csv)
columns=$(awk '{print NF}' metrics_format.csv | sort -nu | tail -n 1)

if [[ "$rows_header" > "$rows_without_header" ]]; then
    echo numero de columnas "$columns"
fi
