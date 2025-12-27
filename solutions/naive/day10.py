from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

from typing import Dict, List, Any, Set
from itertools import combinations
from functools import reduce
import pulp

Machine = Set[int]
Buttons = Set[Set[int]]
Joltage = List[int]

class MachineSplitter(BaseLinesSplitter):
    def line_split(self, line: str) -> Dict[str, Any]:
        lline = line.split(" ")
        # machine
        machine = lline[0][1:-1]
        machine = frozenset({ i for i,light in enumerate(machine) if light=="#"})

        # buttons
        buttons = lline[1:-1]
        for i,button_line in enumerate(buttons):
            button_line = frozenset({int(el) for el in button_line[1:-1].split(",")})
            buttons[i] = button_line
        buttons = frozenset(buttons)

        # joltage
        joltage = tuple(int(el) for el in lline[-1][1:-1].split(","))

        return {"machine": machine, "buttons": buttons, "joltage": joltage}

    def split(self):
        return [self.line_split(line) for line in self.lines]
        
class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=10, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = MachineSplitter(self.test_data).split()
        self.data = MachineSplitter(self.data).split()

    def part_1_line(self, machine: Machine, buttons: Buttons) -> int:
        if machine in buttons:
            return 1
        i = 2
        while i<=len(buttons):
            combs = combinations(buttons, i)
            for comb in combs:
                result = reduce(lambda s,t:s^t, comb)
                if machine==result:
                    return i
            i += 1
        raise Exception("Reached length of buttons without finding a solution")

    def part_1(self, data):
        final_res = 0
        for line in data:
            self.logger.debug(f"Resolving: {line}")
            result = self.part_1_line(machine=line["machine"], buttons=line["buttons"])
            self.logger.debug(f"Found a combination of {result} buttons.")
            self.logger.debug("-"*30)
            final_res += result
        return final_res
    
    def part_2_line(self, buttons: Buttons, joltage: Joltage) -> int:
        # ILP my beloved <3
        m = len(joltage)
        actions = [ tuple(1 if (i in action) else 0 for i in range(m)) for action in buttons ]
        n = len(actions)

        prob = pulp.LpProblem("ExactMatch_MinActions", pulp.LpMinimize)
        x = [pulp.LpVariable(f"x{i}", lowBound=0, cat="Integer") for i in range(n)]
        prob += pulp.lpSum(x)
        for j in range(m):
            prob += (
                pulp.lpSum(actions[i][j] * x[i] for i in range(n)) == joltage[j],
                f"counter_{j}"
            )
        solver = pulp.PULP_CBC_CMD(msg=False)   # set msg=True for solver output
        prob.solve(solver)
        if prob.status != pulp.LpStatusOptimal:
            raise RuntimeError("ILP did not find an optimal solution (status=%s)" %
                            pulp.LpStatus[prob.status])
        counts = [int(pulp.value(var)) for var in x]
        total = sum(counts)
        return total

    def part_2(self, data):
        final_res = 0
        for line in data:
            self.logger.debug(f"Resolving: {line}")
            result = self.part_2_line(buttons=line["buttons"], joltage=line["joltage"])
            self.logger.debug(f"Found a combination of {result} button presses.")
            self.logger.debug("-"*30)
            final_res += result
        return final_res