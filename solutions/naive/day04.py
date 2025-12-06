from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

import copy

class RollsSplitter(BaseLinesSplitter):
    def split(self):
        mapper = {".":0, "@":1}
        return [[mapper[ch] for ch in line] for line in self.lines]

class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=4, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = RollsSplitter(self.test_data).split()
        self.data = RollsSplitter(self.data).split()

    def get_adjacents(self, x, y, pacman=False, data=None):
        res = [(x+dx, y+dy) for dx in (-1,0,+1) for dy in (-1,0,+1) if not ((dx==0) and (dy==0))]
        if not pacman:
            res = list(filter(lambda el : (el[0]>=0) and (el[1]>=0), res))
        else:
            assert (data is not None), "Must provide data matrix if pacman is True"
            max_x = len(data[0])
            max_y = len(data)
            res = list(map(lambda el : (el[0]%max_x, el[1]%max_y), res))
        return res
    
    def get_roll_score(self, x, y, data):
        adjs = self.get_adjacents(x, y)
        vals = []
        for xx,yy in adjs:
            try:
                vals.append(data[yy][xx])
            except IndexError:
                continue
        return sum(vals)

    def part_1(self, data):
        cnt = 0
        for y in range(len(data)):
            for x in range(len(data[0])):
                if data[y][x]==1:
                    score = self.get_roll_score(x,y,data)
                    self.logger.debug(f"Roll ({x}, {y}) has {score} adjacents.")
                    if score<4:
                        cnt+=1
                        self.logger.debug(f"\tFound a valid roll in position ({x}, {y})")
        return cnt

    
    def part_2(self, data):
        # Initialize
        prev_cnt = -1
        curr_cnt = 0
        prev_data = copy.deepcopy(data)
        new_data = copy.deepcopy(data)
        # Stop when there are no more deletions
        while prev_cnt < curr_cnt:
            # Make equal in order to track changes
            prev_cnt = curr_cnt
            for y in range(len(prev_data)):
                for x in range(len(prev_data[0])):
                    if prev_data[y][x]==1:
                        score = self.get_roll_score(x,y,prev_data)
                        self.logger.debug(f"Roll ({x}, {y}) has {score} adjacents.")
                        if score<4:
                            curr_cnt+=1
                            self.logger.debug(f"\tFound a valid roll in position ({x}, {y})")
                            new_data[y][x] = 0 # Delete from new data
            # Update data
            prev_data = copy.deepcopy(new_data)
            # Log changes
            if prev_cnt == curr_cnt:
                self.logger.debug("No more deletions to make, stopping")
            else:
                self.logger.debug(f"Found {curr_cnt - prev_cnt} new deletions")
        return curr_cnt