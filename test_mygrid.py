import pytest
from mygrid import Grid



def foo_gen(nbre_item):
    for i in range(nbre_item):
        yield i*10



@pytest.fixture
def grid():

    # 0  1  2  3     
    # 4  5  6  7
    # 8  9  10 11
    w, h  = 4, 3
    grid = Grid(w, h)
    for j, line in enumerate(grid):
        for i, elt in enumerate(line):
            grid[j][i] = w*j + i
    return grid


def test_grid_fixture(grid):
    assert grid[0][2] == 2
    assert grid[2][3] == 11

def test_size(grid):
    assert grid.width == 4
    assert grid.height == 3

def test_wrong_size():
    with pytest.raises(ValueError):
        grid = Grid(-1, 10)

def test_len():
    grid = Grid(10, 10)
    assert len(grid) == 100

def test_instanciate_with_values():
    w, h = 4, 3
    values = list(range(w*h))
    mygrid = Grid(w, h, values)

    assert mygrid[0] == [values, values, values, values]
    assert mygrid[1, :] == [values] * 3

def test_instanciate_with_value_copy():
    w, h = 4, 3
    class Foo():
        pass

    mygrid = Grid(w, h, value=Foo(), copy=True)
    assert mygrid[0, 0] is not mygrid[0, 1]

def test_instanciate_with_iter():
    w, h = 4, 3
    iterable = list(range(w*h))
    mygrid = Grid.from_iter(w, h, iterable)
    assert mygrid[0] == [0, 1, 2, 3]
    assert mygrid[1, :] == [1, 5, 9]

def test_instanciate_with_iter_wrong_len():
    w, h = 4, 3
    values = list(range(w*h-2))
    with pytest.raises(ValueError):
        mygrid = Grid.from_iter(w, h, values)

def test_instanciate_with_gen():
    w, h = 4, 3
    values = range(w*h)
    mygrid = Grid.from_iter(w, h, values)
    assert mygrid[0] == [0, 1, 2, 3]
    assert mygrid[1, :] == [1, 5, 9]


def test_eq(grid):
    w, h = grid.width, grid.height
    ngrid = Grid(w, h)
    assert ngrid != grid
    for j, line in enumerate(ngrid):
        for i, elt in enumerate(line):
            ngrid[j][i] = w*j + i

    assert ngrid == grid
    assert not ngrid is grid

def test_getitem(grid):
    assert grid[2, 0] == 2

def test_getitem_slice_x(grid):
    assert grid[:2, 2] == [8, 9]

def test_getitem_slice_y(grid):
    assert grid[2, :2] == [2, 6]
    assert grid[2, -2:] == [6, 10]
    assert grid[2, ::-1] == [10, 6, 2]


def test_getitem_slice_xy(grid):
    assert grid[:, :] == grid

def test_setitem(grid):
    grid[2, 0] = 20
    assert grid[2, 0] == 20

def test_setitem_slice_x(grid):
    value = [10, 11, 12, 13]
    grid[:, 0] = value 
    assert grid[:, 0] == [value] * 4
    
    grid[:, 0] = 20
    assert grid[:, 0] == [20, 20, 20, 20]
    
    grid[1:5:2, 2] = 30
    assert grid[:, 2] == [8, 30, 10, 30]

    new_grid = Grid(4, 1, 99)
    grid[:, 0] = new_grid
    assert grid[:, 0] == [99] * 4

    with pytest.raises(ValueError):
        new_grid = Grid(4, 2, 99)
        grid[:, 0] = new_grid

def test_setitem_slice_y(grid):
    new_grid = Grid(1, 3, 99)
    grid[0, :] = new_grid
    assert grid[0, :] == [99] * 3

    grid[0, :] = 20
    assert grid[0, :] == [20, 20, 20]
    
    grid[1, 1:3] = 30
    assert grid[1, 1:3] == [30, 30]

    new_grid = Grid(1, 3, 99)
    grid[0, :] = new_grid
    assert grid[0, :] == [99] * 3

def test_setitem_slice_xy(grid):
    
    new_grid = Grid(2,2, 99)
    grid[1:3, 0:2] = new_grid
    assert grid[:, 0] == [0, 99, 99, 3]
    assert grid[1, :] == [99, 99, 9]


def test_get_slices_size(grid):
    assert grid.get_slices_size(slice(None), slice(None)) == \
                                                (grid.width, grid.height)
    assert grid.get_slices_size(slice(None), slice(0, 2)) == \
                                                (grid.width, 2)
    assert grid.get_slices_size(slice(None), slice(1, 2)) == \
                                                (grid.width, 1)
    assert grid.get_slices_size(slice(None), slice(0, 3, 2)) == \
                                                (grid.width, 2)                                          
    assert grid.get_slices_size(slice(1,3), slice(0, 3, 2)) == \
                                                (2, 2)
    assert grid.get_slices_size(2, slice(None)) == (1, 3)

def test_transpose(grid):
    transposed_grid = grid.transposed()
    assert transposed_grid.width == grid.height
    assert transposed_grid.height == grid.width
    assert transposed_grid[2, 3] == 11
    assert transposed_grid[1, 2] == 6

def test_flatten(grid):
    assert grid.flatten() == list(range(12))