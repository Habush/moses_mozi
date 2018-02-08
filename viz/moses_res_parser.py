from anytree import Node, RenderTree
from anytree.exporter import JsonExporter
from lark import Lark
from lark.lexer import Token
from lark.tree import Transformer, Tree

moses_result_grammer = r"""
    
        model: "(EquivalenceLink (stv 1.0 1.0)" "(" "PredicateNode" mname ")" func ")" 
        
        func:"(" func_name param+ ")"
        
        param: "(" "PredicateNode" name ")" | func
        
        func_name: WORD
        
        param_name: "PredicateNode" name
        
        name: ESCAPED_STRING+ | WORD
        mname: ESCAPED_STRING+
        
        
        %import common.ESCAPED_STRING
        %import common.WORD
        %import common.WS
        %import common.NUMBER
        %ignore WS
"""

moses_parser = Lark(moses_result_grammer, start='model', parser="lalr")


class MosesTree(Transformer):
    def __init__(self):
        self.par_stack = []
        self.root = None
        self.curr = None
        self.res_tree = None
        self.nodes = []

    def func(self, args):
        self.curr = Node(name="", parent=self.curr)
        self.nodes.append(self.curr)

    def func_name(self, (s, )):
        self.curr.name = s

    def mname(self, (s, )):
        self.root = Node(name=s)
        self.curr = self.root
        self.nodes.append(self.curr)

    def param(self, args):
        self.curr = Node(name="", parent=self.curr)
        self.nodes.append(self.curr)

    def param_name(self, args):
        self.curr = Node(name="", parent=self.curr)
        self.nodes.append(self.curr)

    def name(self, (s, )):
        node = Node(name=s, parent=self.curr)

    def transform(self, tree):
        super(MosesTree, self).transform(tree)
        self.res_tree = RenderTree(self.root)


def bfs_travesal(tree):
    explored = []
    node_explored = []

    queue = [tree]
    node_queue = [Node(name="root", parent=None)]
    i = flag = False
    prev = None
    while len(queue) > 0:
        node = queue.pop(0)
        k = node_queue[-1]

        if node not in explored:
            explored.append(node)
            try:
                children = node.children

                for child in children:
                    if isinstance(child, Token):
                        name = child.value
                    else:
                        name = child.data
                    node_queue.append(Node(name, parent=k))
                    queue.append(child)
            except AttributeError:
                continue

    return node_queue


tbd_nodes = ["param", "func", "param_name"]


def _pretty_label(tree):
    # if tree.data in tbd_nodes:
    #     return "*"
    return tree.data


def traverse(tree, parent):
    if len(tree.children) == 1 and not isinstance(tree.children[0], Tree):
        return [Node(name=tree.children[0], parent=parent)]

    l = Node(name=_pretty_label(tree), parent=parent)
    bucket = [l]
    for n in tree.children:
        if isinstance(n, Tree):
            bucket += traverse(n, l)

    return bucket


def delete_node(tree):
    if len(tree.children) == 0:
        return [tree]
    if tree.name == "*":
        temp = []
        for node in tree.children:
            node.parent = tree.parent
            temp += [node]
        tree.parent = None
        return temp
    else:
        bucket = [tree]
        for node in tree.children:
            bucket += delete_node(node)
        return bucket

text = """(EquivalenceLink (stv 1.0 1.0)
    (PredicateNode "temp_file_5a757b012ae73d5ddf306289:moses_model_10")
    (OrLink (AndLink (OrLink (NotLink (PredicateNode "PRR14L")) (PredicateNode "RUNX2")) (NotLink (PredicateNode "SCFD2")) (NotLink (PredicateNode "TRIO.1"))) (AndLink (PredicateNode "TRIO.1") (NotLink (PredicateNode "PRR14L")))))"""

text2 = """(EquivalenceLink (stv 1.0 1.0)
    (PredicateNode "moses_model_00")
    (AndLink (NotLink (PredicateNode "SCFD2")) (PredicateNode "TRIO.1") (NotLink (PredicateNode "PRR14L"))))"""

if __name__ == "__main__":
    tree = moses_parser.parse(text2)

    # moses = MosesTree()
    # tree = moses.transform(tree)
    # for pre, fill, node in moses.res_tree:
    #         print("%s%s" % (pre, node.name))

    # print(tree.pretty())
    # result = bfs_travesal(tree)
    # print result
    root = Node(name="root", parent=None)

    nodes = traverse(tree, root)

    # nodes = delete_node(nodes.pop(0))
    exporter = JsonExporter(indent=0)
    re_tree = RenderTree(nodes.pop(0))
    for pre, fill, node in re_tree:
            print("%s%s" % (pre, node.name))

    # print(exporter.export(nodes.pop(0)))
