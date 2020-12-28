from typing import List
import json
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph


def min_w(nodes_list) -> int:
    min_weight = float('inf')
    for node in nodes_list:
        if node.get_weight() < min_weight:
            min_weight = node.get_weight()
            min_node = node
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
                new_g.add_node(node.get('id'))
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
        unvisited_nodes = self.connected_component(current_node)
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

        path = [current_node]
        while parent.get(current_node) is not None:
            current_node = parent.get(current_node)
            path.append(current_node)
        path.reverse()
        return self.G.get_node(id2).get_weight(), path

    def connected_component(self, id1: int) -> list:
        self.bfs(id1)
        connected = []
        for node in self.G.get_all_v().values():
            if node.get_tag() == 1:
                connected.append(node)
        return connected

    def connected_components(self) -> List[list]:
        list_of_nodes = self.G.get_all_v()
        while len(list_of_nodes) != 0:
            current_component = list_of_nodes.popitem()
            self.bfs(current_component)
            for node in list_of_nodes:
                if node.get_tag() == 1:
                    list_of_nodes.pop(node.get_key())

    def plot_graph(self) -> None:
        pass

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


