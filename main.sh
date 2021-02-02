#! /bin/bash

set -x

all_dir_list=(
    'CNXCPC_2020-2021'
)

dir_list=(
    'CNXCPC_2020-2021'
)

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

[ -d $SHELL_FOLDER/site ] && rm -rf $SHELL_FOLDER/site

if [ ! -d $SHELL_FOLDER/site ]; then
  mkdir $SHELL_FOLDER/site
fi

for dir in ${dir_list[@]}
do
    bash $SHELL_FOLDER/data/$dir/main.sh
    mkdir $SHELL_FOLDER/site/$dir
    cp $SHELL_FOLDER/data/$dir/rating.json $SHELL_FOLDER/site/$dir/rating.json
    cp $SHELL_FOLDER/data/$dir/config.json $SHELL_FOLDERsite/$dir/config.json
done

[ -f list.json ] && rm -f list.json
echo [] > list.json
for dir in ${all_dir_list[@]}
do
<<<<<<< HEAD
    python3 $SHELL_FOLDER/get_info.py -i=$SHELL_FOLDER/data/$dir/config.json -o=$SHELL_FOLDER/list.json -d=$dir
=======
    python3 get_info.py -i=$SHELL_FOLDER/data/$dir/config.json -o=$SHELL_FOLDER/list.json -d=$dir
>>>>>>> 1c822e77cf1170d64319b1b0be90f7a64ef1342c
done

cp $SHELL_FOLDER/list.json $SHELL_FOLDER/site/list.json