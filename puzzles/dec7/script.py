from itertools import chain
from collections import OrderedDict
from pathlib import Path
import re
from typing import Generator, Iterator, Iterable


def read_input(path: None | Path = None) -> Generator[str, None, None]:
    """ Read input lines """
    path = path or Path('input.txt')

    with path.open('r') as input_file:
        for line in input_file:
            yield line.strip('\n')


class Node:

    def __init__(self, name: str, value: int = 0, children: Iterable['Node'] | None = None):
        self.__name = name
        self.__value = value
        self.__children = children or []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def value(self) -> int:
        return self.__value + sum(n.value for n in self.__children)

    @property
    def children(self) -> Iterable['Node']:
        return self.__children

    def __iter__(self):
        return chain(*[iter(n) for n in self.children], [self])

    def __repr__(self):
        return ('Node{name=' + repr(self.__name) + ',' +
                'value=' + repr(self.__value) + ',' +
                'children=[' + ','.join(repr(n) for n in self.__children) + ']}')

    def __eq__(self, other: 'Node'):
        return (self.__name == other.__name and
                self.__value == other.__value and
                tuple(self.__children) == tuple(other.__children))

    def __hash__(self):
        return hash((self.__name, self.__value) + tuple(self.__children))


class Dir(Node):
    """ Directory (children only, no size) """
    def __init__(self, name: str, children: Iterable['Node']):
        super().__init__(name, value=0, children=children)


class File(Node):
    """ File (size only, no children) """
    def __init__(self, name: str, value: int):
        super().__init__(name, value=value, children=None)


def ls(lines: Iterator[str]) -> tuple[Iterator[str], Iterator[str]]:
    """ Parse ls output (lines that don't start with $) and return tuple(command output, remaining lines) """
    result = []
    for line in lines:
        if line.startswith('$'):
            return iter(result), chain([line], lines)  # Chain line back together with remaining lines
        else:
            result.append(line)

    return iter(result), iter([])


def cd(lines: Iterator[str]) -> tuple[Iterator[str], Iterator[str]]:
    """ Parse cd (all lines that occur within a subdir) and return tuple(lines in subdir, remaining lines) """
    result = []
    level = 1
    for line in lines:
        if (match := re.match('^\$\scd\s(/|[a-z]+|\.\.)$', line)) is not None:
            dirname = match.group(1)
            if dirname == '..':
                level -= 1
                if level == 0:
                    return iter(result), lines
            else:
                level += 1

        result.append(line)

    return iter(result), iter([])


def parse_dir(name: str, lines: Iterator[str]) -> 'Node':
    """ Parse directory output (i.e. ls + visit each subdir) """
    # '$ ls'
    try:
        line = next(lines)
    except StopIteration:
        print('Fuck')
    assert re.match(r'^\$\sls$', line) is not None

    children: dict[str, None | Node] = OrderedDict()

    # ls output
    ls_out, lines = ls(lines)
    for line in ls_out:
        if (match := re.match(r'^dir\s(/|[.a-z]+)$', line)) is not None:
            # Dir
            dir_name = match.group(1)
            children[dir_name] = None
        elif (match := re.match(r'^([1-9][0-9]*)\s(/|[.a-z]+)$', line)) is not None:
            # File
            file_size = int(match.group(1))
            file_name = match.group(2)
            children[file_name] = File(file_name, file_size)
        else:
            raise ValueError(f'Unparseable line: "{line}"')

    # Remaining output: visit directories
    for line in lines:
        if (match := re.match(r'^\$\scd\s(/|[.a-z]+)$', line)) is not None:
            # cd into dir
            dir_name = match.group(1)
            dir_lines, lines = cd(lines)
            children[dir_name] = parse_dir(dir_name, dir_lines)
        else:
            raise ValueError(f'Unparseable line: "{line}"')

    for k, v in children.items():
        assert v is not None, f'No dir info: "{k}"'

    return Dir(name, children.values())


if __name__ == '__main__':

    lines = read_input()
    assert next(lines) == '$ cd /'
    tree = parse_dir('/', lines)

    # Part 1
    result = sum([node.value for node in tree if isinstance(node, Dir) and node.value <= 100000])
    print(f'Part 1: {result}')

    # Part 2
    space_needed = 30000000 - (70000000 - tree.value)
    dir_to_delete = sorted([node for node in tree if isinstance(node, Dir) and node.value >= space_needed],
                           key=lambda node: node.value)[0]
    result = dir_to_delete.value
    print(f'Part 2: {result}')


def test_parse() -> None:
    """ Test simple case """
    output = [
        # '$ cd /',
        '$ ls',
        'dir a',
        '1 d.txt',
        'dir e',
        '$ cd a',
        '$ ls',
        '2 b.txt',
        '3 c.txt',
        '$ cd ..',
        '$ cd e',
        '$ ls',
        '5 f',
    ]

    tree = parse_dir('/', iter(output))

    assert tree == Dir('/', (
        Dir('a', (
            File('b.txt', 2),
            File('c.txt', 3),
        )),
        File('d.txt', 1),
        Dir('e', (
            File('f', 5),
        ))
    ))
