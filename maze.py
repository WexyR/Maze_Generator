#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from mygrid import Grid
from random import randint, choice, seed


class MazeCell():
    def __init__(self):
        self.edges = {'N':False, 'E':False, 'S':False, 'W':False}
        self.coords = (None, None)

class Maze(Grid):
    """Model of a Maze"""
    def __init__(self, width, height):
        super().__init__(width, height, value=MazeCell(), copy=True)
        self._set_coordinates_to_cells()

    def __str__(self):
        result = "_"*2*self.width + '\n'
        for row in self:
            line = '|'
            for cell in row:
                if cell.edges['S']:
                    line += " "
                else:
                    line += "_"

                if cell.edges['E']:
                    line += "_"
                else:
                    line += "|"
            result += line + '\n'
        return result


    def get_neighbors(self, cell):
        neighbors = set()
        x, y = cell.coords
        if x != 0:
            neighbors.add(self[x-1, y])
        if x != self.width-1:
            neighbors.add(self[x+1, y])
        if y != 0:
            neighbors.add(self[x, y-1])
        if y != self.height-1:
            neighbors.add(self[x, y+1])

        return neighbors

    def _set_coordinates_to_cells(self):
        for y, line in enumerate(self):
            for x, _ in enumerate(line):
                self[x, y].coords = (x, y)

    def open_frontier(self, cell_1, cell_2):
        cx, cy = cell_1.coords
        nx, ny = cell_2.coords
        if cx-nx == 1:
            # The next cell is on the left of the current cell
            cell_1.edges['W'] = True
            cell_2.edges['E'] = True
        elif cx-nx == -1:
            # The next cell is on the right of the current cell
            cell_1.edges['E'] = True
            cell_2.edges['W'] = True
        elif cy-ny == 1:
            # The next cell is on the top of the current cell
            cell_1.edges['N'] = True
            cell_2.edges['S'] = True
        elif cy-ny == -1:
            # The next cell is on the bottom of the current cell
            cell_1.edges['S'] = True
            cell_2.edges['N'] = True

    def generate(self):
        stack = []
        visited_cells = set()

        current_cell = self[0,0]
        visited_cells.add(current_cell)

        while len(visited_cells) != len(self):
            neighbors = self.get_neighbors(current_cell)
            neighbors -= visited_cells
            if neighbors:
                next_cell = choice(tuple(neighbors))
                stack.append(current_cell)
                self.open_frontier(current_cell, next_cell)
                current_cell = next_cell
                visited_cells.add(current_cell)
            elif stack:
                current_cell = stack.pop()
    
    def get_ways(self, cell):
        neighbors = set()
        x, y = cell.coords
        if cell.edges['N']:
            neighbors.add(self[x, y-1])
        if cell.edges['S']:
            neighbors.add(self[x, y+1])
        if cell.edges['E']:
            neighbors.add(self[x+1, y])
        if cell.edges['W']:
            neighbors.add(self[x-1, y])
        return neighbors


    def resolve(self, start_cell, end_cell):
        stack = []
        visited_cells = set()

        current_cell = start_cell
        visited_cells.add(current_cell)

        while not end_cell in visited_cells:
            neighbors = self.get_ways(current_cell)
            neighbors -= visited_cells
            if neighbors:
                next_cell = choice(tuple(neighbors))
                stack.append(current_cell)
                # self.open_frontier(current_cell, next_cell)
                current_cell = next_cell
                visited_cells.add(current_cell)
            elif stack:
                current_cell = stack.pop()
        stack.append(current_cell)
        return stack


if __name__ == "__main__":
    maze = Maze(30, 30)
    maze.generate()
    list_solution_cells = maze.resolve(maze[0,0], maze[29,29])
    list_solution_coords = [cell.coords for cell in list_solution_cells]
    print(maze)
    print(list_solution_coords)
