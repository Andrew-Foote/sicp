import sys
import typing as t

if __name__ == '__main__':
    while True:
        print('>', end=' ')
        s: str = input()

        if s == 'exit':
            sys.exit()
        
        print(s)
