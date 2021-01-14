import unittest
import copy
from src.GraphAlgo import GraphAlgo
from src.DiGraph import DiGraph


class MyTestCase(unittest.TestCase):

    def test_save_load(self):
        algo = GraphAlgo()
        algo.load_from_json('../data/A4')
        G = copy.deepcopy(algo.get_graph())
        self.assertTrue(algo.get_graph().__eq__(G))
        G.remove_node(5)
        self.assertNotEqual(algo.get_graph(), G)
        algo.__init__(G)
        self.assertEqual(algo.get_graph(), G)
        algo.G.remove_node(1)
        algo.G.remove_node(2)
        algo.G.remove_node(3)
        algo.save_to_json('test_save_load.json')
        G = copy.deepcopy(algo.get_graph())
        algo.__init__(DiGraph())
        self.assertNotEqual(algo.get_graph(), G)
        algo.load_from_json('test_save_load.json')
        self.assertTrue(algo.get_graph().__eq__(G))

    def test_strongly_connected(self):
        algo = GraphAlgo()
        algo.load_from_json('../data/A4')
        components = len(algo.connected_components())
        self.assertEqual(components, 1)

    def test_shortest_path(self):
        algo = GraphAlgo()
        algo.load_from_json('../data/A0')
        path, pathList= algo.shortest_path(3, 9)
        pathDist=len(pathList)-1
        pathList2 = [3,2,1,0,10,9]
        self.assertEqual(pathDist, 5)
        self.assertEqual(pathList,pathList2)


if __name__ == '__main__':
    MyTestCase.test_save_load()
    MyTestCase.test_strongly_connected()
    MyTestCase.test_shortest_path()
