from random import randint

def sidewinder(grid):

    def getSample(list):
        return list[randint(0, len(list)-1)]

    for row in grid.each_row():
        run = []
        for cell in row:
            run.append(cell)

            at_eastern_boundary = True # end of row
            if cell.neighbors.get('east'):
                at_eastern_boundary = False
            at_northern_boundary = True # top of grid
            if cell.neighbors.get('north'):
                at_northern_boundary = False

                
            should_close_out = at_eastern_boundary or (not at_northern_boundary and randint(0, 1) == 0)

            if should_close_out:
                member = getSample(run)
                northerner = member.neighbors.get('north')
                if northerner:
                    member.link(northerner)
                run.clear()
            else:
                easterner = cell.neighbors.get('east')
                cell.link(easterner)
        
    return grid