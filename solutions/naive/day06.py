from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

from functools import reduce

class MathSplitter(BaseLinesSplitter):
    def split(self):
        # Numbers
        num_lines = self.lines[:-1]
        spaces_idxs_list = [set([i for i, x in enumerate(list(line)) if x == " "]) for line in num_lines]
        common_spaces_idxs = spaces_idxs_list[0]
        for s in spaces_idxs_list:
            common_spaces_idxs = common_spaces_idxs.intersection(s)
        processed_num_lines = []
        for line in num_lines:
            list_line = list(line)
            for space_idx in common_spaces_idxs:
                list_line[space_idx] = "/"
            string_line = "".join(list_line)
            split_line = string_line.split("/")
            processed_num_lines.append(split_line)

        # Number matrix for part 1
        num_matrix = [[int(el.strip()) for el in line] for line in processed_num_lines]

        # Operations
        ops = list(filter(lambda x: x!="", self.lines[-1].split(" ")))
        return {"processed_nums": processed_num_lines, "nums": num_matrix, "ops": ops}

class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=6, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = MathSplitter(self.test_data).split()
        self.data = MathSplitter(self.data).split()

    def invert_matrix(self, matrix):
        max_x = len(matrix[0])
        max_y = len(matrix)
        return [
            [matrix[y][x] for y in range(max_y)] for x in range(max_x)
        ]
    
    def invert_processed_matrix(self, matrix):
        matrix = self.invert_matrix(matrix)
        final_matrix = []
        for line in matrix:
            max_l = max(*[len(el) for el in line])
            new_line = []
            for i in range(max_l):
                new_line.append(int("".join([el[i] for el in line]).strip()))
            self.logger.debug(f"{line} -> {new_line}")
            final_matrix.append(new_line)
        return final_matrix

    def part_1(self, data):
        nums = self.invert_matrix(data["nums"])
        ops = data["ops"]
        assert len(ops)==len(nums), f"Found {len(ops)} problems but {len(nums)} number tuples."

        s = 0
        for op, num_line in zip(ops, nums):
            if op=="+":
                res = reduce(lambda a,b:a+b, num_line)
            elif op=="*":
                res = reduce(lambda a,b:a*b, num_line)
            else:
                raise Exception(f"Wrong operation found: expected + or *, found {op}")
            self.logger.debug(f"Solving {num_line} for op {op} -> {res}")
            s += res
        return s
    
    def part_2(self, data):
        nums = self.invert_processed_matrix(data["processed_nums"])
        ops = data["ops"]
        assert len(ops)==len(nums), f"Found {len(ops)} problems but {len(nums)} number tuples."

        s = 0
        for op, num_line in zip(ops, nums):
            if op=="+":
                res = reduce(lambda a,b:a+b, num_line)
            elif op=="*":
                res = reduce(lambda a,b:a*b, num_line)
            else:
                raise Exception(f"Wrong operation found: expected + or *, found {op}")
            self.logger.debug(f"Solving {num_line} for op {op} -> {res}")
            s += res
        return s