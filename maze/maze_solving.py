# Performs maze generation algorithms.
# These are made specifically for 2D orthogonal mazes

from random import choice
from utilities import Path


## INSIDE ALGORITHMS
def randomMouse(start, end):
    """
    Random Mouse: stimulates a mouse moving inside maze.
    Very inefficent, especially with no memory.
    """
    cell = start
    path = Path(cell)
    while cell != end:
        cell = choice(cell.getNeighbors())
        path.append(cell)
    return path


def wallFollower(start, end, direct="right"):
    """
    Wall Follower: follows on the side of the wall.
    This not guarenteed to solve if the starting position starts inside the maze
    (as opposed to a cell on the very edge of the grid)
    """
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


def pledge(start, end):
    """
    Pledge: runs a straight direction until it hits a wall. Afterwards, follows a wall follower
    algorithm until the number of clockwise turns is equal to the number of counterclockwise turns,
    at which it resumes running a straight direction again.
    """
    orientations = ["north", "east", "south", "west"]
    orientation = choice(orientations)

    direct = choice(["left", "right"])
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


def tremaux(start, end):
    """
    Chooses arbitrary paths at a crossroads but marks where it came from.
    If it comes to the same crossroads and marks the direction twice,
    then it is treated as a wall.
    """
    pass


## OUTSIDE ALGORITHMS
def dead_end_filler(grid):
    """
    Scans the maze for a dead end, upon which it starts to fill passages until it is able to move in more than one direction.
    """
    pass


def cul_de_sac_filler(grid):
    """
    Find nooses (loops with one way out of them), converts them into a dead end, then runs the dead end filler.
    """
    pass


def blind_alley_filler(grid):
    """
    Sends a wall follower to every direction at a crossroads.
    If a follower returns from the same path then the direction is a dead end and filled.
    """
    pass


def blind_alley_sealer(grid):
    """
    Identical to the blind_alley_filler except instead of filling dead ends,
    it seals the entrances toward them.
    """
    pass


## OTHER ALGORITHMS
def recursive_backtracker(start, end):
    """
    Uses recursion to retreat from dead ends while it explores
    """

    def recursion(current, end, path, visited):
        visited.add(current)

        if current == end:
            return path

        for neighbor in current.getLinks():
            if neighbor not in visited:
                path.append(neighbor)
                final_path = recursion(neighbor, end, path, visited)
                if final_path:
                    return final_path
                path.pop()

    path = Path(start)
    visited = set()
    return recursion(start, end, path, visited)


def collision_solver(grid):
    """Breadth-First search algorithm that seals loops upon collision
    and then uses the dead end filler algorithm until only the path remains"""
    pass


def shortest_path_finder(grid):
    """Breadth-First search algorithm that traces back its path once it reaches the solution"""
    pass


def shortest_paths_finder(grid):
    """Breadth-First search algorithm that runs a Breadth-First search again from the end"""
    pass
