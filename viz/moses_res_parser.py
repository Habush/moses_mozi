__author_ = 'Xabush Semrie'

from anytree.exporter import JsonExporter
from lark import Lark
from tree_transform import MosesTree

grammer = r"""
    
        model: "(EquivalenceLink (stv 1.0 1.0)" "(" "PredicateNode" mname ")" func ")" 
        
        func: lpar func_name param+ rpar | lpar param_name rpar
        
        param: "(" param_name ")" | func
        
        func_name: WORD
        
        lpar: "("
        rpar: ")"
        
        param_name: "PredicateNode" name
        
        name: ESCAPED_STRING+
        mname: ESCAPED_STRING+
        
        
        %import common.ESCAPED_STRING
        %import common.WORD
        %import common.WS
        %import common.NUMBER
        %ignore WS
"""


def read_scm_file(path):
    output = []
    in_model = False
    current = ""
    with open(path, 'r') as fp:
        for line in fp:
            if line.rstrip() == ";;end_model":
                in_model =  False
                output.append(current)
                current = ""
            if in_model:
                current += line
            if line.rstrip() == ";;begin_model":
                in_model = True



    return output

def parse_moses_result(path):
    moses_parser = Lark(grammer, start='model', parser="lalr")

    models = read_scm_file(path)
    exporter = JsonExporter(indent=0)

    output = []

    for model in models:
        tree = moses_parser.parse(model.rstrip())
        tree_transformer = MosesTree()
        tree_transformer.transform(tree)
        result = exporter.export(tree_transformer.root)
        output.append(result.strip())

    return output

if __name__ == "__main__":
    test_path = "/home/xabush/mozi_datasets/result/test.scm"

    print(parse_moses_result(test_path)[17])