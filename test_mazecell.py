from maze import MazeCell

def test_cell_initialize():
    cell = MazeCell()
    assert isinstance(cell, MazeCell)
    assert cell.edges == {'N':False, 'E':False, 'S':False, 'W':False}

