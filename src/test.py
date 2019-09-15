import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from tree_draw import tree_pos


G = nx.Graph()

G.add_node(1, image=mpimg.imread('icon1.png'))
G.add_node(2, image=mpimg.imread('icon2.png'))
G.add_node(3, image=mpimg.imread('icon2.png'))
G.add_node(4, image=mpimg.imread('icon1.png'))
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(1, 4)

# G.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (2, 7), (3, 8), (3, 9), (4, 10),
#                   (5, 11), (5, 12), (6, 13)])
pos = tree_pos(G, 1)
# nx.draw(G, pos=pos, with_labels=True)
fig = plt.figure(figsize=(5, 5))
ax = plt.subplot(111)
ax.set_aspect('equal')
nx.draw_networkx(G, pos=pos)

trans = ax.transData.transform
trans2 = fig.transFigure.inverted().transform

piesize = 0.2  # this is the image size
p2 = piesize / 2.0
for n in G:
    xx, yy = trans(pos[n])  # figure coordinates
    xa, ya = trans2((xx, yy))  # axes coordinates
    a = plt.axes([xa - p2, ya - p2, piesize, piesize])
    a.set_aspect('equal')
    a.imshow(G.node[n]['image'])
    a.axis('off')
ax.axis('off')

plt.savefig('tree.png')