from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

from typing import Tuple, List, Set, Optional

Point = Tuple[int, int]
Rect = Tuple[Point, Point]

class PointSplitter(BaseLinesSplitter):
    def split(self):
        return [tuple(int(el) for el in line.split(",")) for line in self.lines]
    
def area(a: Point, b: Point) -> int:
    dist = lambda x0,x1 : abs(x0-x1)+1
    ax, ay = a
    bx, by = b
    return dist(ax,bx)*dist(ay,by)

def canonical_rect(a: Point, b: Point) -> Rect:
    return (a, b) if a <= b else (b, a)

def get_rect_points(a: Point, b: Point) -> Set[Point]:
    ax,ay = a
    bx,by = b
    min_x, max_x = (min([ax,bx]), max([ax,bx]))
    min_y, max_y = (min([ay,by]), max([ay,by]))
    return {(x,y) for x in range(min_x, max_x+1) for y in range(min_y, max_y+1)}
        
class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=9, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = PointSplitter(self.test_data).split()
        self.data = PointSplitter(self.data).split()

    def prettyprint(self, grid: List[List[bool]], with_sep: bool = True, draw_rec: Optional[Rect] = None) -> None:
        new_grid = [["#" if el else "." for el in line] for line in grid]
        if draw_rec is not None:
            a,b = draw_rec
            points = get_rect_points(a,b)
            for x,y in points:
                new_grid[y][x] = "O"

        self.logger.debug("\n".join(["".join(line) for line in new_grid]))
        if with_sep:
            self.logger.debug("\n"+"-"*30+"\n")


    def is_inside(self, p: Point, grid: List[List[bool]]) -> bool:
        x,y = p
        has_left = any(grid[y][:x])
        has_right = any(grid[y][x+1:])
        if has_left and has_right:
            max_y = len(grid)
            has_up = any([grid[iy][x] for iy in range(0, y)])
            has_down = any([grid[iy][x] for iy in range(y+1, max_y)])
            if has_up and has_down:
                return True
        return False

    def part_1(self, data):
        self.logger.debug(data)
        areas = [area(a,b) for a in data for b in data]
        self.logger.debug(areas)
        return max(areas)
    
    def part_2(self, data):
        # solved through aid on subreddit
        points = set(data)
        
        # compress
        unique_X: List[int] = sorted(list({ p[0] for p in points}))
        unique_Y: List[int] = sorted(list({ p[1] for p in points}))

        x_map = {i:x for x,i in enumerate(unique_X)}
        y_map = {i:x for x,i in enumerate(unique_Y)}

        grid = [[ False for _ in range(len(unique_X))] for _ in range(len(unique_Y))]
        z_points = []
        for x,y in points:
            x_pos = x_map[x]
            y_pos = y_map[y]
            grid[y_pos][x_pos] = True
            z_points.append((x_pos, y_pos))
        
        self.prettyprint(grid=grid, with_sep=True)
        
        # polygon
        z_couples = {canonical_rect(a,b) for a in z_points for b in z_points if a!=b}
        for a,b in z_couples:
            ax,ay = a
            bx,by = b

            if (ax==bx):
                y0, y1 = sorted([ay,by])
                for y in range(y0, y1+1):
                    grid[y][ax] = True
            elif (ay==by):
                x0, x1 = sorted([ax, bx])
                for x in range(x0, x1+1):
                    grid[ay][x] = True

        self.prettyprint(grid=grid, with_sep=True)

        # fill
        filled_points = set()
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                res = grid[y][x]
                if not res:
                    res = self.is_inside((x,y), grid)
                    grid[y][x] = res
                if res:
                    filled_points.add((x,y))
        self.prettyprint(grid=grid, with_sep=True)

        # get valid rects
        valid_z_rects = set()
        for a,b in z_couples:
            rect_points = get_rect_points(a,b)
            if len(rect_points)==len(rect_points.intersection(filled_points)):
                valid_z_rects.add((a,b))
                self.logger.debug(f"Found a valid rect between points {a} and {b}:")
                self.prettyprint(grid=grid, with_sep=True, draw_rec=(a,b))
        self.logger.debug(f"Valid rects: {valid_z_rects}")

        # decompress and get areas
        zx_map = { v:k for k,v in x_map.items()}
        zy_map = { v:k for k,v in y_map.items()}
        valid_rects = { ((zx_map[a[0]], zy_map[a[1]]), (zx_map[b[0]], zy_map[b[1]])) for a,b in valid_z_rects}
        self.logger.debug(f"Decompressed: {valid_rects}")

        areas = { area(a,b) for a,b in valid_rects }
        self.logger.debug(f"Found areas: {areas}")

        return max(areas)

