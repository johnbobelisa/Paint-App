from __future__ import annotations
from action import PaintAction
from grid import Grid
from layer_store import *
from data_structures.stack_adt import *


class UndoTracker:

    def __init__(self) -> None:
        self.tree_of_actions = ArrayStack(10000)   #Stack that acts as the tree of actions
        self.redo_branch = ArrayStack(10000)       
        
    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """

        self.tree_of_actions.push(action) #add an action to the stack


    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """
        
        if self.tree_of_actions.is_empty():
            return None

        p_action:PaintAction = self.tree_of_actions.peek()

        p_action.undo_apply(grid)
        
        returned_action = self.tree_of_actions.pop()
        self.redo_branch.push(returned_action)
        return returned_action


    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        if self.redo_branch.is_empty():
            return None
        
        temp_storage:PaintAction = self.redo_branch.pop()

        temp_storage.redo_apply(grid)
            
        self.tree_of_actions.push(temp_storage)
        return temp_storage