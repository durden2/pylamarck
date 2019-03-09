from pylamarck.production import NullarySearchOperation, UnarySearchOperation
from pylamarck.algorithms.evolutionary import Evaluator

import numpy as np
import random
from copy import copy, deepcopy


class Node:
    def get_tag(self):
        raise NotImplementedError

    def get_child(self, child_num):
        raise NotImplementedError

    def get_child_tags(self):
        raise NotImplementedError

    def get_child_tag(self, child_num):
        raise NotImplementedError

    def num_children(self):
        raise NotImplementedError

    def set_child(self, child_num, node):
        raise NotImplementedError

    def get_depth(self):
        if self.num_children() == 0:
            return 1
        else:
            return 1 + max(self.get_child(i).get_depth()
                           for i in range(self.num_children()))

    def get_node_number(self):
        if self.num_children() == 0:
            return 1
        else:
            return 1 + sum(self.get_child(i).get_node_number()
                           for i in range(self.num_children()))


class SimplifyingEvaluator(Evaluator):
    """
    Evaluator that punishes large trees
    """
    def __init__(self, coeff_num_nodes, coeff_depth):
        self.coeff_num_nodes = coeff_num_nodes
        self.coeff_depth = coeff_depth

    def __call__(self, ind):
        num_nodes = ind.g.get_node_number()
        depth = ind.g.get_depth()
        ind.fitness = ind.y +\
            self.coeff_num_nodes * num_nodes +\
            self.coeff_depth * depth
        return ind.fitness


class NodeGenerator:
    def __call__(self, num_children, tag, child_tags=None):
        """

        :param num_children: either a non-negative integer of '>0'
        :param tag: information about the "returned value"
        :param child_tags: tags of children (optional)
            When given, children must have matching tags.
        :return:
        """
        raise NotImplementedError


class GrowTree(NullarySearchOperation):
    def __init__(self, max_depth, root_tag, rand_node):
        """

        :param max_depth: maximum depth of generated tree
        :param root_tag: tag for the root of the tree
        :param rand_node: implements the NodeGenerator interface
        """
        if max_depth < 1:
            raise Exception("Depth must be positive (given " +
                            str(max_depth) + ")")
        self.max_depth = max_depth
        self.root_tag = root_tag
        self.rand_node = rand_node

    def __call__(self):
        if self.max_depth == 1:
            return self.rand_node(0, self.root_tag)
        else:
            nonterminal = self.rand_node('>0', self.root_tag)
            for i in range(nonterminal.num_children()):
                child_tag = nonterminal.get_child_tag(i)
                child_grower = GrowTree(self.max_depth - 1,
                                        child_tag,
                                        self.rand_node)
                nonterminal.set_child(i, child_grower())

            return nonterminal


class NodeSingleSwap(UnarySearchOperation):
    """
    Root-preserving swapping of a single subtree
    """
    def __init__(self, rand_node):
        self.rand_node = rand_node

    def recursive_replace(self, parent_tree, distance_to_root):
        num_nodes = parent_tree.get_node_number()
        choices = [-1] + list(range(parent_tree.num_children()))
        probabilities = [1.0/num_nodes] +\
                        [parent_tree.get_child(i).get_node_number()/num_nodes
                         for i in range(parent_tree.num_children())]
        selected = int(np.random.choice(choices,
                                        1,
                                        p=probabilities)[0])
        if selected == -1:
            # whole subtree or node type?
            if distance_to_root > 0 and random.choice([True, False]):
                # whole subtree
                max_depth = parent_tree.get_depth()
                grower = GrowTree(max_depth,
                                  parent_tree.get_tag(),
                                  self.rand_node)
                return grower()
            else:
                # just node
                new_node = self.rand_node(parent_tree.num_children(),
                                          parent_tree.get_tag(),
                                          parent_tree.get_child_tags())
                for i in range(parent_tree.num_children()):
                    new_node.set_child(i, parent_tree.get_child(i))
                return new_node
        else:
            new_tree = deepcopy(parent_tree)
            replacement = self.recursive_replace(new_tree.get_child(selected),
                                                 distance_to_root + 1)
            new_tree.set_child(selected, replacement)
            return new_tree

    def __call__(self, parent):
        return self.recursive_replace(parent.g, 0)
