import re
from pathlib import Path
from typing import Generator, Iterator


def read_input(path: None | Path = None) -> Generator[str, None, None]:
    """ Read input lines """
    path = path or Path('input.txt')

    with path.open('r') as input_file:
        for line in input_file:
            yield line.strip('\n')


def init_stacks(input_lines: Iterator[str]) -> dict[int, list[str]]:
    """ Read first lines of input file and return initialized stacks """

    item_rows: list[list[None | str]] = []

    stacks: dict[int, list[str]] = {}

    # Build a stack for stacking the stacks
    while (line := next(input_lines)) != '':
        if re.match(r'((^|\s)(\[[A-Z]\]|\s{3}))*$', line) is not None:
            row = []
            for _match in re.finditer(r'((^|\s)(\[[A-Z]\]|\s{3}))', line):
                if (_item_match := re.search(r'[A-Z]', _match.group())) is not None:
                    row.append(_item_match.group())
                else:
                    row.append(None)
            item_rows.append(row)
        elif re.match(r'^\s[1-9]\s(\s\s[1-9]\s)+$', line) is not None:
            for i, g in enumerate(re.findall(r'[1-9]', line)):
                assert int(g) == i + 1
                stacks[i + 1] = list()
        else:
            raise ValueError(f'Invalid line: "{line}"')

    # Stack the stacks
    for row in reversed(item_rows):
        for i, item in enumerate(row):
            if item is not None:
                stacks[i + 1].append(item)

    return stacks


def parse_move(line: str) -> tuple[int, int, int]:
    """ Parse move instruction. Return tuple of (num, src, dst). """
    # noinspection PyShadowingNames
    num, src, dst = tuple(int(s) for s in re.search(r'move ([0-9]+) from ([0-9]) to ([0-9])', line).groups())
    return num, src, dst


if __name__ == '__main__':

    # Part 1
    lines = read_input()
    stacks = init_stacks(lines)
    for line in lines:
        num, src, dst = parse_move(line)
        for _ in range(num):
            stacks[dst].append(stacks[src].pop())

    result = ''.join(stacks[i + 1][-1] for i in range(len(stacks)))
    print(f'Part 1: "{result}"')

    # Part 2
    lines = read_input()
    stacks = init_stacks(lines)
    for line in lines:
        num, src, dst = parse_move(line)
        stacks[dst].extend(stacks[src][-num:])
        stacks[src] = stacks[src][:-num]

    result = ''.join(stacks[i + 1][-1] for i in range(len(stacks)))
    print(f'Part 2: "{result}"')
