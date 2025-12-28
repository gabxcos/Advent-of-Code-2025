# Note: this day changes test input from part 1 to part 2

from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

from typing import Set, Dict

class DeviceSplitter(BaseLinesSplitter):
    def split(self):
        lines = [line.split(" ") for line in self.lines]
        return { line[0][:-1] : frozenset(line[1:]) for line in lines }
        
class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=11, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = DeviceSplitter(self.test_data).split()
        self.data = DeviceSplitter(self.data).split()

    def walk_forward(self, data: Dict[str, Set[str]]) -> int:
        paths = { "you": 1 }
        finished = 0
        while paths:
            self.logger.debug(paths)
            new_paths = dict()
            for device,cost in paths.items():
                for new_device in data[device]:
                    new_paths[new_device] = new_paths.setdefault(new_device, 0) + cost
            if "out" in new_paths:
                finished += new_paths["out"]
                del new_paths["out"]
            paths = new_paths
        return finished
    
    def walk_forward_two(self, data: Dict[str, Set[str]]) -> int:
        # Tuple indicates: device, passes-fft, passes-dac
        paths = { ("svr", False, False): 1 }
        finished = 0
        while paths:
            self.logger.debug(paths)
            new_paths = dict()
            for (device, passes_fft, passes_dac),cost in paths.items():
                for new_device in data[device]:
                    new_d_tuple = (new_device, passes_fft or (new_device=="fft"), passes_dac or (new_device=="dac"))
                    new_paths[new_d_tuple] = new_paths.setdefault(new_d_tuple, 0) + cost
            # find "out" tuples
            out_tuples = [t for t in new_paths.keys() if t[0]=="out"]
            for t in out_tuples:
                if t==("out", True, True):
                    finished += new_paths[t]
                del new_paths[t]
            paths = new_paths
        return finished

    def part_1(self, data):
        self.logger.debug(f"Starting with data: {data}")
        results = self.walk_forward(data=data)
        self.logger.debug(f"Found {results} paths")
        return results
    
    def part_2(self, data):
        self.logger.debug(f"Starting with data: {data}")
        results = self.walk_forward_two(data=data)
        self.logger.debug(f"Found {results} paths")
        return results