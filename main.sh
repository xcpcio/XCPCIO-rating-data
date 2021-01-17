#! /bin/bash

dir_list=(
    'CNXCPC_2020-2021'
)

set -x

mkdir site

for dir in ${dir_list[@]}
do
    echo $dir
    bash ./$dir/main.sh
    mkdir site/$dir
    cp ./$dir/rating.json site/$dir/rating.json
    cp ./$dir/config.json site/$dir/config.json
done
