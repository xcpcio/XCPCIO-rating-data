import json
import sys
import math
import logging
import os
from shutil import copyfile, rmtree, make_archive
from time import strftime, localtime, time
import argparse
import requests

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

def json_fetch(path):
    while True:
        r = requests.get(path)
        if r.status_code == 200:
            return json.loads(r.text)

def get_path(path, filename):
    return '/'.join([host_prefix, path, filename])

def json_fetch_all(path):
    config = json_fetch(get_path(path, 'config.json'))
    run = json_fetch(get_path(path, 'run.json'))
    team = json_fetch(get_path(path, 'team.json'))
    return config, run, team

parser = argparse.ArgumentParser(description='Get Contest Rank.')
parser.add_argument('-p', '--path', type=str, help='path of contest')
parser.add_argument('-o', '--output', type=str, help='path of output')
args = parser.parse_args()

host_prefix = 'https://raw.githubusercontent.com/XCPCIO/XCPCIO-board-data/gh-pages/data'

config, run, team = json_fetch_all(args.path)

rating_info = {}
rating_info['contestName'] = config['contest_name']
rating_info['endTime'] = config['end_time']
rating_info['link'] = 'https://board.xcpcio.com/' + args.path
rating_info['teams'] = []

penalty = config['penalty']
group = []

if 'group' in config.keys():
    group = config['group']

for k in team.keys():
    team[k]['problem'] = [0] * len(config['problem_id'])
    team[k]['solved'] = 0
    team[k]['time'] = 0

def Correct(status):
    _status = status.lower()
    return _status in ['correct', 'ac', 'accepted']

def IgnoreStatus(status):
    _status = status.lower()
    return _status in ['ce', 'pe']

run.sort(key=lambda e:(e['timestamp']))

for i in range(len(run)):
    _run = run[i]
    t_id = str(_run['team_id'])
    p_id = int(_run['problem_id'])
    if team[t_id]['problem'][p_id] >= 0 and Correct(_run['status']):
        team[t_id]['solved'] += 1
        team[t_id]['time'] += _run['timestamp'] + penalty * team[t_id]['problem'][p_id]
        team[t_id]['problem'][p_id] = -1
    elif not IgnoreStatus(_run['status']):
        team[t_id]['problem'][p_id] += 1

_team = []

for k in team.keys():
    _team.append(team[k])

_team.sort(key=lambda e:(-e['solved'], e['time'], e['name']))

for i in range(len(_team)):
    __team = _team[i]
    name = ''
    info = []
    if 'name' in __team.keys():
        info.append(__team['name'].strip())
        name = __team['name'].strip()
    for g in group.keys():
        if g in __team.keys():
            info.append(group[g])
    members = []
    if 'members' in __team.keys():
        members = __team['members']
        for j in range(len(members)):
            members[j] = members[j].strip()
    item = {
        'handle': ', '.join(members),
        'organization': '',
        'rank': i + 1,
        'solved': __team['solved'],
        'time': __team['time'],
        'info': ', '.join(info),
        'teamName': name
    }
    if 'organization' in __team.keys():
        item['organization'] = __team['organization'].strip()
    rating_info['teams'].append(item)
    
output(args.output, rating_info)