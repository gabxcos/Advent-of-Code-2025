from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

import copy

class IngredientsSplitter(BaseLinesSplitter):
    def split(self):
        # Separate
        empty_line_idx = self.lines.index("")
        fresh_ranges = self.lines[:empty_line_idx]
        available_items = self.lines[empty_line_idx+1:]
        # Transform
        fresh_ranges = [( int(ra.split("-")[0]), int(ra.split("-")[1])) for ra in fresh_ranges]
        available_items = [int(it) for it in available_items]
        # Send
        return {"fresh": fresh_ranges, "available": available_items}

class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=5, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = IngredientsSplitter(self.test_data).split()
        self.data = IngredientsSplitter(self.data).split()

    def merge_overlap(self, ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
        i = 0
        new_ranges = []

        self.logger.debug(f"Trying to fix ranges: {ranges}")
        merges_done = False
        while i < (len(ranges)-1):
            first_a, first_b = ranges[i]
            second_a, second_b = ranges[i+1]
            if first_b >= second_a:
                new_ranges.append((first_a, max(first_b, second_b)))
                i += 2
                self.logger.debug(f"Merged ranges {first_a, first_b} and {second_a, second_b}")
                merges_done = True
            else:
                new_ranges.append((first_a, first_b))
                i+=1

            # Add last item
            if i==(len(ranges)-1):
                new_ranges.append(ranges[-1])

        # Repeat until there are no more necessary merges
        if merges_done:
            return self.merge_overlap(sorted(new_ranges, key=lambda x:x[0]))

        return new_ranges

    def binary_search_fresh(self, ranges: list[tuple[int, int]], value: int) -> bool:
        self.logger.debug(f"Testing for item with ID {value}")
        left, right = 0, len(ranges) - 1
        while left <= right:
            mid = (left + right) // 2
            mid_a, mid_b = ranges[mid]
            if (value >= mid_a) and (value <= mid_b):
                self.logger.debug(f"FRESH: ID {value} is in range ({mid_a}, {mid_b})")
                return True
            elif value > mid_b:
                self.logger.debug("\tTesting for higher than "+str(mid_b))
                left = mid + 1
            else:
                self.logger.debug("\tTesting for lower than "+str(mid_a))
                right = mid - 1
        self.logger.debug(f"NOT FRESH: ID {value} is in no ranges")
        return False

    def part_1(self, data):
        # Obtain fresh ranges
        fresh_ranges = sorted(data["fresh"], key=lambda x:x[0])
        fresh_ranges = self.merge_overlap(fresh_ranges)
        self.logger.debug(fresh_ranges)
        # Obtain available list
        available_list = data["available"]
        # Cycle
        s = 0
        for val in available_list:
            if self.binary_search_fresh(fresh_ranges, val):
                s+=1
        return s

    
    def part_2(self, data):
        # Obtain fresh ranges
        fresh_ranges = sorted(data["fresh"], key=lambda x:x[0])
        fresh_ranges = self.merge_overlap(fresh_ranges)
        self.logger.debug(fresh_ranges)
        # Compute number of items
        s = 0
        for a,b in fresh_ranges:
            num = (b-a+1)
            s += num
            self.logger.debug(f"Range {a,b} contains {num} elements, new total is {s}")
        return s