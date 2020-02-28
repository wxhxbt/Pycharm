from pyvis.network import Network
import networkx as nw
import random
import matplotlib.pyplot as plt
import numpy as np


colors = ['#DC143C', '#800080', '#0000CD', '#00FF00', '#008000', '#FFFF00',
              '#FFA500', '#000000', '#8B4513', '#00FFFF', '#FF1493']

def build_graph():
    result = []
    with open('graph_drawing.txt', 'r') as f:
        for line in f:
            result.append(list(map(int, line.split(' '))))
            # print(result)
    g = Network()
    for i in range(0, len(result)):
        g.add_node(result[i][0])
        g.add_node(result[i][1])
        g.add_edge(result[i][0], result[i][1])
    degrees = {}
    x = g.get_nodes()
    for node in x:
        degrees[node] = len(g.neighbors(node))
    net = Network()
    for i in range(0, len(result)):
        str1 = str(result[i][0]) + ':' + str(degrees[result[i][0]])
        str2 = str(result[i][1]) + ':' + str(degrees[result[i][1]])
        net.add_node(result[i][0], label=str1)
        net.add_node(result[i][1], label=str2)
        net.add_edge(result[i][0], result[i][1])

    g.show_buttons()
    g.toggle_physics(False)
    g.show("original.html")
    net.toggle_physics(False)
    net.show_buttons()
    net.show("mygraph.html")
    edges_list = []
    for edge in g.get_edges():
        edges_list.append((edge['from'], edge['to']))
    degrees[3] += 1
    print(degrees[3])
    return x, edges_list, degrees.values()


def network_x(nodes, edges):
    G = nw.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    ntx = Network()
    ntx.from_nx(G)
    ntx.show_buttons()
    # ntx.show("networkX.html")
    print(nw.is_biconnected(G))
    bc = list(nw.biconnected_components(G))
    print(bc)
    ap = list(nw.articulation_points(G))
    return bc, ap


def color_bc(edges, bc):
    # random.shuffle(colors)

    g = Network()
    for i in range(0, len(edges)):
        x = edges[i][0]
        y = edges[i][1]
        color_index = -1
        for j in range(0, len(bc)):
            if x in bc[j] and y in bc[j]:
                print("Edge:", edges[i], " BC_index:", j)
                color_index = j
                break
        g.add_node(x)
        g.add_node(y)
        g.add_edge(x, y, color=colors[color_index], width=7)
    g.show_buttons()
    g.show('bcc.html')


def meta_graph(bc, ap):
    g = Network()
    g.add_nodes(ap)
    for i in range(len(bc)):
        g.add_node(1000+i, label='BC'+str(i+1), color=colors[i])
        for j in ap:
            if j in bc[i]:
                g.add_edge(j, 1000+i, color=colors[i], width=7)

    g.show_buttons()
    g.show('meta_graph.html')


nodes, edges, degrees = build_graph()
print(len(nodes), len(edges))
bc, ap = network_x(nodes, edges)
color_bc(edges, bc)
meta_graph(bc, ap)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(list(degrees), bins=6, edgecolor="black", align='mid')
plt.title('Degree distribution')
plt.xlabel('Degree')
plt.ylabel('Nodes')
plt.show()
print(np.mean(list(degrees)))
