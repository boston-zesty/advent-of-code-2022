from pathlib import Path
from typing import Generator


def sum_calories(lines: list[str]) -> Generator[int, None, None]:
    """ Yield sums of calories by elf. """
    calories = 0
    for line in lines:
        line = line[:-1]  # Strip '\n'
        if line != '':
            calories += int(line)
        else:
            yield calories
            calories = 0


if __name__ == '__main__':

    with Path('input.txt').open('r') as input_file:
        input_lines = input_file.readlines()

    # Part 1
    result = max(sum_calories(input_lines))
    print(f'Part 1: {result}')

    # Part 2
    elves = sorted(list(sum_calories(input_lines)))
    result = sum(elves[-3:])
    print(f'Part 2: {result}')
