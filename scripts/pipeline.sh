#!/bin/bash

namespace=${1:-default}

mkdir -p metrics

kubectl top pods --all-namespaces --no-headers > "metrics/metric.csv"

