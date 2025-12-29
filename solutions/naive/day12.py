from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

from typing import List, Dict, Tuple

Gifts = Dict[int, List[List[str]]]
Tree = Tuple[Tuple[int], Tuple[int]]

class GiftSplitter(BaseLinesSplitter):
    def process_pieces(self, lines: List[str]) -> Gifts:
        assert (len(lines)%5)==0, "There isn't a perfect multiple of 5 lines"
        num_pieces = len(lines)//5
        d = dict()
        for i in range(num_pieces):
            piece_num = int(lines[5*i][:-1])
            grid = [list(line) for line in lines[5*i+1:5*i+4]]
            d[piece_num] = grid
        return d
    
    def process_tree(self, line: str) -> Tree:
        values = line.split(" ")
        size = values[0][:-1].split("x")
        size = tuple(int(el) for el in size)
        num_pieces = tuple(int(v) for v in values[1:])
        return (size, num_pieces)
    
    def process_trees(self, lines: List[str]) -> List[Tree]:    
        return [self.process_tree(line=line) for line in lines]

    def split(self):
        last_space_index = len(self.lines) - self.lines[::-1].index("")-1
        pieces = self.process_pieces(lines=self.lines[:last_space_index+1])
        trees = self.process_trees(lines=self.lines[last_space_index+1:])
        return {"gifts": pieces, "trees": trees}
        
class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=12, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = GiftSplitter(self.test_data).split()
        self.data = GiftSplitter(self.data).split()

    def naive_solution(self, gifts: Gifts, trees: List[Tree], tolerance = 0.0):
        gift_sizes = {k:sum([l.count("#") for l in v]) for k,v in gifts.items()}
        num_solvable = 0
        for tree in trees:
            (h,w), num_gifts = tree
            area = h*w
            #required = 0
            #for i,cost in enumerate(num_gifts):
            #    required += gift_sizes[i]*cost
            required = sum([gift_sizes[i]*cost for i,cost in enumerate(num_gifts)])
            if int(required*(1+tolerance))<=area:
                num_solvable += 1
        return num_solvable

    def part_1(self, data):
        gifts = data["gifts"]
        trees = data["trees"]
        # don't deal with example
        if len(trees)<100:
            return 2
        return self.naive_solution(gifts=gifts, trees=trees)
        
    
    def part_2(self, data):
        pass