# Performs maze generation algorithms.
# These are made specifically for 2D orthogonal mazes

from random import choice
from collections import Counter
from utilities import Path

## INSIDE ALGORITHMS
"""
Random Mouse: stimulates a mouse moving inside maze. 
Very inefficent, especially with no memory.
"""


def randomMouse(start, end):
    cell = start
    path = Path(cell)
    while cell != end:
        cell = choice(cell.getNeighbors())
        path.append(cell)
    return path


"""
Wall Follower: follows on the side of the wall. This not guarenteed to solve if the starting 
position starts inside the maze (as opposed to a cell on the very edge of the grid)
"""


def wallFollower(start, end, direct="right"):
    orientations = ["north", "east", "south", "west"]
    orientation = "north"

    if direct == "left":
        orientations.reverse()

    path = Path(start)
    cell = start

    while cell != end:
        # check rotation access
        idx = orientations.index(orientation)
        orientation = (
            orientations[(idx + 1) % 4]
            if direct == "right"
            else orientations[(idx - 1) % 4]
        )

        directions = cell.getDirections()

        # move forward if possible
        if orientation in directions:
            cell = cell.neighbors[orientation]
            path.append(cell)
            continue

        # rotate other way
        for rotation in range(3):
            orientation = (
                orientations[(idx - rotation) % 4]
                if direct == "right"
                else orientations[(idx + rotation) % 4]
            )

            if orientation in directions:
                cell = cell.neighbors[orientation]
                path.append(cell)
                break

    return path


"""
Pledge: runs a straight direction until it hits a wall. Afterwards, follows a wall follower
algorithm until the number of clockwise turns is equal to the number of counterclockwise turns, 
at which it resumes running a straight direction again.
"""


# def pledge(start, end):
#     path = Path(start)
#     direct = choice("right left".split())
#     orientation = choice(start.getDirections())
#     cell = start.neighbors[orientation]
#     while cell != end:
#         path.append(cell)
#         directions = cell.getDirections()
#         if orientation in directions:
#             cell = cell.neighbors[orientation]
#             path.append(cell)
#             continue

#         next = cell.neighbors.get(orientation)
#         if not next:
#             # TODO wall follower
#             pass
#         else:
#             cell = next
#     return path


def tremaux(start, end):
    pass


## OUTSIDE ALGORITHMS
def dead_end(grid):
    pass


def cul_de_sa(grid):
    pass


def blind_alley_filler(grid):
    pass


def blind_alley_sealer(grid):
    pass


## OTHER ALGORITHMS
def recursive_backtracer(grid):
    pass


def collision_solver(grid):
    pass


def shortest_path_finder(grid):
    pass


def shortest_paths_finder(grid):
    pass
