import json
import sys
import math
import logging
import os
from shutil import copyfile, rmtree, make_archive
from time import strftime, localtime, time
import argparse

def ensure_dir(s):
    if not os.path.exists(s):
        os.makedirs(s)

def ensure_no_dir(s):
    if os.path.exists(s):
        rmtree(s)

def json_output(data):
    return json.dumps(data, sort_keys=False, separators=(',', ':'), ensure_ascii=False)

def output(filename, data):
    with open(filename, 'w') as f:
        f.write(json_output(data))

def json_input(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

parser = argparse.ArgumentParser(description='Get Season Info.')
parser.add_argument('-i', '--input', type=str, help='path of input file')
parser.add_argument('-o', '--output', type=str, help='path of output file')
parser.add_argument('-d', '--dir', type=str, help='path of season dir')
args = parser.parse_args()

config = json_input(args.input)
data = json_input(args.output)
data.append({
    'name': config['name'],
    'link': args.dir
})
output(args.output, data)