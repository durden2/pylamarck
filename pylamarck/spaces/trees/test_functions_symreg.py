from pylamarck.spaces.trees.production import Node, NodeGenerator
import random
import math
import numpy as np


class SymbolicNode(Node):
    def __init__(self, tag, child_tags, evaluator, print_name, child_nodes=None):
        self.tag = tag
        self.child_tags = child_tags
        self.evaluator = evaluator
        if child_nodes is None:
            self.child_nodes = [None for _ in range(len(child_tags))]
        else:
            self.child_nodes = child_nodes
        if not isinstance(print_name, str):
            raise ValueError("print_name must be a str")
        self.print_name = print_name

    def get_tag(self):
        return self.tag

    def get_child_tag(self, child_num):
        return self.child_tags[child_num]

    def get_child_tags(self):
        return self.child_tags

    def get_child(self, child_num):
        return self.child_nodes[child_num]

    def num_children(self):
        return len(self.child_nodes)

    def set_child(self, child_num, node):
        if node.get_tag() == self.get_child_tag(child_num):
            self.child_nodes[child_num] = node
        else:
            raise Exception("Incompatible tags: " + node.get_tag() +
                            " and " + self.get_child_tag(child_num))

    def evaluate(self, variables):
        """

        :param variables: variable assignments
        :return:
        """
        if len(self.child_nodes) == 0:
            return self.evaluator(variables)
        else:
            child_values = [child_node.evaluate(variables)
                            for child_node in self.child_nodes]
            return self.evaluator(*child_values)

    def print_expression(self):
        ret = self.print_name
        if len(self.child_nodes) > 0:
            ret += '('
            for i, child in enumerate(self.child_nodes):
                ret += child.print_expression()
                if i < len(self.child_nodes)-1:
                    ret += ', '
            ret += ')'

        return ret


class SymbolicNodeGenerator(NodeGenerator):
    def __init__(self, float_var_names, int_var_names):
        self.float_var_names = float_var_names
        self.int_var_names = int_var_names

    def __call__(self, num_children, tag, child_tags=None):
        if num_children == 0:
            name = '?'
            if tag == 'float':
                if len(self.float_var_names) > 0 and \
                        np.random.choice([True, False], p=[0.75, 0.25]):
                    name = random.choice(self.float_var_names)

                    def evaluator(variables):
                        return variables[name]
                else:
                    val = random.uniform(0, 1)
                    name = str(val)

                    def evaluator(_):
                        return val
            elif tag == 'int':
                if len(self.int_var_names) > 0 and \
                        np.random.choice([True, False], p=[0.75, 0.25]):
                    name = random.choice(self.int_var_names)

                    def evaluator(variables):
                        return variables[name]
                else:
                    val = random.randint(0, 5)
                    name = str(val)

                    def evaluator(_):
                        return val
            else:
                raise Exception("Unknown tag: " + tag)
            return SymbolicNode(tag, [], evaluator, name)
        elif num_children == '>0':
            num_children = random.randint(1, 2)

        # nodes_per_children[num_children][tag]:
        #   (evaluator function, child_tags]
        nodes_per_children = {
            1: {'float': [(math.sin, ['float'], 'sin'),
                          (math.cos, ['float'], 'cos'),
                          (math.tan, ['float'], 'tan'),
                          (math.exp, ['float'], 'exp'),
                          (float, ['int'], 'float')],
                'int': [(abs, ['int'], 'abs')]},
            2: {'float': [(pow, ['float', 'int'], 'pow'),
                          (lambda x, y: x + y, ['float', 'float'], '+'),
                          (lambda x, y: x * y, ['float', 'float'], '*')],
                'int': [(pow, ['int', 'int'], 'pow'),
                        (lambda x, y: x + y, ['int', 'int'], '+'),
                        (lambda x, y: x * y, ['int', 'int'], '*')]}
        }
        matching_nodes = nodes_per_children[num_children][tag]
        if child_tags is not None:
            matching_nodes = list(filter(lambda x: x[1] == child_tags,
                                         matching_nodes))

        if len(matching_nodes) == 0:
            raise Exception("No matching nodes; parent tag: " + tag +
                            " child tags: " + str(child_tags) +
                            " num_children: " + str(num_children))

        evaluator, selected_child_tags, print_name =\
            random.choice(matching_nodes)
        return SymbolicNode(tag, selected_child_tags, evaluator, print_name)


class UnivariateRegressionProblem:
    def __init__(self, xs, ys):
        self.xs = xs
        self.ys = ys

    def __call__(self, sym_expr):
        try:
            calc_ys = np.array([sym_expr.evaluate({'x': x}) for x in self.xs])
            return np.linalg.norm(self.ys - calc_ys) ** 2
        except (OverflowError, ValueError):
            return math.inf

