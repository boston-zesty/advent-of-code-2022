from enum import IntEnum
from pathlib import Path


class Move(IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3

    def vs(self, other: 'Move') -> int:
        """ Determine outcome of round (-1: loss, 0: draw, 1: win) """
        return (((self.value - other.value) + 4) % 3) - 1

    def has_outcome(self, outcome: int) -> 'Move':
        """ Determine opponent's move from outcome of round (-1: loss, 0: draw, 1: win) """
        return Move(((int(self) - outcome + 2) % 3) + 1)


def score_round_pt1(line: str) -> int:
    """ Score a round of rock, paper, scissors """
    his_code, my_code = line.split()

    his = Move('ABC'.find(his_code) + 1)
    mine = Move('XYZ'.find(my_code) + 1)

    return (1 + mine.vs(his)) * 3 + int(mine)


def score_round_pt2(line: str) -> int:
    """ Score a round of rock, paper, scissors """
    his_code, outcome_code = line.split()

    his = Move('ABC'.find(his_code) + 1)
    outcome = 'XYZ'.find(outcome_code) - 1

    return (outcome + 1) * 3 + int(his.has_outcome(outcome * -1))


if __name__ == '__main__':

    with Path('input.txt').open('r') as input_file:
        input_lines = input_file.readlines()

    # Part 1
    result = sum([score_round_pt1(line) for line in input_lines])
    print(f'Part 1: {result}')

    # Part 2
    result = sum([score_round_pt2(line) for line in input_lines])
    print(f'Part 2: {result}')


def test_moves() -> None:
    """ Test outcomes of moves """
    assert Move.Rock.vs(Move.Rock) == 0
    assert Move.Rock.vs(Move.Paper) == -1
    assert Move.Rock.vs(Move.Scissors) == 1
    assert Move.Paper.vs(Move.Rock) == 1
    assert Move.Paper.vs(Move.Scissors) == -1
    assert Move.Scissors.vs(Move.Rock) == -1
    assert Move.Scissors.vs(Move.Paper) == 1

    assert Move.Rock.has_outcome(-1) == Move.Paper
    assert Move.Rock.has_outcome(0) == Move.Rock
    assert Move.Rock.has_outcome(1) == Move.Scissors
    assert Move.Paper.has_outcome(-1) == Move.Scissors
    assert Move.Paper.has_outcome(1) == Move.Rock
    assert Move.Scissors.has_outcome(-1) == Move.Rock
    assert Move.Scissors.has_outcome(1) == Move.Paper
