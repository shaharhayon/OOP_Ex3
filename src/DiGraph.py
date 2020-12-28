

from GraphInterface import GraphInteface


class DiGraph(GraphInteface):
    class Node:
        def __init__(self, key, pos=()):
            self.key = key
            self.tag = 0
            self.weight = 0.0
            self.info = ""
            self.position = pos

        def __str__(self) -> str:
            to_str = "Node ", self.get_key(), ":\n", self.get_location()
            return to_str

        def get_key(self):
            return self.key

        def get_location(self):
            return self.position

        def set_location(self, p):
            self.position = p

        def get_weight(self):
            return self.weight

        def set_weight(self, w):
            self.weight = w

        def get_info(self):
            return self.info

        def set_info(self, s):
            self.info = s

        def get_tag(self):
            return self.tag

        def set_tag(self, t):
            self.tag = t

        # def __eq__(self, o: object) -> bool:
        #     return self.key == o.key

    class Edge:
        def __init__(self, src: int, dest: int, weight: float):
            self.src, self.dest = src, dest
            self.tag = 0
            self.weight = weight
            self.info = ""

        def get_src(self):
            return self.src

        def get_dest(self):
            return self.dest

        def get_weight(self):
            return self.weight

        def get_info(self):
            return self.info

        def set_info(self, s):
            self.info = s

        def get_tag(self):
            return self.tag

        def set_tag(self, t):
            self.tag = t

    def __init__(self):
        self.nodes_list = {}
        self.edges_list = {}
        self.nodeSize, self.edgeSize, self.MC = 0, 0, 0

    def v_size(self) -> int:
        return self.nodeSize

    def e_size(self) -> int:
        return self.edgeSize

    def get_mc(self) -> int:
        return self.MC

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self.nodes_list.keys() or id2 not in self.nodes_list.keys():
            return False

        if self.edges_list.get(id1) is None:
            self.edges_list[id1] = []

        for e in self.edges_list[id1]:
            if e.get_src() == id1 and e.get_dest == id2:
                return False

        e = DiGraph.Edge(id1, id2, weight)
        self.edges_list[id1].append(e)

        if e in self.edges_list.get(id1):
            self.edgeSize += 1
            return True
        else:
            return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self.nodes_list.keys():
            return False

        n = DiGraph.Node(node_id, pos)
        self.nodes_list[node_id] = n

        if self.nodes_list.get(node_id) == n:
            self.nodeSize += 1
            return True
        else:
            return False

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self.nodes_list.keys():
            return False

        self.edges_list.pop(node_id)
        self.nodeSize -= 1
        for edge_arr in self.edges_list.values():
            for e in edge_arr:
                if e.get_dest == node_id:
                    DiGraph.remove_edge(e.get_src(), e.get_dest())
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        for e in self.edges_list.get(node_id1):
            if e.get_dest() == node_id2:
                self.edges_list[node_id1].remove(e)
                self.edgeSize -= 1
                return True
        return False

    def get_all_v(self) -> dict:
        return self.nodes_list

    def all_in_edges_of_node(self, id1: int) -> dict:
        in_edges = {}
        for el in self.edges_list.values():
            for e in el:
                if e.get_dest() == id1:
                    in_edges[e.get_src()] = e.get_weight()
        return in_edges

    def all_out_edges_of_node(self, id1: int) -> dict:
        out_edges = {}
        if self.edges_list.get(id1) is not None:
            for e in self.edges_list.get(id1):
                out_edges[e.get_dest()] = e.get_weight()
        return out_edges

    def get_node(self, node_id) -> Node:
        return self.nodes_list.get(node_id)
