import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import random
import networkx as nx
from collections import Counter

class Relations:
    def __init__(self, id, depth, edges, rng=(10, 10)):
        self.id = id
        self.depth = depth
        self.G = self.graph_by_id(edges.astype(int))
        self.rng = rng
        self.add_positions()
        
    # Create relation graph with certain depth
    def graph_by_id(self, edges):
        prev = None
        RG = nx.Graph()
        for i in tqdm_notebook(range(self.depth)):
            if prev is None:
                RG.add_edges_from(edges[edges[:,0] == self.id])
                prev = edges[edges[:,0] == self.id]
                continue

            tmp = np.array([]).reshape(-1, 2)
            for j in prev[:,1]:
                tmp =  np.concatenate((tmp, edges[edges[:,0] == j]))
            prev = tmp
            RG.add_edges_from(tmp)
        
        print('Graph is ready for work')
        return RG
    
    # Add positions into graph for each node
    def add_positions(self):
        try:
            nodes = list(self.G.nodes)
            for node in nodes:
                x = random.uniform(0, self.rng[0])
                y = random.uniform(0, self.rng[1])
                self.G.nodes[node]['pos'] = [x, y]
            print('Positions was added')
        except:
            print('Graph not define!')
    
    # Plot relation graph
    def rplot(self):
        edge_x = []
        edge_y = []
        nodes = list(self.G.nodes)

        for edge in self.G.edges():
            x0, y0 = self.G.node[edge[0]]['pos']
            x1, y1 = self.G.node[edge[1]]['pos']
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        node_text = []

        for node in self.G.nodes():
            x, y = self.G.node[node]['pos']
            node_x.append(x)
            node_y.append(y)
            node_text.append('User ' + str(node))

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            hovertext=node_text,
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='Viridis',
                reversescale=True,
                color=[j for j in range(len(node_x))],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))


        fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title='Relations plot',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
        fig.show()
        
    def top_friends(self, mc=3):
        nrs_now = list(self.G.neighbors(self.id))
        good = []

        for _ in range(self.depth):
            tmp_good = []
            c = Counter()
            for i in nrs_now:
                tmp = list(self.G.neighbors(i))
                for j in tmp:
                    c[j] += 1
            for i in c:
                if c[i]/len(nrs_now) >= 0.5:
                    tmp_good.append((i, c[i]/len(nrs_now)))

            if len(tmp_good) < 3:
                mcommon = c.most_common(mc)[len(tmp_good):]
                for common in mcommon:
                    tmp_good.append((common[0], common[1]/len(nrs_now)))

            nrs_now = [i[0] for i in tmp_good]
            good += tmp_good
        

        good.sort(key=lambda x: x[1], reverse=True)
        return good