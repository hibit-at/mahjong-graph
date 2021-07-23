import os
import pickle
from collections import defaultdict, deque

# hyper_parameter

agari_num = 8
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
    v.sort()
    ans = [tab[c] for c in v]
    ans = ''.join(ans)
    return ans


def dfs_agari(v):
    global agari
    last_num = 1
    for i in range(pai_range):
        if v.count(i) > 4:
            return
    if len(v) == agari_num:
        s = decode(v)
        agari[s] = True
        return
    if len(v) == 0:
        for i in range(pai_range):
            dfs_agari(v+[i, i])
    if len(v) > 1:
        for i in range(pai_range):
            dfs_agari(v + [i, i, i])
        for i in range(7):
            dfs_agari(v + [i, i+1, i+2])
        for i in range(9, 16):
            dfs_agari(v + [i, i+1, i+2])
        # for i in range(18, 25):
        #     dfs_agari(v + [i, i+1, i+2])
    return


def make_graph():
    q = deque()

    # アガリを末端の goal として設定。これを目指すような DAG を形成。
    for a in agari:
        graph[a] = ([])
        q.append(a)

    cnt = 1

    while q:
        goal = q.popleft()
        print(f'{goal} は {cnt} 番目のノードです')
        cnt += 1
        for i in range(pai_range):
            c = tab[i]
            # 何切る状態か？　何待ち状態か？
            if len(goal) == agari_num:
                # 持っていない牌は切り牌になりえない
                if goal.count(c) == 0:
                    continue
                start = goal.replace(c, '', 1)
            else:
                # 4枚ある牌は待ち牌になりえない
                if goal.count(c) > 3:
                    continue
                start = goal + c
                start = decode(encode(start))
            # 自分のgoalだったものは対象としない（つまり、必ず向聴数が増えるノードに辺を張らせる）
            if start in graph[goal]:
                continue
            graph[start].append(goal)
            # ノードから辺が張られたのが初めてだった場合、それを探索キューに追加
            if start not in q:
                q.append(start)


if os.path.exists('agari.pcl'):
    agari = pickle.load(open('agari.pcl', 'rb'))
else:
    agari = defaultdict(bool)
    dfs_agari([])
    pickle.dump(agari, open('agari.pcl', 'wb'))

# print(agari)

if os.path.exists('graph.pcl'):
    graph = pickle.load(open('graph.pcl', 'rb'))
else:
    graph = defaultdict(list)
    make_graph()
    print(len(graph))
    pickle.dump(graph, open('graph.pcl', 'wb'))


def shanten(s):
    if len(graph[s]) == 0:
        return 0
    ans = min([shanten(parent) for parent in graph[s]])
    return .5 + ans


def machihai(s):
    ans = 0
    for parent in graph[s]:
        # remove
        for c in s:
            parent = parent.replace(c, '', 1)
        ans += 4 - s.count(parent)
    return ans


def nanikiru(s):
    print(f'{s}の何切る？')
    for parent in graph[s]:
        print(parent)
        print(f'{len(graph[parent])}種 {machihai(parent)}枚')


def total(s, indent=0):
    space = ' '*indent
    print(space, f'{s}の待ち牌を検出中...')
    if len(s) == agari_num:
        if len(graph[s]) == 0:
            print(space, 'アガリ')
            return 1
        ans = 0
        print(space, '何切るを開始します')
        for parent in graph[s]:
            ans += total(parent, indent=indent+4)
        return ans
    else:
        ans = 0
        for parent in graph[s]:
            res = parent
            # remove
            for c in s:
                res = res.replace(c, '', 1)
            machi_num = 4 - s.count(res)
            print(space, f'{res} を {machi_num} 枚で待っている')
            ans += machi_num * total(parent, indent=indent+4)
        return ans


def final_tree(s, indent=0):
    space = ' '*indent
    print(space, s)
    if len(s) == agari_num:
        if len(graph[s]) == 0:
            return
        for parent in graph[s]:
            final_tree(parent, indent=indent+4)
    else:
        for parent in graph[s]:
            final_tree(parent, indent=indent+4)
        return


def final(s):
    ans = []
    for parent in graph[s]:
        if len(graph[parent]) == 0:
            return [parent]
        ans.extend(final(parent))
    return ans


graph_list = sorted(graph.items(), key=lambda x: encode(x[0]))

# for s in graph_list:
#     print(s)
#     print(f'total is {total(s[0])}')

ans = final('一二三四五六七八')

ans = list(set(ans))

print(ans)
