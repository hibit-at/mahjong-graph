import copy
import os
import pickle
from collections import defaultdict, deque

import numpy as np

# hyper_parameter

agari_num = 14
pai_range = 21

manzu = '一二三四五六七八九'
souzu = '１２３４５６７８９'
jihai = '白発中'
all_hai = manzu + souzu + jihai

tab = {}
cnt = 0
for a in all_hai:
    tab[cnt] = a
    cnt += 1

inv = {}
cnt = 0
for a in all_hai:
    inv[a] = cnt
    cnt += 1

print(tab)


def encode(s):
    ans = [inv[c] for c in s]
    ans.sort()
    return ans


def decode(v):
    ans = ''
    for i in range(pai_range):
        for c in range(v[i]):
            ans += tab[i]
    return ans


def dfs_agari(v):
    global agari_num
    maisu = 0
    for i in range(pai_range):
        maisu += v[i]
        if v[i] > 4:
            return
    if maisu == agari_num:
        w = tuple(v)
        if not agari[w]:      
            if len(agari) % 10000 == 0:
                print(f'{len(agari)} 番目のアガり形は {decode(v)}')
        agari[w] = True
        return
    if maisu == 0:
        for i in range(pai_range):
            w = v.copy()
            w[i] = 2
            dfs_agari(w)
    if maisu > 1:
        for i in range(pai_range):
            if v[i] > 1:
                continue
            w = v.copy()
            w[i] += 3
            dfs_agari(w)
        for i in range(7):
            if v[i] > 3 or v[i+1] > 3 or v[i+2] > 3:
                continue
            w = v.copy()
            w[i] += 1
            w[i+1] += 1
            w[i+2] += 1
            dfs_agari(w)
            if v[i+9] > 3 or v[i+10] > 3 or v[i+11] > 3:
                continue
            w = v.copy()
            w[i+9] += 1
            w[i+10] += 1
            w[i+11] += 1
            dfs_agari(w)
    return


def make_graph():
    global graph
    global sep_graph
    shanten = -.5

    # アガリを末端の goal として設定。これを目指すような DAG を形成。
    for a in agari:
        sep_graph[shanten][a] = []
        graph[a] = []
    cnt = 1

    while sep_graph[shanten]:

        # 何切る

        print(f'{shanten} シャンテンの何切る')

        for goal in sep_graph[shanten]:
            if cnt % 10000 == 0:
                print(f'{decode(goal)} は {cnt} 番目のノードです')
            cnt += 1
            for i in range(pai_range):
                # 持っていない牌は切り牌になりえない
                if goal[i] == 0:
                    continue
                start = list(goal)
                start[i] -= 1
                start = tuple(start)
                # アガリだった場合、問答無用で辺を張る
                if shanten == -.5:
                    sep_graph[shanten+.5][start].append(goal)
                    graph[start].append(goal)
                    continue
                # 自分のgoalだったものは対象としない（つまり、必ず向聴数が増えるノードに辺を張らせる）
                if start in sep_graph[shanten-.5]:
                    continue
                sep_graph[shanten+.5][start].append(goal)
                graph[start].append(goal)
                # ノードから辺が張られたのが初めてだった場合、それを探索キューに追加

        # 何待ち

        shanten += .5

        print(f'{shanten} シャンテンの何待ち')

        for goal in sep_graph[shanten]:
            if cnt % 10000 == 0:
                print(f'{decode(goal)} は {cnt} 番目のノードです')
            cnt += 1
            for i in range(pai_range):
                # 4枚ある牌は待ち牌になりえない
                if goal[i] > 3:
                    continue
                start = list(goal)
                start[i] += 1
                start = tuple(start)
                # 自分のgoalだったものは対象としない（つまり、必ず向聴数が増えるノードに辺を張らせる）
                if start == (1, 3, 3, 1, 0, 0, 0, 0, 0):
                    print('stop')
                if start in sep_graph[shanten-.5]:
                    continue
                sep_graph[shanten+.5][start].append(goal)
                graph[start].append(goal)

        shanten += .5


if os.path.exists('agari.pcl'):
    agari = pickle.load(open('agari.pcl', 'rb'))
else:
    agari = defaultdict(bool)
    v = np.zeros(pai_range, dtype='int32')
    dfs_agari(v)
    pickle.dump(agari, open('agari.pcl', 'wb'))


def func():
    return defaultdict(list)


if os.path.exists('sep_graph.pcl') and os.path.exists('graph.pcl'):
    sep_graph = pickle.load(open('sep_graph.pcl', 'rb'))
    graph = pickle.load(open('graph.pcl', 'rb'))
else:
    sep_graph = defaultdict(func)
    graph = defaultdict(list)
    make_graph()
    pickle.dump(sep_graph, open('sep_graph.pcl', 'wb'))
    pickle.dump(graph, open('graph.pcl', 'wb'))

richi = sep_graph[0]

richi = sorted(richi.items(), key = lambda x : -len(x[1]))
richi = richi[:5]

for r in richi:
    print(decode(r[0]),'の待ち牌',len(r[1]),'種類')
    machihai = [decode(m) for m in r[1]]
    print(','.join(machihai))
    
print('stop')
