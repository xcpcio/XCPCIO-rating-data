#! /bin/bash

set -x

SHELL_FOLDER=$(dirname "$(realpath "$0")")

echo "$SHELL_FOLDER"

i_list=(
    'ccpc/2020/qinhuangdao'
    'ccpc/2020/weihai'
    'ccpc/2020/mianyang'
    'ccpc/2020/changchun'
    'icpc/2020/shanghai'
    'icpc/2020/nanjing'
    'icpc/2020/jinan'
    'icpc/2020/kunming'
    'ccpc/2020/final'
    'icpc/2020/shenyang'
)

[ -d "$SHELL_FOLDER/raw" ] && rm -rf "$SHELL_FOLDER/raw"

if [ ! -d "$SHELL_FOLDER/raw" ]; then
  mkdir "$SHELL_FOLDER/raw"
fi

[ -f rating.json ] && rm -f rating.json

for i in "${i_list[@]}"
do
    out=$( echo "${i}" | sed 's/\//-/g' ) 
    python3 "$SHELL_FOLDER/../../fetch_from_xcpcio_board.py" "-p=${i}" "-o=$SHELL_FOLDER/raw/${out}.json"
done

for i in "${i_list[@]}"
do
    echo "$SHELL_FOLDER/raw/${out}"
    out=$( echo "${i}" | sed 's/\//-/g' ) 
    python3 "$SHELL_FOLDER/../../rating.py" "-i=$SHELL_FOLDER/raw/${out}.json" "-o=$SHELL_FOLDER/rating.json" -b=2300
done
