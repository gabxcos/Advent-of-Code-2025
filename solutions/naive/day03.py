from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class BankSplitter(BaseLinesSplitter):
    def split(self):
        return [[int(ch) for ch in line] for line in self.lines]
    
def solve_bank(bank: list[int]) -> int:
    digits = sorted(set(bank), reverse=True)
    for i in range(len(digits)-1):
        for j in range(len(digits)):
            a = digits[i]
            b = digits[j]
            pos_a = bank.index(a)
            try:
                _ = bank[pos_a+1:].index(b)
                return int(str(a)+str(b))
            except ValueError:
                continue
    raise Exception("No joltage was computed")


class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=3, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = BankSplitter(self.test_data).split()
        self.data = BankSplitter(self.data).split()

    def part_1(self, data):
        s = 0
        for bank in data:
            str_bank = "".join([str(el) for el in bank])
            jolt = solve_bank(bank=bank)
            self.logger.debug(f"Bank {str_bank} -> Jolt {jolt}")
            s+=jolt
        return s
    
    def part_2(self, data):
        pass