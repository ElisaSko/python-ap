import game_of_life as gol

def test_Game_Of_Life_functions():
    alive_cell=gol.Cell(1,1,1)
    dead_cell=gol.Cell(1,1,0)
    pattern=gol.Pattern([[0,0,0],[0,1,0],[0,0,0]],3,3)
    set_of_cells=gol.Set_Of_Cells([],4,4).initialize(pattern)
    corner_cell=set_of_cells.cells[0][0]
    assert alive_cell.alive == True
    assert dead_cell.alive == False
    assert pattern.height == 3
    assert pattern.width == 3
    assert set_of_cells.height == 4
    assert set_of_cells.width == 4
    assert set_of_cells.cells[0][0].alive == False
    assert set_of_cells.cells[1][1].alive == True
    assert set_of_cells.cells[3][3].alive == False
    assert alive_cell.neighbours(set_of_cells) == [0,0,0,0,0,0,0,0]
    assert corner_cell.neighbours(set_of_cells) == [0,1,0]
    assert alive_cell.count_neighbours(set_of_cells) == 0
    assert corner_cell.count_neighbours(set_of_cells) == 1

def test_Cell_update():
    pattern=gol.Pattern([[0,0,0],[0,1,0],[0,0,0]],3,3)
    set_of_cells=gol.Set_Of_Cells([],4,4).initialize(pattern)
    set_of_cells.update()
    assert set_of_cells.cells==[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    pattern=gol.Pattern([[0,0,0],[1,1,1],[0,0,0]],3,3)
    set_of_cells=gol.Set_Of_Cells([],4,4).initialize(pattern)
    set_of_cells.update()
    assert set_of_cells.cells==[[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,0,0,0]]

def test_global():
    pattern = gol.Pattern([[0,0,1],[0,1,1],[0,0,0]],3,3)
    set_of_cells = gol.Set_Of_Cells([],3,3).initialize(pattern)
    number_of_iterations = 3
    for i in range (number_of_iterations):
        set_of_cells.update()
    result = [[0,0,0],[0,1,1],[0,1,1]]
    assert set_of_cells.cells == result