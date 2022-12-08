from pathlib import Path
from typing import Generator


def read_input(path: None | Path = None) -> Generator[str, None, None]:
    """ Read input lines """
    path = path or Path('input.txt')

    with path.open('r') as input_file:
        for line in input_file:
            yield line.strip('\n')


def parse_range(range_str: str) -> range:
    """ Parse inclusive range string, e.g. '2-6' -> range(2, 7) """
    return range(*tuple(int(s) for s in range_str.split('-')))


def is_overlap(line: str, partial: bool = False) -> bool:
    """ Check if one set is completely contained within the other """
    left, right = tuple(parse_range(s) for s in line.split(','))
    if partial:
        return left.start <= right.stop and left.stop >= right.start
    else:
        return (left.start >= right.start and left.stop <= right.stop) or \
            (left.start <= right.start and left.stop >= right.stop)


if __name__ == '__main__':

    # Part 1
    result = sum(is_overlap(line) for line in read_input())
    print(f'Part 1: {result}')

    # Part 2
    result = sum(is_overlap(line, partial=True) for line in read_input())
    print(f'Part 2: {result}')


def test_is_overlap() -> None:
    """ Test whether there is overlap between ranges """

    # Part 1
    assert is_overlap('2-8,3-7')
    assert is_overlap('3-7,2-8')
    assert not is_overlap('2-4,6-8')
    assert not is_overlap('4-8,2-6')
    assert is_overlap('6-6,4-6')
    assert not is_overlap('1-1,2-2')

    # Part 2
    assert is_overlap('5-7,7-9', partial=True)
    assert is_overlap('2-8,3-7', partial=True)
    assert is_overlap('6-6,4-6', partial=True)
    assert is_overlap('2-6,4-8', partial=True)
    assert not is_overlap('2-4,6-8', partial=True)
    assert is_overlap('2-6,6-8', partial=True)
    assert is_overlap('6-8,2-6', partial=True)
    assert is_overlap('1-1,1-1', partial=True)
    assert not is_overlap('1-1,2-2', partial=True)
