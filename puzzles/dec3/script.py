from pathlib import Path
from typing import Sequence


def item_priority(item: str) -> int:
    """ Return the priority of the item """
    return 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.find(item) + 1


def item_type(line: str) -> str:
    """ Return the item type that is represented in both compartments of the rucksack """
    line = line.strip('\n')
    n = len(line) / 2
    assert n == round(n), f'Unexpected input size: {len(line)} ("{line}")'
    n = int(n)
    left, right = line[:n], line[n:]
    common = set(left) & set(right)
    assert len(common) == 1
    return list(common)[0]


def badge_types(lines: Sequence[str]) -> Sequence[str]:
    """ Return the badge types common between groups of three elves """
    counter = 0
    common_items: None | set[str] = None
    for line in lines:
        items = set(line.strip('\n'))
        if common_items is not None:
            common_items &= items
        else:
            common_items = items
        counter += 1
        if counter == 3:
            counter = 0
            # Check only one item in common
            assert len(common_items) == 1
            yield list(common_items)[0]
            common_items = None

    # Check that lines were counted in even groups of 3
    assert counter == 0


if __name__ == '__main__':

    with Path('input.txt').open('r') as input_file:
        input_lines = input_file.readlines()

    # Part 1
    result = sum([item_priority(item_type(line)) for line in input_lines])
    print(f'Part 1: {result}')

    # Part 2
    result = sum([item_priority(badge) for badge in badge_types(input_lines)])
    print(f'Part 2: {result}')


def test_item_priority() -> None:
    """ Test values returned by item_priority() function """
    assert item_priority('a') == 1
    assert item_priority('A') == 27
    assert item_priority('Z') == 52
