#! /bin/bash

set -x

all_dir_list=(
    'CNXCPC_2020-2021'
)

dir_list=(
    'CNXCPC_2020-2021'
)

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

mkdir site

for dir in ${dir_list[@]}
do
    dir=data/$dir
    echo $dir
    bash ./$dir/main.sh
    mkdir site/$dir
    cp ./$dir/rating.json site/$dir/rating.json
    cp ./$dir/config.json site/$dir/config.json
done

[ -f list.json ] rm -f list.json
echo [] > list.json
for dir in ${all_dir_list[@]}
do
    dir=data/$dir
    python3 get_info.py -i=$SHELL_FOLDER/$dir/config.json -o=$SHELL_FOLDER/list.json -d=$dir
done

cp list.json site/list.json