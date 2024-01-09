import game_of_life as gol

def test():
    assert gol.Cell(1, 1, True).alive == True
    assert gol.Cell(1, 1, False).alive == False 
