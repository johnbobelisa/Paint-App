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

    def __init__(self, draw_style:str, x:int, y:int) -> None:
        """
        Args:
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x:int, y:int: The dimensions of the grid.

        Raises:
        -ValueError: If draw_style is not one of draw_style_options
        -TypeError: If x or y or brush_size is not an interger

        Returns:
        None

        What it does:
        Initialise the grid object.
        Should also intialise the brush size to the DEFAULT provided as a class variable.
        self.grid = ArrayR(x): Create a one dimensional array with x elements.
        for i in range(x): Loop through the x dimension of the grid.
        self.grid[i] = ArrayR(y): Create a new one dimensional array with y elements for each element in the outer array.
        for j in range(y): Loop through the height of the grid.

        Then we check what draw style is being used, and depending on what draw style has been received,
        we create an appropriate layerstore object to the current grid square.

        Complexity:
        -Worst Case: O(xy), where xy are the dimensions of the grid.
        -Best Case: O(xy), where xy are the dimensions of the grid.

        Because the operations involve straightforward assignment or accessing an element 
        in an array, which requires constant time regardless of the size of the grid, the 
        time complexity of each operation inside the loops is constant time, or O(1). 

        But, based on the number of iterations carried out by the nested loops, the time 
        complexity of the initialisation is then expressed as O(x*y), as we have to
        assign every possible combination of x and y in the grid with a corresponding layerstore. 
        """

        
        if draw_style not in self.DRAW_STYLE_OPTIONS: #O(1)
            raise ValueError("Invalid Draw Style, draw style must be one of draw style options!") #O(1)
        if not isinstance(x, int): #O(1)
            raise TypeError("x must be an integer!") #O(1)
        if not isinstance(y, int): #O(1)
            raise TypeError("y must be an integer!") #O(1)
        if not isinstance(self.DEFAULT_BRUSH_SIZE, int): #O(1)
            raise TypeError("DEFAULT_BRUSH_SIZE must be an integer!") #O(1)
        
        
        self.draw_style:str = draw_style #O(1)
        self.x:int = x #O(1)       
        self.y:int = y #O(1)
        self.brush_size:int = self.DEFAULT_BRUSH_SIZE #O(1)

        self.grid = ArrayR(x)  #O(x) - Create 1D array with x elements    

        for i in range(x):   #O(x) - iterate x times
            self.grid[i] = ArrayR(y) #O(y) - Create 1D array wtih y elements
            for j in range(y):  #O(y) iterate y times
                if self.draw_style == self.DRAW_STYLE_SET: #O(1)                               
                    self.grid[i][j] = SetLayerStore() #O(1)         
                elif self.draw_style == self.DRAW_STYLE_ADD: #O(1)
                    self.grid[i][j] = AdditiveLayerStore() #O(1)
                elif self.draw_style == self.DRAW_STYLE_SEQUENCE: #O(1)
                    self.grid[i][j] = SequenceLayerStore() #O(1)
        
       
    def __getitem__(self, index:int):
        """
        Args: 
        - index: int

        Raises:
        TypeError: if index not int

        Returns:
        Grid at a certain x and y coordinate, where we can access the layerstore

        What it does:
        The __getitem__ method returns the information stored in the inner array inside the 
        grid attribute of the Grid object for a given index x and y. 

        Complexity:
        - Worst case: O(1) - Element access inside array takes constant time
        - Best case: O(1) - Same reason as worst case
        Accessing an element in an array using an index takes constant time, so __getitem__ has a time complexity of O(1).
        """
        if not isinstance(index, int): #O(1)
            raise TypeError("index must be an integer!") #O(1)
        return self.grid[index] #O(1)
    
    def increase_brush_size(self):
        """
        Args: 
        - self

        Raises:
        TypeError: if index not int type

        Returns:
            None
        
        What it does:
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        
        Complexity:
        Best case: O(1)
        Worst case: O(1)

        This method has a constant time complexity of O(1) 
        since it only involves simple arithmetic operation.

        """

        if self.brush_size < self.MAX_BRUSH:    #O(1)
            self.brush_size += 1    #O(1)

         

    def decrease_brush_size(self):
        """
        Args: 
        - self

        Raises:
        TypeError: if index not int type

        Returns:
            None
        
        What it does:
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        
        Complexity:
        Best case: O(1)
        Worst case: O(1)

        This method has a constant time complexity of O(1) 
        since it only involves simple arithmetic operation.

        """

        if self.brush_size > self.MIN_BRUSH: #O(1)
            self.brush_size -= 1 #O(1)
            

    def special(self):
        """
        Args: self

        Raises:
            None
        
        Returns:
            None

        What it does:
        Activate the special affect on all grid squares.

        for i in range(self.x): iterates over width of grid
        for j in range(self.y): iterates over height of grid
        self.grid[i][j].special(): activates the layerstore special effect on corresponding grid coordinate

        Complexity:
        the code iterates over the x and y inputs of the grid using nested loops, where
        x and y are the dimensions of the grid. Hence, the time complexity is O(xy).
        """
        for i in range(self.x):     #O(x)
            for j in range(self.y): #O(y)
                self.grid[i][j]:LayerStore 
                self.grid[i][j].special() #O(1)
        
        
        
                

            

    