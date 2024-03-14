from networkx.drawing.nx_pydot import graphviz_layout
import networkx as nx
from matplotlib import pyplot as plt

class GameTree:
    """
    GameTree class
    """
    def __init__(self, graph: nx.DiGraph):
        self.G = graph

    def plot_mini_max_tree(self):
        """
        Plots the minimax tree
        """
        G = self.G

        # Get nodes at odd and even levels
        odd_level_nodes = [node for node, data in G.nodes(
            data=True) if data['level'] % 2 == 0]
        even_level_nodes = [node for node, data in G.nodes(
            data=True) if data['level'] % 2 == 1]

        # Use graphviz_layout with dot for a tree-like layout
        pos = graphviz_layout(G, prog='dot')

        # Draw nodes at odd levels with triangle shape
        nx.draw_networkx_nodes(
            G, pos, nodelist=odd_level_nodes, node_shape='^', node_color='lightblue')

        # Draw nodes at even levels with upside-down triangle shape
        nx.draw_networkx_nodes(
            G, pos, nodelist=even_level_nodes, node_shape='v', node_color='red')

        # Draw edges and labels for all nodes
        nx.draw_networkx_edges(G, pos, arrowsize=10, edge_color='lightgrey')
        nx.draw_networkx_labels(
            G, pos, labels={node: data['value'] for node, data in G.nodes(data=True)}, font_size=6, font_color='black')

        plt.show()
