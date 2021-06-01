from json import dumps, JSONEncoder, loads

from MathLang.Core.nodes import *


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
    """Serialises MathLang AST to JSON. This function is dangerous and used for debugging purposes only."""
    return dumps(ast, cls=ASTSerialiser)


def deserialise_ast(d: str) -> AST:
    """Deserialises JSON to MathLang AST. This function is dangerous and used for debugging purposes only."""
    return loads(d, object_hook=json_decode_hook)
