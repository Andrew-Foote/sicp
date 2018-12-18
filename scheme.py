import string
import sys
import typing as t

def lex(s: str) -> t.Iterator[str]:
    """Lex a string of Scheme source code, returning an iterator over
    its tokens."""
    token: t.List[str] = []

    def flush() -> t.Iterator[str]:
        if token:
            yield ''.join(token)
            token.clear()

    for c in s:
        if c in string.whitespace:
            yield from flush()
        elif c in ('(', ')'):
            yield from flush()
            yield c
        else:
            token.append(c)

    yield from flush()

class SchemeError(Exception):
    pass

StrTree = t.Union[str, t.List['StrTree']]

def parse(tokens: t.Iterable[str]) -> StrTree:
    """Parse an iterable of Scheme tokens, returning a concrete syntax
    tree.

    Raises `SchemeError` if there are unmatched parentheses."""
    trees: t.List[t.List[StrTree]] = [[]]

    for token in tokens:
        if token == '(':
            trees.append([])
        elif token == ')':
            tree: t.List[StrTree] = trees.pop()

            try:
                trees[-1].append(tree)
            except IndexError:
                raise SchemeError('unmatched closing parenthesis')
        else:
            trees[-1].append(token)

    if len(trees) > 1:
        raise SchemeError('unmatched opening parenthesis')

    return trees[0]

if __name__ == '__main__':
    while True:
        print('>', end=' ')
        s: str = input()

        if s == 'exit':
            sys.exit()
        
        try:
            print(parse(lex(s)))
        except SchemeError as error:
            print(f'Error: {error}')