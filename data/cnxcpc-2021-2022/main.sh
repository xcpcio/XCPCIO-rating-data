#! /bin/bash

set -x

SHELL_FOLDER=$(dirname "$(realpath "$0")")

echo "$SHELL_FOLDER"

i_list=(
    'ccpc/7th/guilin'
    'ccpc/7th/guangzhou'
    'icpc/46th/jinan'
    'ccpc/7th/weihai'
    'ccpc/7th/harbin'
    'icpc/46th/nanjing'
)

[ -d "$SHELL_FOLDER/raw" ] && rm -rf "$SHELL_FOLDER/raw"

if [ ! -d "$SHELL_FOLDER/raw" ]; then
    mkdir "$SHELL_FOLDER/raw"
fi

[ -f rating.json ] && rm -f rating.json

for i in "${i_list[@]}"; do
    out=$(echo "${i}" | sed 's/\//-/g')
    python3 "$SHELL_FOLDER/../../fetch_from_xcpcio_board.py" "-p=${i}" "-o=$SHELL_FOLDER/raw/${out}.json"
done

for i in "${i_list[@]}"; do
    echo "$SHELL_FOLDER/raw/${out}"
    out=$(echo "${i}" | sed 's/\//-/g')
    python3 "$SHELL_FOLDER/../../rating.py" "-i=$SHELL_FOLDER/raw/${out}.json" "-o=$SHELL_FOLDER/rating.json" -b=2300
done
