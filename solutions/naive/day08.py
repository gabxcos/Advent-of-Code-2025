from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

import math
from typing import List, Set, Tuple

Point3D = Tuple[int, int, int]
Circuit = Set[Point3D]
ScoredCircuit = Tuple[Circuit, float] 

class BoxesSplitter(BaseLinesSplitter):
    def split(self):
        return [tuple(int(el) for el in line.split(",")) for line in self.lines]

def distance(b1: Point3D, b2: Point3D) -> float:
    # do we need to normalize with sqrt?
    x1,y1,z1 = b1
    x2,y2,z2 = b2
    return math.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)

class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=8, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = BoxesSplitter(self.test_data).split()
        self.data = BoxesSplitter(self.data).split()

    def merge(self, couples: List[ScoredCircuit]) -> Tuple[List[Circuit], Circuit]:
        links = [couple for couple,_ in couples]
        latest_link = None
        self.logger.debug(f"Starting merging with boxes: {links}")
        merged = True
        merged_cycles = 0
        while merged:
            # reset
            merged = False
            new_links = []
            # cycle
            for link in links:
                found = False
                for i,new_link in enumerate(new_links):
                    common_len = len(link.intersection(new_link))
                    if common_len>0:
                        new_links[i] = new_link.union(link)
                        merged = True # ensures a new general cycle
                        found = True # ensures the base set is not added solo, as it has been merged somewhere already
                        merge_len = len(new_links[i])
                        if (merge_len>len(new_link)) and (len(link)==2): # couple was not contained, but is actually a new merge
                            latest_link = link
                if not found:
                    new_links.append(link)
            # cycle update
            merged_cycles+=1
            links = new_links
            self.logger.debug(f"Cycle {merged_cycles}: Ended up with links: {links}")
        return links, latest_link

    def find_latest_link(self, couples: List[ScoredCircuit]) -> Circuit:
        links = [couple for couple,_ in couples]
        merge_links = []
        latest_link = None
        for couple in links:
            b1,b2 = couple
            # Skip if fully contained in single circuit
            if len(merge_links)==1:
                only_link = merge_links[0]
                if (b1 in only_link) and (b2 in only_link):
                    continue
            self.logger.debug(f"Adding couple {couple}:")
            contained_links = list(filter(lambda s : ((b1 in s) or (b2 in s)), merge_links))
            not_contained_links = list(filter(lambda s : ((b1 not in s) and (b2 not in s)), merge_links))
            if len(contained_links)==0:
                merge_links = [couple]+not_contained_links
            else:
                new_link = set()
                for link in contained_links:
                    new_link = new_link.union(link)
                # Update latest link if it connected all links into a single one
                #new_node = (len(contained_links)==1) and not ((b1 in contained_links[0]) and (b2 in contained_links[0]))
                if (len(not_contained_links)==0): # and ((len(contained_links)>1) or new_node):
                    latest_link = couple
                    self.logger.debug(f"Couple {couple} united all circuits into one")
                new_link = new_link.union(couple)
                merge_links = [new_link] + not_contained_links
            self.logger.debug(merge_links)
            self.logger.debug("-"*20)
                
        return latest_link


    def part_1(self, data):
        couples = sorted(list({frozenset({b1, b2}): distance(b1, b2) for b1 in data for b2 in data if b1!=b2}.items()), key=lambda x: x[1])
        num_couples = len(couples)
        self.logger.debug(f"Found {num_couples} distinct couples.")
        top_couples = couples[:(10 if num_couples< 1000 else 1000)]
        circuits,_ = self.merge(couples=top_couples)
        circuit_lens = sorted([len(s) for s in circuits], reverse=True)
        self.logger.debug(f"Ended up with these circuit lens: {circuit_lens}")
        assert len(circuit_lens)>=3, f"Needed at least 3 circuits connected, found {len(circuit_lens)}"
        return circuit_lens[0]*circuit_lens[1]*circuit_lens[2]
    
    def part_2(self, data):
        couples = sorted(list({frozenset({b1, b2}): distance(b1, b2) for b1 in data for b2 in data if b1!=b2}.items()), key=lambda x: x[1])
        num_couples = len(couples)
        self.logger.debug(f"Found {num_couples} distinct couples.")
        link = self.find_latest_link(couples=couples)
        link = list(link)
        self.logger.debug(f"The latest relevant link was {link}")
        return link[0][0]*link[1][0]