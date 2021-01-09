from typing import List
import json
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
import copy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random



def min_w(nodes_list) -> int:
    min_weight = float('inf')
    for node in nodes_list:
        if node.get_weight() < min_weight:
            min_weight = node.get_weight()
            min_node = node
    if min_weight == float('inf'):
        return -1
    return min_node.get_key()


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, g=DiGraph()):
        self.G = g

    def get_graph(self):
        return self.G

    def load_from_json(self, file_name: str) -> bool:
        try:
            with open(file_name, encoding='utf-8') as f:
                json_string = f.read()
            a = json.loads(json_string)
            new_g = DiGraph()
            for node in a.get('Nodes'):
                pos = tuple([float(a) for a in node.get('pos').split(",")])
                new_g.add_node(node.get('id'), pos)
            for edge in a.get('Edges'):
                new_g.add_edge(edge.get('src'), edge.get('dest'), edge.get('w'))
                self.G = new_g
            return True
        except:
            return False

    def save_to_json(self, file_name: str) -> bool:
        try:
            json_string = json.dumps(self.G)
            with open(file_name, "w") as f:
                f.write(json_string)
            return True
        except:
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        current_node = id1
        unvisited_nodes = list(self.G.get_all_v().values())
        self.reset()
        self.G.nodes_list.get(current_node).set_weight(0)
        if self.G.get_node(id2) not in unvisited_nodes:
            return -1, []
        parent = {id1: None}

        while self.G.get_node(current_node).get_weight() != float('inf'):
            if self.G.get_node(id2).get_tag() == 1:
                break
            edges = self.G.all_out_edges_of_node(current_node)
            for edge in edges:
                neighbor = self.G.get_node(edge)
                tmp_weight = self.G.get_node(current_node).get_weight() + edges.get(edge)
                if tmp_weight < neighbor.get_weight():
                    neighbor.set_weight(tmp_weight)
                    parent[neighbor.get_key()] = current_node
            self.G.get_node(current_node).set_tag(1)
            if current_node == id2:
                break
            unvisited_nodes.remove(self.G.get_node(current_node))
            current_node = min_w(unvisited_nodes)
            if current_node == -1:
                return -1, []

        path = [current_node]
        while parent.get(current_node) is not None:
            current_node = parent.get(current_node)
            path.append(current_node)
        path.reverse()
        return self.G.get_node(id2).get_weight(), path

    def connected_component(self, id1: int) -> list:
        G = self.G
        self.bfs(id1)
        connected_org, connected_rev = [], []
        for node in self.G.get_all_v().values():
            if node.get_tag() == 1:
                connected_org.append(node)

        reversed_graph = copy.deepcopy(self.G)
        for edge in reversed_graph.edges_list:
            temp = edge.src
            edge.src = edge.dest
            edge.dest = temp
        self.__init__(reversed_graph)
        self.bfs(id1)
        for node in reversed_graph.get_all_v().values():
            if node.get_tag() == 1:
                connected_rev.append(node)

        self.__init__(G)
        del reversed_graph
        result = []
        for edge_org in connected_org:
            for edge_rev in connected_rev:
                if edge_org.__eq__(edge_rev):
                    result.append(edge_org)
        return result

    def connected_components(self) -> List[list]:
        list_of_nodes = list(self.G.get_all_v().values())
        result = []
        while len(list_of_nodes) != 0:
            connected = self.connected_component(list_of_nodes[0].key)
            result.append(connected)
            for node in connected:
                list_of_nodes.remove(node)
        return result

    def plot_graph(self) -> None:
        points = []
        SIZE = 20
        for node in self.G.get_all_v().values():
            if node.get_location() is None:
                node.set_location((int(random.random() * SIZE), int(random.random() * SIZE), 0))
            points.append(tuple(node.get_location()))

        x_vals = []
        y_vals = []
        for x, y, z in points:
            x_vals.append(x)
            y_vals.append(y)
        plt.figure(figsize=(16, 8), dpi=100)
        plt.scatter(x_vals,y_vals)
        # for node in self.G.get_all_v().values():
        #     x, y, z = node.get_location()
        #     plt.annotate("({x},{y}".format(x=x, y=y), (x, y))
        # size=0.001 , width=0.05, facecolor='red', head_width=3*size, head_length=5*size
        size=0.00001
        for edge in self.G.edges_list:
            x1, y1, z1 = self.G.get_node(edge.src).get_location()
            x2, y2, z1 = self.G.get_node(edge.dest).get_location()
            plt.arrow(x1, y1, x2-x1, y2-y1, length_includes_head=True, width=size, head_width=20*size, head_length=25*size)

        plt.show()

    def reset(self):
        for node in self.G.get_all_v().values():
            node.set_tag(0)
            node.set_weight(float('inf'))
            node.set_info("")

    def bfs(self, node_id):
        for node in self.G.get_all_v():
            self.G.get_node(node).set_tag(0)
        queue = []
        current_node = node_id
        finished = False
        while not finished:
            for edge in self.G.all_out_edges_of_node(current_node).keys():
                neighbor = self.G.get_node(edge)
                if neighbor.get_tag() == 0:
                    if neighbor.get_key() not in queue:
                        queue.append(neighbor.get_key())
            self.G.get_node(current_node).set_tag(1)
            if len(queue) == 0:
                finished = True
            else:
                current_node = queue.pop(0)
