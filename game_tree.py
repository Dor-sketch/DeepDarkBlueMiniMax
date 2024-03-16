from networkx.drawing.nx_pydot import graphviz_layout
import networkx as nx
from matplotlib import pyplot as plt
from typing import List
from game_tic_tac_toe import TicTacToe
MAX_LEVEL = 5

INITIAL_STATE = [0, 0, 0, 0, 0, 0, 0, 0, 0]

class GameTree:
    """
    GameTree class
    """

    def __str__(self) -> str:
        ret = ""
        for node, data in self.G.nodes(data=True):

            board += "\n"
            for i, s in enumerate(data['state']):
                board += str(s)
                if i % 3 == 2:
                    board += "\n"
                else:
                    board += " "
            ret += f"{node} {board}\n"
        return ret

    def __init__(self, initial_state=None):
        self.G = nx.DiGraph()
        root_ply = [0, INITIAL_STATE, 1]
        self.add_node(root_ply)
        if initial_state is not None:
            packed_state = [0, initial_state, -1]
            self.add_node(packed_state)

    def generate_id(self, state, level=None, player=None):
        """
        Generates a unique id for the node
        """
        # Convert state to tuple if it is not
        if not isinstance(state, tuple):
            state = tuple(state)

        level = 0
        for mark in state:
            if mark != 0:
                level += 1
        player = 1 if level % 2 == 0 else -1

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
        node_id = self.generate_id(state, level, player)
        if node_id not in self.G:
            self.G.add_node(node_id)
            self.G.nodes[node_id]['state'] = state
            level = 0
            for mark in state:
                if mark != 0:
                    level += 1
            player = 1 if level % 2 == 0 else -1
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

        parent_id = self.generate_id(parent_state, parent_level, parent_player)
        child_id = self.generate_id(child_state, child_level, child_player)
        self.G.add_edge(parent_id, child_id)

    def update_node_value(self, packed_state, value):
        """
        Updates the value of a node
        """
        level, state, player = packed_state
        if level > MAX_LEVEL:
            return
        node_id = self.generate_id(state, level, player)
        # check if node exists
        if node_id in self.G:
            self.G.nodes[node_id]['value'] = value

    def get_path(self, state):
        """
        Returns the path from the root to the node with the given state
        """
        cur = state
        game = TicTacToe()
        cur_level = 0
        for mark in cur:
            if mark != 0:
                cur_level += 1
        cur_player = 1 if cur_level % 2 == 0 else -1
        best_move = self.G.nodes[self.generate_id(
            cur, cur_level, cur_player)]['best_move']
        if best_move is None:
            return
        result = game.result(cur, best_move)
        if game.is_terminal(cur) == False:
            self.get_path(result)
            print()
        print(game.print_state(result))



    def update_node_best_move(self, packed_state, move):
        """
        Updates the state of a node
        """
        level, state, player = packed_state
        if level > MAX_LEVEL:
            return
        node_id = self.generate_id(state, level, player)
        self.G.nodes[node_id]['best_move'] = move

    def plot_mini_max_tree(self, label_type="state"):
        """
        Plots the minimax tree
        """
        G = self.G
        # # check if all nodes have 'level' attribute
        # if not all('level' in data for node, data in G.nodes(data=True)):
        #     raise ValueError("All nodes must have a 'level' attribute: node{}".format(
        #         [node for node, data in G.nodes(data=True) if 'level' not in data]))
        # assign level 0 to nodes without a level
        for node, data in G.nodes(data=True):
            if 'level' not in data:
                data['level'] = 0
        # remove node without a state
        G.remove_nodes_from(
            [node for node, data in G.nodes(data=True) if 'state' not in data])
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
                        plt.text(pos[node][0], pos[node][1] - 0.7, str(data['value']) if data['value'] not in [float('inf'),
                                                                                                               float('-inf')] else "PRUNED DOWN",
                                 ha='center', va='center',
                                 bbox=dict(facecolor='blue' if data['value'] == 1 else 'red', alpha=0.5) if data['value'] not in [
                            float('inf'), float('-inf')] else dict(facecolor='purple', alpha=0.2),
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


    def print_game_tree_from_node(self, node):
        """
        Prints the game tree from a given node
        """
        print("nodes in full graph:")
        print(self.G.nodes(data=True))
        G = self.G
        # choose only the subgraph of the game tree
        subgraph = nx.bfs_tree(G, node)

        # copy node data from original graph to subgraph
        for n in subgraph.nodes():
            subgraph.nodes[n].update(G.nodes[n])

        print("Nodes in the subgraph:")
        print(subgraph.nodes(data=True))

        # remove node without a state
        subgraph.remove_nodes_from(
            [node for node, data in subgraph.nodes(data=True) if 'state' not in data])

        # if too big for tree layout, use neato
        if len(subgraph.nodes) > 400:
            pos = graphviz_layout(subgraph, prog='neato')
        else:
            # Use graphviz_layout with dot for a tree-like layout
            pos = graphviz_layout(subgraph, prog='dot')

        # Draw edges and labels for all nodes
        nx.draw_networkx_edges(subgraph, pos, arrowsize=8, edge_color='grey')
        nx.draw_networkx_nodes(
            subgraph, pos, node_shape='s', node_color='lightblue', alpha=0.5)
        # skip nodes without a state

        nx.draw_networkx_labels(
            subgraph, pos, labels={node: '\n'.join([' '.join(['X' if cell == 1 else 'O' if cell == -1 else ' ' for cell in data['state'][i:i+3]]) for i in range(0, 9, 3)]) for node, data in subgraph.nodes(data=True)}, font_size=6, font_color='black')

        plt.show()
