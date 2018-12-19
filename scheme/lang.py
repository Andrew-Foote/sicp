import string
import typing as t

class SchemeToken(t.NamedTuple('SchemeToken', [
    ('s', str),
    ('i', int),
])):
    """A Scheme token.

    Attributes:
        s - the content of the token.
        i - the index within the source code of the last character in
        the token.
    """

def lex(s: str) -> t.Iterator[SchemeToken]:
    """Lex a string of Scheme source code, returning an iterator over
    its tokens."""
    token: t.List[str] = []

    def flush(i: int) -> t.Iterator[SchemeToken]:
        if token:
            yield SchemeToken(s=''.join(token), i=i)
            token.clear()

    for i, c in enumerate(s):
        if c in string.whitespace:
            yield from flush(i)
        elif c in ('(', ')'):
            yield from flush(i)
            yield SchemeToken(s=c, i=i)
        else:
            token.append(c)

    yield from flush(i)

class SchemeError(Exception):
    """An error in a Scheme program.

    Attributes:
        i - the index within the source code at which the error was
        detected, or None if it was detected only after parsing.
    """
    i: t.Optional[int]

    def __init__(self, message, i: int=None):
        super().__init__(message)
        self.i = i

StrTree = t.Union[str, t.List['StrTree']]

def parse(tokens: t.Iterable[SchemeToken]) -> StrTree:
    """Parse an iterable of Scheme tokens, returning a concrete syntax
    tree.

    Raises `SchemeError` if there are unmatched parentheses."""
    trees: t.List[t.List[StrTree]] = [[]]

    for token in tokens:
        if token.s == '(':
            trees.append([])
        elif token.s == ')':
            tree: t.List[StrTree] = trees.pop()

            try:
                trees[-1].append(tree)
            except IndexError:
                raise SchemeError('unmatched closing parenthesis', token.i)
        else:
            trees[-1].append(token.s)

    if len(trees) > 1:
        raise SchemeError('{} unmatched opening parenthes{}s'
            .format(len(trees) - 1, ('i', 'e')[len(trees) > 1]))

    return trees[0]