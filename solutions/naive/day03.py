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

def solve_bank_overcharged(bank: list[int]) -> int:
    digits = sorted(set(bank), reverse=True)
    bank_len = len(bank)
    for i in range(len(digits)-1):
        # Initialize first digit
        res_arr = []
        pos_arr = []
        a = digits[i]
        pos_a = bank.index(a)
        if pos_a > (bank_len - 12):
            continue
        res_arr.append(a)
        pos_arr.append(pos_a)
        
        # Repeat for following 11
        for _ in range(11):
            found_val = None
            found_pos = None
            for j in range(len(digits)):
                b = digits[j]
                try:
                    pos_b = bank[pos_arr[-1]+1:].index(b) + pos_arr[-1]+1
                    if pos_b > (bank_len - 12 + len(res_arr)):
                        continue
                    found_val = b
                    found_pos = pos_b
                    break
                except ValueError:
                    continue
            if found_val is None:
                break
            res_arr.append(found_val)
            pos_arr.append(found_pos)
        
        if len(res_arr)==12:
            return int("".join([str(el) for el in res_arr]))
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
        s = 0
        for bank in data:
            str_bank = "".join([str(el) for el in bank])
            jolt = solve_bank_overcharged(bank=bank)
            self.logger.debug(f"Bank {str_bank} -> Jolt {jolt}")
            s+=jolt
        return s