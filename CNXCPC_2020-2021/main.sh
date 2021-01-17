#! /bin/bash

set -x

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

echo $SHELL_FOLDER

i_list=(
    'ccpc-qinhuangdao.json'
    'ccpc-weihai.json'
    'ccpc-mianyang.json'
    'ccpc-changchun.json'
    'icpc-shanghai.json'
    'icpc-nanjing.json'
    'icpc-jinan.json'
)

for i in ${i_list[@]}
do
    echo $SHELL_FOLDER/raw/$i
    python3 $SHELL_FOLDER/../rating.py -i=$SHELL_FOLDER/raw/$i -o=$SHELL_FOLDER/rating.json
done

