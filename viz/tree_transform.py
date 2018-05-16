__author_ = 'Xabush Semrie'

from lark.tree import Transformer
from anytree import Node, RenderTree


class MosesTree(Transformer):
    def __init__(self):
        self.par_stack = []
        self.root = None
        self.curr = None
        self.res_tree = None
        self.nodes = []

    def mname(self, s):
        self.root = Node(name=s[0])
        self.curr = self.root
        self.nodes.append(self.curr)

    def lpar(self, args):
        self.curr = Node(name="", parent=self.curr)
        self.nodes.append(self.curr)

    def rpar(self, args):
        self.nodes.pop()
        self.curr = self.nodes[-1]


    def func_name(self, s):
        self.curr.name = s
        return self.curr

    def name(self, s):
        self.curr = self.nodes[-1]
        return Node(name=s[0], parent=self.curr)

    def transform(self, tree):
        super(MosesTree, self).transform(tree)
        self.res_tree = RenderTree(self.root)
