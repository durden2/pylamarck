from unittest import TestCase
from pylamarck.spaces.trees.production import Node


class TestNode(TestCase):
    def test_get_tag(self):
        node = Node()
        self.assertRaises(NotImplementedError, node.get_tag)

    def test_get_child(self):
        node = Node()
        self.assertRaises(NotImplementedError, lambda: node.get_child(0))

    def test_get_child_tags(self):
        node = Node()
        self.assertRaises(NotImplementedError, lambda: node.get_child_tags())

    def test_get_child_tag(self):
        node = Node()
        self.assertRaises(NotImplementedError, lambda: node.get_child_tag(0))

    def test_num_children(self):
        node = Node()
        self.assertRaises(NotImplementedError, node.num_children)

    def test_set_child(self):
        node = Node()
        self.assertRaises(NotImplementedError, lambda: node.set_child(0, None))
