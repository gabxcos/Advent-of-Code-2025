from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class TachyonSplitter(BaseLinesSplitter):
    def split(self):
        initial_pos = list(self.lines[0]).index("S")
        splitters_pos_setlist = [
            set([i for i,x in enumerate(list(line)) if x=="^"]) for line in self.lines[1:]
        ]
        return {"initial_pos": initial_pos, "splitters": splitters_pos_setlist}

# utils for dict
def upsert(dict, key, value):
    if key in dict:
        dict[key] += value
    else:
        dict[key] = value
    return dict

class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=7, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = TachyonSplitter(self.test_data).split()
        self.data = TachyonSplitter(self.data).split()

    def part_1(self, data):
        initial_pos = data["initial_pos"]
        splitters = data["splitters"]
        self.logger.debug(f"Starting at position {initial_pos}")
        tachyons = {initial_pos}
        total_split_num = 0
        for i,split in enumerate(splitters):
            self.logger.debug(f"Advancing to level {i+1}:")
            split_num = 0
            new_tachyons = set()
            for t in tachyons:
                if t in split:
                    self.logger.debug("\tFound a splitter for tachyon in position "+str(t))
                    new_tachyons.add(t-1)
                    new_tachyons.add(t+1)
                    split_num += 1
                else:
                    new_tachyons.add(t)
            self.logger.debug(f"Performed {split_num} splits at position {i+1}")
            self.logger.debug("-"*20)
            total_split_num += split_num
            tachyons = new_tachyons
        self.logger.debug(f"Performed a total of {total_split_num} splits overall, resulting in {len(tachyons)} final tachyons")
        return total_split_num
    
    def part_2(self, data):
        last_pos = data["initial_pos"]
        splitters = data["splitters"]
        self.logger.debug(f"Starting at position {last_pos} with 1 timeline")
        timelines = {last_pos: 1}
        for i,split in enumerate(splitters):
            self.logger.debug(f"Advancing to level {i+1}:")
            
            new_timelines = dict()
            for pos, count in timelines.items():
                if pos in split:
                    self.logger.debug("\tFound a splitter for tachyon pos. "+str(pos)+" in "+str(count)+" timelines.")
                    # left possibility
                    new_timelines = upsert(new_timelines, pos-1, count)
                    # right possibility
                    new_timelines = upsert(new_timelines, pos+1, count)
                else:
                    self.logger.debug("\tNo splitters encountered for tachyon pos. "+str(pos)+" in "+str(count)+" timelines.")
                    new_timelines = upsert(new_timelines, pos, count)
            timelines = new_timelines
            self.logger.debug(f"There are now {sum(list(timelines.values()))} timelines.")
            self.logger.debug("-"*20)

        self.logger.debug(timelines)
        return sum(list(timelines.values()))