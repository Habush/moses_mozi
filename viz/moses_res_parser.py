__author_ = 'Xabush Semrie'

from anytree.exporter import JsonExporter
from lark import Lark

grammer = r"""
    
        model: "(EquivalenceLink (stv 1.0 1.0)" "(" "PredicateNode" mname ")" func ")" 
        
        func: lpar func_name param+ rpar
        
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

moses_parser = Lark(grammer, start='model', parser="lalr")







text = """(EquivalenceLink (stv 1.0 1.0)
    (PredicateNode "temp_file_5a757b012ae73d5ddf306289:moses_model_10")
    (OrLink (AndLink (OrLink (NotLink (PredicateNode "PRR14L")) (PredicateNode "RUNX2")) (NotLink (PredicateNode "SCFD2")) (NotLink (PredicateNode "TRIO.1"))) (AndLink (PredicateNode "TRIO.1") (NotLink (PredicateNode "PRR14L")))))"""

text2 = """(EquivalenceLink (stv 1.0 1.0)
    (PredicateNode "moses_model_00")
    (AndLink (NotLink (PredicateNode "SCFD2")) (PredicateNode "TRIO.1") (NotLink (PredicateNode "PRR14L"))))"""

text3 = """(EquivalenceLink (stv 1.0 1.0)
    (PredicateNode "temp_file_5a757b012ae73d5ddf306289:moses_model_02")
    (AndLink (OrLink (NotLink (PredicateNode "SCFD21")) (PredicateNode "TRIO.12")) (NotLink (PredicateNode "PRR14L2"))))"""

text4 = """(EquivalenceLink (stv 1.0 1.0)
    (PredicateNode "moses_model_10")
    (OrLink (AndLink (OrLink (NotLink (PredicateNode "PRR14L")) (PredicateNode "RUNX2")) (NotLink (PredicateNode "SCFD2")) (NotLink (PredicateNode "TRIO.1"))) (AndLink (PredicateNode "TRIO.1") (NotLink (PredicateNode "PRR14L")))))"""

if __name__ == "__main__":
    tree = moses_parser.parse(text4)

    moses = MosesTree()
    tree = moses.transform(tree)

    exporter = JsonExporter(indent=0)

    print(exporter.export(moses.root))
