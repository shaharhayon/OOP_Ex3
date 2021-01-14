import unittest

from src.DiGraph import DiGraph


class MyTestCase(unittest.TestCase):
    def test_add_element(self):
        G = DiGraph()
        G.add_node(0)
        self.assertFalse(G.add_edge(0,1,13))
        G.add_node(1)
        self.assertTrue(G.add_edge(0,1,13))

    def test_remove_node(self):
        G = DiGraph()
        self.assertFalse(G.remove_node(0))
        G.add_node(0)
        self.assertTrue(G.remove_node(0))

    def test_remove_edge(self):
        G = DiGraph()
        G.add_node(0)
        G.add_node(1)
        self.assertFalse(G.remove_edge(0,1))
        G.add_edge(0, 1, 13)
        self.assertTrue(G.remove_edge(0,1))
        self.assertEqual(len(G.edges_list), G.edgeSize)
        self.assertEqual(len(G.edges_list), 0)

    def test_get_all_v(self):
        G = DiGraph()
        G.add_node(0)
        G.add_node(1)
        self.assertEqual(len(G.get_all_v()), 2)

    def test_all_edges(self):
        G = DiGraph()
        G.add_node(0)
        G.add_node(1)
        G.add_node(2)
        G.add_edge(0,1,10)
        G.add_edge(2, 1, 10)
        self.assertEqual(len(G.all_in_edges_of_node(1)), 2)
        self.assertEqual(len(G.all_out_edges_of_node(1)), 0)
        self.assertEqual(len(G.all_in_edges_of_node(0)), 0)
        self.assertEqual(len(G.all_out_edges_of_node(0)), 1)


if __name__ == '__main__':
    MyTestCase.test_add_element()
    MyTestCase.test_remove_node()
    MyTestCase.test_remove_edge()
    MyTestCase.test_get_all_v()
    MyTestCase.test_all_edges()
