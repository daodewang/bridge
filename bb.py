import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import json

# 生成随机图
# erdos renyi graph
# generate a graph which has n=20 nodes, probablity p = 0.2.
filename = 'goodG.txt'
flag = 1
if flag == 0:
    print('generate a newG')
    ER = nx.random_graphs.erdos_renyi_graph(100, 0.004004)
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
G = ER
sublist = []
i = 0
len_of_mcc = []
while True:
    # 剩余的连通子图，按大小排序
    sublist.extend([G.subgraph(s) for s in nx.connected_components(G) if len(s) > 1])
    sublist = sorted(sublist, key=len, reverse=False)
    if len(sublist) == 0:
        print('finished')
        break
    print(len(sublist))
    # 找到最大连通子图
    subG = sublist.pop()
    len_of_mcc.append(len(subG))
    G = nx.Graph(subG)

    # 找到介数最大的边
    betweenness = nx.algorithms.centrality.edge_betweenness_centrality(G)
    sbetweenness = sorted(betweenness.items(), key=lambda x: (x[1]), reverse=True)
    #print(sbetweenness)
    mb_edge = sbetweenness[0][0]
    print(mb_edge)

    # 删除该边
    G.remove_edge(*mb_edge)
    i = i+1
    print(f'round{i}')

# 从当前的最大连通子图中删去介数最大的边，直到删去所有边？


'''
##################################
# 删边策略2-桥
arg1 = 0.5
arg2 = 0.5
# 剩余的连通子图，按大小排序
list = []

# 从当前的最大连通子图中找桥接链路
subG = list[0]
brs = nx.bridges(ER)

# 按下面公式找到最优桥
for br in brs:
    subG.remove_edge(br)
    csg = list(nx.connected_components())
    score = 1
'''
