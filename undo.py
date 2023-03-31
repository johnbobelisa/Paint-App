from __future__ import annotations
from action import PaintAction
from grid import Grid
from layer_store import *
from data_structures.stack_adt import *


class UndoTracker:

    def __init__(self) -> None:
        """
        Args:
            self
        Raises:
            None
        Returns:
            None
        What it does:
            self.tree_of_actions: Stack that acts as the tree of actions.
            self.redo_branch: Stack that holds the undone actions, to redo if needed.
        Complexity:
            Best case complexity == Worst case complexity == O(1)
        """
        self.tree_of_actions = ArrayStack(10000) #O(1)
        self.redo_branch = ArrayStack(10000) #O(1)       
        
    def add_action(self, action: PaintAction) -> None:
        """
        Args:
            action: Paintaction
        Raises:
            TypeError -- if action added is not of PaintAction type
        Returns:
            None
        What it does:
            Adds an action to the undo tracker.
            If your collection is already full,
            feel free to exit early and not add the action.
        Complexity:
            Best case complexity == Worst case complexity == O(1)
            Pushing an item onto a stack is O(1), as if it's full we exit out of the
            program instead of resizing. 
        """
        if not isinstance(action, PaintAction): #O(1)
            raise TypeError("action added must be of PaintAction type")
        
        self.tree_of_actions.push(action) #O(1)


    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Args:
            grid: Grid
        Raises:
            TypeError -- if grid input isn't of Grid() type 
        Returns:
            The action:PaintAction that was undone, or None.
        What it does:
            Undo an operation, and apply the relevant action to the grid.
            If there are no actions to undo, simply do nothing.         
        Complexity:
            Best case complexity == Worst case complexity: O(n)
            Where n is the length of the tree of actions stack. 
        """

        if not isinstance(grid, Grid): #O(1)
            raise TypeError("grid input must be of Grid() type")

        if self.tree_of_actions.is_empty(): #O(1)
            return None

        p_action:PaintAction = self.tree_of_actions.peek() #O(1)

        p_action.undo_apply(grid) #O(n)
        
        returned_action:PaintAction = self.tree_of_actions.pop() #O(1)    

        self.redo_branch.push(returned_action) #O(1)
        return returned_action


    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Args:
            grid: Grid
        Raises:
            TypeError -- if grid input isn't of Grid() type 
        Returns:
            The action:PaintAction that was redone, or None.
        What it does:
            redoes an operation, and apply the relevant action to the grid.
            If there are no actions to redo, simply do nothing.         
        Complexity:
            Best case complexity == Worst case complexity: O(n)
            Where n is the length of the redo_branch stack.
        """

        if not isinstance(grid, Grid): #O(1)
            raise TypeError("grid input must be of Grid() type")

        if self.redo_branch.is_empty(): #O(1)
            return None
        
        temp_storage:PaintAction = self.redo_branch.pop() #O(1)

        temp_storage.redo_apply(grid) #O(n) 
            
        self.tree_of_actions.push(temp_storage) #O(1)
        return temp_storage