import re
from collections import defaultdict
from grammar import Grammar
from utils import slugify, deslugify

class Node:
    def __init__(self):

        self.parent = None
        self.tag = ''
        self.tag_parsed = False
        self.children = []

    def descend(self, callback):

        callback(self)
        for child in self.children:
            child.descend(callback)

    def is_leaf(self): return False

class Leaf:
    def __init__(self):

        self.parent = None
        self.text = ''

    def descend(self, callback):
        callback(self)

    def is_leaf(self): return True

def induce(parsed_sents):

    def get_rule_from_node(node):

        if not node.is_leaf():

            child_tags = []

            for child in node.children:

                if child.is_leaf():
                    leafs[node.tag].add(child.text)

                else:
                    child_tags.append(child.tag)

            if len(child_tags):

                key = slugify(child_tags)
                nodes[node.tag].add(key)
    
    g = Grammar()

    for parsed_sent in parsed_sents:

        root = Node()
        current = root

        for char in str(parsed_sent):

            if char == '(':

                child = Node()
                child.parent = current

                current.children.append(child)
                current = child

            elif char == ')':

                if isinstance(current, Leaf):
                    current = current.parent
                current = current.parent

            elif re.match(r'\s', char):
                current.tag_parsed = True

            else:

                if isinstance(current, Leaf):

                    current.text += char

                elif current.tag_parsed:

                    leaf = Leaf()
                    leaf.parent = current
                    leaf.text += char

                    current.children.append(leaf)
                    current = leaf

                else:

                    current.tag += char
            
        leafs = defaultdict(set)
        nodes = defaultdict(set)

        root.children[0].descend(get_rule_from_node)

        for (src, tar_set) in nodes.items():
            for slugged_tars in tar_set:

                tars = deslugify(slugged_tars)
                g.add_rule(src, tars, False)

        for (src, tars) in leafs.items():
            g.add_rule(src, tars, True)

         
    g.dedup()
    return g

