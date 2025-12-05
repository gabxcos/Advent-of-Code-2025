import os

def puzzle_read(day_string: str, test: bool = False) -> list[str]:
    path = os.path.abspath(f"inputs/{'test' if test else 'puzzle'}/{day_string}")
    with open(path, "r") as f:
        lines = [line.replace("\n","") for line in f.readlines()]
    return lines

class BaseLinesSplitter():
    def __init__(self, lines: list[str]):
        self.lines = lines

    def split(self):
        return [list(line) for line in self.lines]