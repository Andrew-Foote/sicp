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

if __name__ == '__main__':
    while True:
        print('>', end=' ')
        s: str = input()

        if s == 'exit':
            sys.exit()
        
        print(' '.join(lex(s)))
