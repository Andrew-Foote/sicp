import sys
from lang import lex, parse, SchemeError

SNIPPET_SIZE = 36

if __name__ == '__main__':
    while True:
        print('>', end=' ')
        s: str = input()

        if s == 'exit':
            sys.exit()
        
        try:
            print(parse(lex(s)))
        except SchemeError as error:
            if error.i is not None:
                snippet: str = s[error.i - SNIPPET_SIZE:error.i + SNIPPET_SIZE]

                if error.i > SNIPPET_SIZE:
                    snippet = '... ' + snippet
                    snippet_i = 4 + SNIPPET_SIZE
                else:
                    snippet_i = error.i

                if error.i < len(s) - SNIPPET_SIZE:
                    snippet = snippet + ' ...'
                snippet = '  ' + snippet
                snippet_i += 2
                print(snippet)
                print(' ' * snippet_i + '^')

            print('Error{}: {}'.format(
                ('' if error.i is None else f' at index {error.i}'),
                error
            ))