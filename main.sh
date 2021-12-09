#! /bin/bash

set -x

pip3 install -U -r requirements.txt

all_dir_list=(
    'cnxcpc-2020-2021'
)

dir_list=(
    'cnxcpc-2020-2021'
)

SHELL_FOLDER=$(dirname "$(realpath "$0")")

[ -d "$SHELL_FOLDER/site" ] && rm -rf "$SHELL_FOLDER/site"

if [ ! -d "$SHELL_FOLDER/site" ]; then
    mkdir "$SHELL_FOLDER/site"
fi

for dir in "${dir_list[@]}"; do
    bash "$SHELL_FOLDER/data/$dir/main.sh"
    mkdir "$SHELL_FOLDER/site/$dir"
    cp "$SHELL_FOLDER/data/$dir/rating.json" "$SHELL_FOLDER/site/$dir/rating.json"
    cp "$SHELL_FOLDER/data/$dir/config.json" "$SHELL_FOLDER/site/$dir/config.json"
done

[ -f list.json ] && rm -f list.json
echo [] >list.json
for dir in "${all_dir_list[@]}"; do
    python3 "$SHELL_FOLDER/get_info.py" "-i=$SHELL_FOLDER/data/$dir/config.json" "-o=$SHELL_FOLDER/list.json" "-d=$dir"
done

cp "$SHELL_FOLDER/list.json" "$SHELL_FOLDER/site/list.json"
