#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from maze import Maze, MazeCell

def test_initialize():
    maze = Maze(10, 5)
    assert maze.width == 10
    assert maze.height == 5

@pytest.fixture
def maze():
    a_maze = Maze(10, 5)
    return a_maze

def test_inside(maze):
    assert isinstance(maze[0, 0], MazeCell)
    assert maze[0, 0] is not maze[0, 1]

def test_wrong_size():
    with pytest.raises(ValueError):
        maze = Maze(-1, 10)
    with pytest.raises(ValueError):
        maze = Maze(10, -1)

def test_neighbour_normal_cell(maze):
    cell = maze[2, 2]
    neighbors = maze.get_neighbors(cell)
    assert len(neighbors) == 4
    assert maze[2, 1] in neighbors
    assert maze[1, 2] in neighbors
    assert maze[3, 2] in neighbors
    assert maze[2, 3] in neighbors

def test_neighbour_border_cell(maze):

    cell = maze[0, 2]
    neighbors = maze.get_neighbors(cell)
    assert len(neighbors) == 3
    assert maze[0, 1] in neighbors
    assert maze[1, 2] in neighbors
    assert maze[0, 3] in neighbors

def test_neighbour_corner_cell(maze):

    cell = maze[0, 0]
    neighbors = maze.get_neighbors(cell)
    assert len(neighbors) == 2
    assert maze[0, 1] in neighbors
    assert maze[1, 0] in neighbors

def test_open_frontier_h(maze):

    cell1 = maze[0, 0]
    cell2 = maze[1, 0]

    maze.open_frontier(cell1, cell2)

    assert cell1.edges == {'N':False, 'E':True, 'S':False, 'W':False}
    assert cell2.edges == {'N':False, 'E':False, 'S':False, 'W':True}

def test_open_frontier_v(maze):

    cell1 = maze[0, 0]
    cell2 = maze[0, 1]

    maze.open_frontier(cell1, cell2)

    assert cell1.edges == {'N':False, 'E':False, 'S':True, 'W':False}
    assert cell2.edges == {'N':True, 'E':False, 'S':False, 'W':False}

def test_open_frontier_wrong_cells(maze):

    cell1 = maze[0, 0]
    cell2 = maze[0, 2] # it's not beside the cell1

    maze.open_frontier(cell1, cell2)

    assert cell1.edges == {'N':False, 'E':False, 'S':False, 'W':False}
    assert cell2.edges == {'N':False, 'E':False, 'S':False, 'W':False}
