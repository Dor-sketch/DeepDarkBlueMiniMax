from networkx.drawing.nx_pydot import graphviz_layout
import networkx as nx
from matplotlib import pyplot as plt
from typing import List

MAX_LEVEL = 4

class GameTree:
    """
    GameTree class
    """

    def __init__(self, initial_state=None):
        self.G = nx.DiGraph()
        if initial_state is not None:
            packed_state = [0, initial_state, 1]
            self.add_node(packed_state)

    def generate_id(self, state, level, player):
        """
        Generates a unique id for the node
        """
        print(
            f'generating id for state {state} at level {level} and player {player}')
        # Convert state to tuple if it is not
        if not isinstance(state, tuple):
            state = tuple(state)

        # Generate id
        return "#".join([str(level), str(state), str(player)])

    def add_node(self, packed_state):
        """
        Adds a node to the graph
        """
        # TODO: switch to named tuple or class
        level, state, player = packed_state
        if level > MAX_LEVEL:
            return
        print(
            f'adding node at level {level} with state {state} and player {player}')
        print(packed_state)
        node_id = self.generate_id(state, level, player)
        if node_id not in self.G:
            self.G.add_node(node_id)
            self.G.nodes[node_id]['state'] = state
            self.G.nodes[node_id]['level'] = level
            # player can also be calculated based on level
            self.G.nodes[node_id]['player'] = player
            self.G.nodes[node_id]['value'] = None

    def add_edge(self, parent: List, child: List):
        """
        Adds an edge to the graph
        """
        parent_level, parent_state, parent_player = parent
        child_level, child_state, child_player = child

        if parent_level > MAX_LEVEL or child_level > MAX_LEVEL:
            return
        print(f'adding edge from {parent_state} to {child_state}')

        parent_id = self.generate_id(parent_state, parent_level, parent_player)
        child_id = self.generate_id(child_state, child_level, child_player)
        self.G.add_edge(parent_id, child_id)

    def update_node_value(self, packed_state, value):
        """
        Updates the value of a node
        """
        print(packed_state)
        level, state, player = packed_state
        if level > MAX_LEVEL:
            return
        print(
            f'updating node value for state {state} at level {level} and player {player} to {value}')
        node_id = self.generate_id(state, level, player)
        self.G.nodes[node_id]['value'] = value

    def update_node_state(self, packed_state, state):
        """
        Updates the state of a node
        """
        level, state, player = packed_state
        if level > MAX_LEVEL:
            return
        node_id = self.generate_id(state, level, player)
        self.G.nodes[node_id]['state'] = state

    def plot_mini_max_tree(self, label_type="value"):
        """
        Plots the minimax tree
        """
        G = self.G

        # Get nodes at odd and even levels
        odd_level_nodes = [node for node, data in G.nodes(
            data=True) if data['level'] % 2 == 0]
        even_level_nodes = [node for node, data in G.nodes(
            data=True) if data['level'] % 2 == 1]

        # if too big for tree layout, use neato
        if len(G.nodes) > 400:
            pos = graphviz_layout(G, prog='neato')
        else:
            # Use graphviz_layout with dot for a tree-like layout
            pos = graphviz_layout(G, prog='dot')

        # Draw edges and labels for all nodes
        nx.draw_networkx_edges(G, pos, arrowsize=8, edge_color='grey')

        if label_type == "state":
            # draw nodes at odd levels with rectangle shape based on player color
            nx.draw_networkx_nodes(
                G, pos, nodelist=odd_level_nodes, node_shape='s', node_color='lightblue', alpha=0.5)

            # draw nodes at even levels with circle shape based on player color
            nx.draw_networkx_nodes(
                G, pos, nodelist=even_level_nodes, node_shape='s', node_color='red', alpha=0.5)
            nx.draw_networkx_labels(
                G, pos, labels={node: '\n'.join([' '.join(['X' if cell == 1 else 'O' if cell == -1 else ' ' for cell in data[label_type][i:i+3]]) for i in range(0, 9, 3)]) for node, data in G.nodes(data=True)}, font_size=6, font_color='black')

            # add utility values to the terminal nodes
            for node, data in G.nodes(data=True):
                if data['value'] is not None:
                    if G.out_degree(node) == 0:
                        plt.text(pos[node][0], pos[node][1] - 0.7, str(data['value']) if data['value'] not in [float('inf'), float('-inf')] else "PRUNED DOWN",
                                 ha='center', va='center', bbox=dict(facecolor='green', alpha=0.5) if data['value'] not in [float('inf'), float('-inf')] else dict(facecolor='purple', alpha=0.2),
                                    fontsize=4 if data['value'] not in [float('inf'), float('-inf')] else 2)
        else:
            # Draw nodes at odd levels with triangle shape
            nx.draw_networkx_nodes(
                G, pos, nodelist=odd_level_nodes, node_shape='^', node_color='lightblue')

            # Draw nodes at even levels with upside-down triangle shape
            nx.draw_networkx_nodes(
                G, pos, nodelist=even_level_nodes, node_shape='v', node_color='red')

            nx.draw_networkx_labels(
                G, pos, labels={node: data[label_type] for node, data in G.nodes(data=True)}, font_size=6, font_color='black')




        plt.show()
