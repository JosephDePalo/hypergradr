#!/bin/bash

lines=()
while IFS= read -r line; do
  lines+=("$line")
done <"$1"

for name in "${lines[@]}"; do
  namecode=$(echo "$name" | tr '[:upper:]' '[:lower:]' | tr -d ' ,')
  echo "GRADING '$name'"
  poetry run python -m hypergradr --config config.toml -s "$name" update \
    -C -G \
    -f "f25-reports/f25-reports-nibadder/${namecode}_nibadder_report.txt" \
    -f "f25-reports/f25-reports-nibmux/${namecode}_nibmux_report.txt"
done
