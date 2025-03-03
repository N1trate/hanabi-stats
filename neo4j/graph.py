import csv
import networkx as nx
from networkx.algorithms import community

import py_no_doc.utils as u


G = nx.Graph()
players = []
with open('data/cut version/players_cut.csv', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        players.append(line.rstrip('\n'))


G.add_nodes_from(players)
print(G)
# Graph with 49992 nodes and 0 edges

weights_all = u.open_csv('data/cut version/weights_cut.csv')
for w in weights_all:
    G.add_edge(w[0], w[1], weight=w[2], type='rel')
print(G)
# Graph with 49992 nodes and 126238 edges

pr = nx.pagerank(G)
print('--pagerank--')

res = list(community.label_propagation.asyn_lpa_communities(G, weight='weight'))
print('--community--')

f = open('pagerank.csv', 'w', encoding='UTF-8', newline='')
w = csv.writer(f)
for p in players:
    print(p)
    p_pr = pr[p]
    p_com = res.index([r for r in res if p in r][0])
    w.writerow([p, p_pr, p_com])
f.close()
