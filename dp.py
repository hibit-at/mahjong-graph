import os
import pickle
from collections import defaultdict

import numpy as np

# hyper_parameter

agari_num = 11
pai_range = 27

manzu = '一二三四五六七八九'
pinzu = '①②③④⑤⑥⑦⑧⑨'
souzu = '１２３４５６７８９'
all_hai = manzu + pinzu + souzu

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
    if maisu % 3 == 2:
        w = tuple(v)
        if not agari[w]:      
            if len(agari) % 1000 == 0:
                print(f'{len(agari)} 番目のアガり形は {decode(v)}')
        agari[w] = True
    if maisu == agari_num:
        return
    if maisu == 0:
        for i in range(pai_range):
            w = v.copy()
            w[i] = 2
            dfs_agari(w)
    if maisu > 1:
        for i in range(pai_range):
            w = v.copy()
            w[i] += 3
            dfs_agari(w)
        for i in range(7):
            w = v.copy()
            w[i] += 1
            w[i+1] += 1
            w[i+2] += 1
            dfs_agari(w)
            w = v.copy()
            w[i+9] += 1
            w[i+10] += 1
            w[i+11] += 1
            dfs_agari(w)
            w = v.copy()
            w[i+18] += 1
            w[i+19] += 1
            w[i+20] += 1
            dfs_agari(w)
    return


def make_graph():
    
    visited_graph = {}
    shanten = -.5

    if os.path.exists('graph_-0.5.pcl'):
        current_graph = pickle.load(open('graph_-0.5.pcl','rb'))
    else:
        current_graph = defaultdict(list)
        # アガリを末端の goal として設定。これを目指すような dp table を形成。
        for a in agari:
            current_graph[a] = []
        pickle.dump(current_graph,open('graph_-0.5.pcl','wb'))

    cnt = 1

    while os.path.exists(f'graph_{shanten}.pcl'):

        if os.path.exists(f'graph_{shanten+.5}.pcl'):
            print(f'{shanten} シャンテンは既に計算が済んでいるようです')
            shanten += .5
            continue

        if shanten == -.5:
            visited_graph = {}
        else:
            visited_graph = pickle.load(open(f'graph_{shanten-.5}.pcl','rb'))
        current_graph = pickle.load(open(f'graph_{shanten}.pcl','rb'))
        new_graph = defaultdict(list)

        if shanten % 1 == .5:
            state = '何切る'
            nanikiru = True
        else:
            state = '何待ち'
            nanikiru = False

        for goal in current_graph:
            if cnt % 10000 == 0:
                print(f'{decode(goal)} は {cnt} 番目のノードです。（{shanten} シャンテンの{state}）')
            cnt += 1
            for i in range(pai_range):
                if nanikiru:
                    # 持っていない牌は切り牌になりえない
                    if goal[i] == 0:
                        continue
                    start = list(goal)
                    start[i] -= 1
                else:
                    # 4枚ある牌は待ち牌になりえない
                    if goal[i] > 3:
                        continue
                    start = list(goal)
                    start[i] += 1
                start = tuple(start)
                # 自分のgoalだったものは対象としない（つまり、必ず向聴数が増えるノードに辺を張らせる）
                if start in visited_graph:
                    continue
                new_graph[start].append(goal)
        
        if len(new_graph) > 0:
            pickle.dump(new_graph,open(f'graph_{shanten+.5}.pcl','wb'))
        shanten += .5


if os.path.exists('agari.pcl'):
    agari = pickle.load(open('agari.pcl', 'rb'))
else:
    agari = defaultdict(bool)
    v = np.zeros(pai_range, dtype='int32')
    dfs_agari(v)
    pickle.dump(agari, open('agari.pcl', 'wb'))

make_graph()

print('stop')
