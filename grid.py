from __future__ import annotations
from layer_store import *
from data_structures.referential_array import *

class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x:int, y:int) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.
        

        the code iterates over the x and y inputs of the grid using nested loops, where
        x and y are the dimensions of the grid. Hence, the time complexity is O(xy).

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """

        self.draw_style = draw_style
        self.x = x
        self.y = y
        self.brush_size:int = self.DEFAULT_BRUSH_SIZE

        self.grid = ArrayR(x)      

        for i in range(x):                  #O(x) time complexity, where x is the width 
            self.grid[i] = ArrayR(y)    
            for j in range(y):              #O(y) time complexity, where y is the height
                if self.draw_style == self.DRAW_STYLE_SET:                                 
                    self.grid[i][j] = SetLayerStore()       #O(1)         
                elif self.draw_style == self.DRAW_STYLE_ADD:   
                    self.grid[i][j] = AdditiveLayerStore()     #O(1)
                elif self.draw_style == self.DRAW_STYLE_SEQUENCE:
                    self.grid[i][j] = SequenceLayerStore()  #O(1)
        

    #How the grid works:
    #1.Set the grid to an empty(None Value) array of length x, where x is the width of the grid (line 36)
    #2.For each "space" created, we want to fill that space with an array of length y, where y is the height of the grid (line 38-39)
    #3.For each "space" created in the array of length y, we want to set these values to a LayerStore depending on the draw style (line 40-46)
    
       
    def __getitem__(self, index):
        return self.grid[index] 
    
    #4.So now getting a certain "space" of grid[x][y] at a certain index is just grabbing the information from the
    #smaller array inside the grid, and so this is the purpose of __getitem__ 
    
    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.

        The time complexity is constant as we are using an arithmetic operation (addition)
        to increment the size of the brush

        """

        if self.brush_size < self.MAX_BRUSH:    #O(1)
            self.brush_size += 1    #O(1)

         

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.

        The time complexity is constant as we are using an arithmetic operation (subtraction)
        to decrement the size of the brush

        """

        if self.brush_size > self.MIN_BRUSH: #O(1)
            self.brush_size -= 1 #O(1)
            

    def special(self):
        """
        Activate the special affect on all grid squares.

        the code iterates over the x and y inputs of the grid using nested loops, where
        x and y are the dimensions of the grid. Hence, the time complexity is O(xy).
        """
        for i in range(self.x):     #O(x)
            for j in range(self.y): #O(y)
                self.grid[i][j].special() #O(1)
        
        
                

            

    