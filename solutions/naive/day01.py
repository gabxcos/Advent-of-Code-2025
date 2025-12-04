from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

from itertools import accumulate

class DialSplitter(BaseLinesSplitter):
    def split(self):
        return [int(l.replace("L","-").replace("R","")) for l in self.lines]
    
def dial_add(a, b):
    return (a+b)%100

class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=1, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = DialSplitter(self.test_data).split()
        self.data = DialSplitter(self.data).split()

    def part_1(self, data):
        data = [50]+data
        acc = list(accumulate(data, dial_add))
        return acc.count(0)
    
    def part_2(self, data):
        cnt = 50
        zero_cnt = 0
        for move in data:
            self.logger.debug(f"Starting at {cnt}, moving of {move}...")
            abs_move = abs(move)
            if abs_move >= 100:
                full_turns = (abs_move // 100)
                remainder = int(move/abs_move*(abs_move%100))
                self.logger.debug(f"\tDoing {full_turns} full turns with a remainder of {remainder}")
                zero_cnt += full_turns
                move = remainder
            new_cnt = cnt + move
            if (new_cnt <= 0) or (new_cnt > 99):
                new_cnt = new_cnt%100
                if cnt!=0: # don't count the zero we had stopped on twice
                    if (new_cnt==0):
                        self.logger.debug("\tStopped on zero")
                    else:
                        self.logger.debug("\tPassed the zero while turning")
                    zero_cnt += 1
            # update
            cnt = new_cnt
            self.logger.debug(f"\t- Found a zero {zero_cnt} times")
        return zero_cnt