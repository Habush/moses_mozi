from lark import Lark, Transformer

class TreeToJson(Transformer):
    def string(self, (s,)):
        return s[1:-1]

    def number(self, (n,)):
        return float(n)

    list = list
    pair = tuple
    dict = dict

    null = lambda self, _: None
    true = lambda self, _: True
    false = lambda  self, _: False





json_grammer = r"""
    ?value: dict
        | list
        | string
        | SIGNED_NUMBER -> number
        | "true" -> true
        | "false" -> false
        | "null" -> null
        
    list: "[" [value ("," value)*] "]"
    
    dict: "{" [pair ("," pair)*] "}"
    
    pair: ESCAPED_STRING ":" value
    
    string: ESCAPED_STRING
    
    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS
"""

json_parser = Lark(json_grammer, start='value')


if __name__ == "__main__":
    text = '{"key": ["item0", "item1", 3.14]}'

    tree = json_parser.parse(text)

    print(TreeToJson().transform(tree))