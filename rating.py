import json
import sys
import math
import logging
import os
from shutil import copyfile, rmtree, make_archive
from time import strftime, localtime, time
import argparse

class User():
    def __init__(self, rank, old_rating, handle='', official_new_rating=0):
        self.rank = float(rank)
        self.old_rating = int(old_rating)
        self.seed = 1.0
        self.handle = str(handle)
        # official_new_rating: used for validating result
        self.official_new_rating = int(official_new_rating)

class RatingCalculator():
    def __init__(self):
        self.user_list = []

    def cal_p(self, user_a, user_b):
        return 1.0 / (1.0 + pow(10, (user_b.old_rating - user_a.old_rating) / 400.0))

    def get_ex_seed(self, user_list, rating, own_user):
        ex_user = User(0.0, rating)
        result = 1.0
        for user in user_list:
            if user != own_user:
                result += self.cal_p(user, ex_user)
        return result

    def cal_rating(self, user_list, rank, user):
        left = 1
        right = 8000
        while right - left > 1:
            mid = int((left + right) / 2)
            if self.get_ex_seed(user_list, mid, user) < rank:
                right = mid
            else:
                left = mid
        return left

    def calculate(self):
        logger.info(f"Calculate seed")
        # Calculate seed
        for i in range(len(self.user_list)):
            self.user_list[i].seed = 1.0
            for j in range(len(self.user_list)):
                if i != j:
                    self.user_list[i].seed += self.cal_p(
                        self.user_list[j], self.user_list[i])
            # print(self.user_list[i].seed)
        logger.info(f"Calculate initial delta and sum_delta")
        # Calculate initial delta and sum_delta
        sum_delta = 0
        for user in self.user_list:
            user.delta = int(
                (self.cal_rating(self.user_list,
                                 math.sqrt(user.rank * user.seed), user) -
                 user.old_rating) / 2)
            sum_delta += user.delta
        logger.info(f"Calculate first inc")
        # Calculate first inc
        inc = int(-sum_delta / len(self.user_list)) - 1
        for user in self.user_list:
            user.delta += inc
            # print(user.delta)
        logger.info(f"Calculate second inc")
        # Calculate second inc
        self.user_list = sorted(self.user_list,
                                key=lambda x: x.old_rating,
                                reverse=True)
        s = min(len(self.user_list),
                int(4 * round(math.sqrt(len(self.user_list)))))
        sum_s = 0
        for i in range(s):
            sum_s += self.user_list[i].delta
        inc = min(max(int(-sum_s / s), -10), 0)
        logger.info(f"Calculate new rating")
        # Calculate new rating
        for user in self.user_list:
            user.delta += inc
            user.new_rating = user.old_rating + user.delta
            # print(user.new_rating)
        self.user_list = sorted(self.user_list,
                                key=lambda x: x.rank,
                                reverse=False)

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

def calc_rating(history):
    global base
    rating = base
    maxRating = base
    for contest in history:
        rating = contest['newRating']
        maxRating = max(maxRating, contest['newRating'])
    return rating, maxRating

parser = argparse.ArgumentParser(description='Calculate Rating.')
parser.add_argument('-i', '--input', type=str, help='path of input file')
parser.add_argument('-o', '--output', type=str, help='path of output file')
parser.add_argument('-b', '--base', type=int, help="base rating of unrated user")
args = parser.parse_args()

# base rating of unrated user
base = 1500

ensure_dir('log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('log/{}.log'.format(strftime('%Y-%m-%d %H:%M:%S', localtime(time()))))
console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(console)
logger.addHandler(handler)

if args.base: base = args.base
logger.info(f"input: {args.input}")
logger.info(f"output: {args.output}")
logger.info(f"base rating: {base}")

if not args.input or not args.output:
    logger.error("please input args -i or -o")
    exit()

dist = args.output
contest = json_input(args.input)

if not os.path.isfile(dist):
    with open(dist, 'a', encoding='utf-8') as f:
        f.write(json.dumps({}))

data = json_input(dist)

logger.info(f"{args.input} start: ")
calculator = RatingCalculator()
last_idx = 0
last_rank = 1
contestName = contest['contestName']
time = contest['endTime']
link = contest['link']
logger.info(f"Contest Name: {contestName}")

for team in contest['teams']:
    handle = ', '.join(team['members'])
    if handle == '':
        continue
    rank = team['rank']
    _team = {}
    _team['handle'] = handle
    _team['organization'] = team['organization']
    _team['members'] = team['members']
    info = ''
    if 'info' in team.keys():
        info = team['info']
    if handle not in data.keys():
        data[handle] = _team
        data[handle]['history'] = []
    ix = -1
    for i in range(len(data[handle]['history'])):
        if data[handle]['history'][i]['contestId'] == contestName:
           ix = i
           break 
    if ix != -1:
        del data[handle]['history'][ix]
    
    data[handle]['rating'], data[handle]['maxRating'] = calc_rating(data[handle]['history'])

    data[handle]['history'].append({
        'contestId': contestName,
        'contestName': contestName,
        'time': time,
        'teamName': team['name'],
        'rank': rank,
        'oldRating': data[handle]['rating'],
        'link': link,
        'info': info,
    })

    calculator.user_list.append(
        User(
            rank = rank,
            old_rating = data[handle]['rating'],
            handle = handle,
    ))

calculator.calculate()

logger.info(f"Team Number: {len(calculator.user_list)}")

for i in range(len(calculator.user_list)):
    team = calculator.user_list[i]
    handle = team.handle
    rating = team.new_rating
    ix = -1
    for i in range(len(data[handle]['history'])):
        if data[handle]['history'][i]['contestId'] == contestName:
           ix = i
           break
    data[handle]['history'][ix]['newRating'] = rating
    data[handle]['rating'], data[handle]['maxRating'] = calc_rating(data[handle]['history'])

output(dist, data)