from json import dumps, JSONEncoder, loads

from Grapher.Core.nodes import *


class ASTSerialiser(JSONEncoder):
    def default(self, o):
        if isinstance(o, AST):
            return o.serialise()
        else:
            raise TypeError(f"Object of type '{type(o)}' is not serialisable")


def json_decode_hook(o):
    obj_list = [
        "Assignment",
        "BinaryOps",
        "Comparison",
        "Evaluation",
        "Plot",
        "Print",
        "Program",
        "Solve",
    ]
    t = o.get("type", None)
    if t is not None and t in obj_list:
        return eval(f"{o['type']}(**(o['params']))")
    return o


def serialise_ast(ast: AST) -> str:
    return dumps(ast, cls=ASTSerialiser)


def deserialise_ast(d: str) -> AST:
    return loads(d, object_hook=json_decode_hook)
