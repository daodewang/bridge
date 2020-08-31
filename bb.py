import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import json

# 生成随机图
# erdos renyi graph
# generate a graph which has n=20 nodes, probablity p = 0.2.
filename = 'goodG.txt'
flag = 0
N = 1000
P = 0.004004
if flag == 0:
    print('generate a newG')
    ER = nx.random_graphs.erdos_renyi_graph(N, P)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_graph.node_link_data(ER), f)
else:
    print('load a goodG')
    f = open(filename, 'r', encoding='utf-8')
    nld = json.load(f)
    ER = json_graph.node_link_graph(nld)
    f.close()

# 画图
'''
pos = nx.spring_layout(ER)
nx.draw(ER, pos, with_labels=False, node_size=40)
plt.show()'''


##################################
# 删边策略1-边介数
G = nx.Graph(ER)
sublist = []
len_of_mcc = []
edges = []
# 从当前的最大连通子图中删去介数最大的边，直到删去所有边
i = 0
while True:
    # 剩余的连通子图，按大小排序
    sublist.extend([G.subgraph(s) for s in nx.connected_components(G) if len(s) > 1])
    sublist = sorted(sublist, key=len, reverse=False)
    if len(sublist) == 0:
        print('finished')
        len_of_mcc.append(0)
        break
    #print(len(sublist))
    # 找到最大连通子图
    subG = sublist.pop()
    len_of_mcc.append(len(subG))
    G = nx.Graph(subG)

    # 找到介数最大的边
    betweenness = nx.algorithms.centrality.edge_betweenness_centrality(G)
    sbetweenness = sorted(betweenness.items(), key=lambda x: (x[1]), reverse=True)
    #print(sbetweenness)
    mb_edge = sbetweenness[0][0]
    edges.append(mb_edge)
    #print(mb_edge)

    # 删除该边
    G.remove_edge(*mb_edge)
    i = i+1
    #print(f'round{i}')

print(len_of_mcc)
print(edges)
with open('del_eb.txt', 'w', encoding='utf-8') as f:
    json.dump(len_of_mcc, f)


print('-------------------------------------------------------')

##################################
# 删边策略2-桥
G = nx.Graph(ER)
MEIQIAO = 1
sublist = []
len_of_mcc = []
edges = []

arg1 = 0.5
arg2 = 0.5
# 从当前的最大连通子图中删去介数最大的边，直到删去所有边
i = 0
while True:
    # 剩余的连通子图，按大小排序
    sublist.extend([G.subgraph(s) for s in nx.connected_components(G) if len(s) > 1])
    sublist = sorted(sublist, key=len, reverse=False)
    if len(sublist) == 0:
        print('finished')
        len_of_mcc.append(0)
        break
    #print(len(sublist))
    # 找到最大连通子图
    subG = sublist.pop()
    len_of_mcc.append(len(subG))
    G = nx.Graph(subG)

    # 从当前的最大连通子图中找桥接链路
    brs = list(nx.bridges(G))
    score_brs = []
    #print(len(brs))
    if len(brs) == 0:
        if MEIQIAO == 0:
            # 策略1 最大连通子图没桥，游戏结束
            print('finished with big subgraph')
            break
        else:
            # 策略2 只计算score2
            # 按下面公式找到最优桥
            for e in G.edges():
                #print('here')
                #print(e)
                deg = G.degree()
                sdeg = sorted(deg, key=lambda x: (x[1]), reverse=True)
                maxdeg = sdeg[0][1]

                score2 = G.degree(e[0]) * G.degree(e[1]) / maxdeg / maxdeg
                score = arg2 * score2
                score_brs.append((e, score))
    else:
        # 按下面公式找到最优桥
        for br in brs:
            deg = G.degree()
            sdeg = sorted(deg, key=lambda x: (x[1]), reverse=True)
            maxdeg = sdeg[0][1]
            #print(maxdeg)
            # 删边算分
            G.remove_edge(*br)
            csg = list(nx.connected_components(G))
            score1 = 4*len(csg[0])*len(csg[1])/N/N
            score2 = G.degree(br[0])*G.degree(br[1])/maxdeg/maxdeg
            score = arg1*score1 + arg2*score2
            score_brs.append((br, score))
            # 算完补边
            G.add_edge(*br)

    # 选最高分的桥删
    ssb = sorted(score_brs, key=lambda x: (x[1]), reverse=True)
    #print(ssb)
    msb_edge = ssb[0][0]
    edges.append(msb_edge)
    #print(msb_edge)
    G.remove_edge(*msb_edge)
    i = i + 1
    #print(f'round{i}')

print(len_of_mcc)
print(edges)
with open('del_bridge.txt', 'w', encoding='utf-8') as f:
    json.dump(len_of_mcc, f)



