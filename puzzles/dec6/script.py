from pathlib import Path
from typing import Generator


def read_input(path: None | Path = None) -> Generator[str, None, None]:
    """ Read input lines """
    path = path or Path('input.txt')

    with path.open('r') as input_file:
        for line in input_file:
            yield line.strip('\n')


def find_distinct_chars(buffer: str, n: int = 4) -> int:
    """ Return index of first char after start-of-packet marker """
    seq: list[str] = []
    for i, char in enumerate(buffer):
        if len(seq) == n:
            seq = seq[1:]
            seq.append(char)
            if len(set(seq)) == n:
                return i + 1
        else:
            seq.append(char)

    raise ValueError('Start-of-packet marker not found')


if __name__ == '__main__':

    # Part 1
    line = list(read_input())[0]
    result = find_distinct_chars(line)
    print(f'Part 1: "{result}"')

    # Part 2
    line = list(read_input())[0]
    result = find_distinct_chars(line, n=14)
    print(f'Part 2: "{result}"')
