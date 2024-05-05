from types import FunctionType
from prettyprinter import register_pretty
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalTrueColorFormatter, Terminal256Formatter, TerminalFormatter
from inspect import getsource

@register_pretty(FunctionType)
def pretty_function(value, ctx):
    return highlight(
        getsource(value),
        lexer=PythonLexer(),
        formatter=TerminalTrueColorFormatter(),
    )
