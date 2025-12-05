from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class RangesSplitter(BaseLinesSplitter):
    def split(self):
        l = self.lines[0]
        ranges = l.split(",")
        ranges = [[int(r.split("-")[0]), int(r.split("-")[1])] for r in ranges]
        return ranges
    
def solve_range(range: list[int]) -> list[int]:
    a, b = range
    res = []
    curr = a
    scurr = str(curr)
    ls = len(scurr)
    # treat the case of odd number of digits
    if (ls%2)==1:
        ls += 1
        hls = int(ls/2)
        rep_s = "1" + ("0" * (hls-1))
        curr = int(rep_s*2)
    else:
        # generate first valid based on first number of range
        hls = int(ls/2)
        rep_s = scurr[0:hls]
        test_curr = int(rep_s*2)
        if test_curr>=curr:
            curr = test_curr
        # it could be lower than the first number: in that case, adjust
        else:
            rep_s = str(int(rep_s)+1)
            curr = int(rep_s*2)
    # progressively increment left half of number and double it
    while curr<=b:
        res.append(curr)
        rep_s = str(int(rep_s)+1)
        curr = int(rep_s*2)
    return res

def generate_invalid_numbers(max_digits: int) -> list[int]:
    res = []
    for pat_len in range(1, max_digits // 2 + 1):          # at least two repetitions needed
        # All possible patterns of this length that do NOT start with '0'.
        start = 10 ** (pat_len - 1)                        # smallest pat_len‑digit number
        stop  = 10 ** pat_len                              # one past the largest

        for pattern in range(start, stop):
            pat_str = str(pattern)

            # How many times can we repeat this pattern before exceeding max_digits?
            max_repeat = max_digits // pat_len
            # We need at least two repetitions to be a “repeated” number.
            for repeat in range(2, max_repeat + 1):
                res.append(int(pat_str * repeat))
    return sorted(set(res))


class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=2, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = RangesSplitter(self.test_data).split()
        self.data = RangesSplitter(self.data).split()

    def part_1(self, data):
        s = 0
        for ra in data:
            res = solve_range(range=ra)
            self.logger.debug(f"Range {ra} contains the following invalid IDs: {res}")
            s += sum(res)
        return s
    
    def part_2(self, data):
        range_maxes = [b for _,b in data]
        max_num = max(range_maxes)
        max_digits = len(str(max_num))
        invalids = generate_invalid_numbers(max_digits=max_digits)
        s = 0
        for a,b in data:
            res = list(filter(lambda x : (a<=x) and (x<=b), invalids))
            self.logger.debug(f"Range {[a,b]} contains the following invalid IDs: {res}")
            s += sum(res)
        return s