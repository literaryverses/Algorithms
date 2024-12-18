# Performs maze generation algorithms.
# These are made specifically for 2D orthogonal mazes

from random import choice
from objects import Path, Cell
from copy import deepcopy


## INSIDE ALGORITHMS
def random_mouse(start, end):
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


def wall_follower(start, end, direct="right"):
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
        # straight direction
        while orientation in cell.getDirections() and cell != end:
            cell = cell.neighbors[orientation]
            path.append(cell)

        clockwise = 0
        counterclockwise = 0

        # wall follower
        while (
            clockwise != counterclockwise or (clockwise == 0 and counterclockwise == 0)
        ) and cell != end:
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
                clockwise += 1
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
                    if rotation == 1:
                        counterclockwise += 1
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
    cell = start
    path = Path(cell)
    visited = {}
    orientations = ["north", "east", "south", "west"]

    def init_cell_visits(cell):
        directions = cell.getDirections()
        if cell not in visited and len(directions) > 1:
            visited[cell] = {direction: 0 for direction in directions}

    init_cell_visits(cell)

    while cell != end:
        directions = cell.getDirections()
        next_direction = None

        if len(directions) > 1:
            # select the least visited direction that hasn't been visited twice
            next_direction = min(
                (direction for direction in directions if visited[cell][direction] < 2),
                key=lambda d: visited[cell][d],
            )
        else:
            next_direction = directions[0]

        if len(directions) > 1:
            visited[cell][next_direction] += 1  # mark visit

        cell = cell.neighbors[next_direction]
        init_cell_visits(cell)

        if cell in visited:
            reciprocal_direction = orientations[
                (orientations.index(next_direction) + 2) % 4
            ]  # mark reciprical visit
            visited[cell][reciprocal_direction] += 1
        path.append(cell)

    return path


## OUTSIDE ALGORITHMS
def dead_end_filler(_grid, _start, _end):
    """
    Scans the maze for a dead end, upon which it starts to fill passages until it is able to move in more than one direction.
    """
    grid = deepcopy(_grid)
    start = grid.getCell(*_start.coord)
    end = grid.getCell(*_end.coord)
    for level in grid.grid:
        for row in level:
            for cell in row:
                if isinstance(cell, Cell) and cell not in (start, end):
                    while len(cell.getLinks()) == 1:
                        neighbor = cell.getLinks()[0]
                        if neighbor in (start, end):
                            break
                        cell.unlink(neighbor)
                        cell = neighbor

    # create rest of path
    path = Path(start)
    visited = {start}
    cell = start
    while cell != end:
        cell = choice(cell.getLinks())
        if cell in visited and cell != start:
            continue
        visited.add(cell)
        path.append(cell)
    return path


def cul_de_sac_filler(_grid, _start, _end):
    """
    Find nooses (loops with one way out of them), converts them into a dead end, then runs the dead end filler.
    """
    grid = deepcopy(_grid)
    start = grid.getCell(*_start.coord)
    end = grid.getCell(*_end.coord)

    def is_outer_border(cell):
        row, col, _ = cell.coord
        return row == 0 or col == 0 or row == grid.rows - 1 or col == grid.cols - 1

    def find_nooses(grid):
        nooses = []

        for row in range(grid.rows):
            for col in range(grid.cols):
                cell = grid.grid[0][row][col]

                if is_outer_border(cell):
                    continue

                accessible_neighbors = [neighbor for neighbor in cell.getLinks()]

                # if the cell has exactly one accessible way out, it's a noose
                if len(accessible_neighbors) == 1:
                    nooses.append((cell, accessible_neighbors[0]))

        return nooses

    def convert_nooses_to_dead_ends(nooses):
        for noose, exit_cell in nooses:
            # seal all links except the exit
            for neighbor in noose.getLinks():
                if neighbor != exit_cell:
                    noose.unlink(neighbor)

    def dead_end_filler(grid, start, end):
        for level in grid.grid:
            for row in level:
                for cell in row:
                    if isinstance(cell, Cell) and cell not in (start, end):
                        while len(cell.getLinks()) == 1:
                            neighbor = cell.getLinks()[0]
                            if neighbor in (start, end):
                                break
                            cell.unlink(neighbor)
                            cell = neighbor
        return grid

    while True:
        nooses = find_nooses(grid)

        if not nooses:
            break
        convert_nooses_to_dead_ends(nooses)
        grid = dead_end_filler(grid, start, end)

        path = Path(start)
    visited = {start}
    cell = start
    while cell != end:
        cell = choice(cell.getLinks())
        if cell in visited and cell != start:
            continue
        visited.add(cell)
        path.append(cell)
    return path


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


def collision_solver(start):
    """Breadth-First search algorithm that seals loops upon collision
    and then uses the dead end filler algorithm until only the path remains"""
    pass


def shortest_path_finder(grid):
    """Breadth-First search algorithm that traces back its path once it reaches the solution"""
    pass


def shortest_paths_finder(grid):
    """Breadth-First search algorithm that runs a Breadth-First search again from the end"""
    pass
