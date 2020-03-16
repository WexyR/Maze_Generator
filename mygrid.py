#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from collections.abc import Iterable
from copy import deepcopy

def n_wise(iterable, n):
    """Use to separate an iterable by n-elements groups"""
    a = iter(iterable)
    return zip(*[a] * n)

class Grid():
    
    def __init__(self, width=0, height=0, value=None, copy=False):
        if width < 1 or height < 1:
            raise ValueError("Wrong width or height value")

        if copy:
            self.grid = [[deepcopy(value) for _ in range(width)]
                                              for _ in range(height)]
        else:
            self.grid = [[value for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height

    @classmethod
    def from_iter(cls, width, height, iterable):
        values = list(iterable)
        len_values = len(values)
        if len_values != width*height:
            raise ValueError("Wrong number of values, received: "
                    "{}, expected: {}".format(len_values, width*height))
        new_instance = cls(width, height)
        for index, v in enumerate(values):
            new_instance.grid[index//width][index-index//width*width] = v
        return new_instance

    def __str__(self):
        result = ""
        for line in self.grid:
            for i, elt in enumerate(line):
                result += str(elt)
                if i == len(line)-1:
                    result += '\n'
                else:
                    result += ' '
        return result
    
    def __repr__(self):
        return str(self.grid)

    def __len__(self):
        """Return the number of elements of the grid"""
        return self.width*self.height

    def __eq__(self, other):
        return self.grid == other.grid

    def __getitem__(self, index):
        if type(index) == tuple:
            i, j = index
            
            if type(j) == slice and type(i) != slice:
                result = [line[i] for line in self.grid[j]]
            elif type(i) == slice and type(j) == slice:
                new_height = len(self.grid[j])
                new_width = len(self.grid[0][i])
                new_grid = Grid(new_width, new_height)
                for y, line in enumerate(self.grid[j]):
                    new_grid.grid[y] = line[i]
                result = new_grid
            else: # i slice, j non_slice OU i non-slice, j non slice
                result = self.grid[j][i]
                
        else:
            result = self.grid.__getitem__(index)
        return result
        
    def __setitem__(self, index, value):

        if type(index) == tuple:
            i, j = index
            if not type(i) == slice and not type(j) == slice:
                self.grid[j][i] = value
                return
        
            if type(i) == slice and type(j) != slice:
                def assign_grid():
                    self.grid[j][i] = value[:, 0]
                def assign_scalar():
                    self.grid[j][i] = [value] * len_slice

            elif type(j) == slice and type(i) != slice:
                def assign_grid(): 
                    for elts, v in zip(self.grid[j], value[0, :]):
                        elts[i] = v
                def assign_scalar():
                    values = [value] * len_slice
                    for elts, v in zip(self.grid[j], values):
                        elts[i] = v
            elif type(j) == slice and type(i) == slice:
                def assign_grid():
                    for line_slices, v in zip(self.grid[j], value.grid):
                        line_slices[i] = v
                        
                def assign_scalar():
                    slice_width = len(self.grid[0][i])
                    values = [value] * slice_width
                    for line_slices in self.grid[j]:
                        line_slices[i] = values
            isgrid = False
            if isinstance(value, Grid):
                isgrid = True
            len_slice = len(self[i, j])
            if isgrid:
                slice_w, slice_h = self.get_slices_size(i, j)

                if (slice_w, slice_h) != (value.width, value.height):
                    raise ValueError("Wrong grid dimension")
                assign_grid()
            else:
                assign_scalar()

        else:
            self.grid[index] = value


    def transposed(self):
        """Return the transposed Grid"""

        transgrid = Grid(self.height, self.width)
        transgrid.grid = [list(line) for line in zip(*self.grid)]
        return transgrid

    def flatten(self):
        """Return the flattened Grid: a list of all elements"""
        flat = list()
        for line in self.grid:
            for elt in line:
                flat.append(elt)
        return flat
    
    def get_slices_size(self, slice_x, slice_y):
        if isinstance(slice_x, slice):
            width = len(self.grid[0][slice_x])
        else:
            width = 1
        if isinstance(slice_y, slice):
            height = len(self.grid[slice_y])
        else:
            height = 1
        return width, height