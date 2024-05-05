# Specify syntax higlighting theme in IPython;
# will be picked up by prettyprinter.
from pygments import styles

from prettyprinter.color import GitHubLightStyle

def light_theme():
    """For light terminal backgrounds."""
    ipy = get_ipython()
    ipy.colors = 'LightBG'
    ipy.highlighting_style = GitHubLightStyle


def dark_theme():
    """For dark terminal background."""
    ipy = get_ipython()
    ipy.colors = 'linux'
    ipy.highlighting_style = styles.get_style_by_name('monokai')

import prettyprinter

dark_theme()

prettyprinter.install_extras(
    # Comment out any packages you are not using.
    include=[
        'ipython',
        'ipython_repr_pretty',
        'attrs',
        'django',
        'requests',
        'dataclasses',
    ],
    exclude=['django', 'attrs'],
    warn_on_error=True,
)

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
