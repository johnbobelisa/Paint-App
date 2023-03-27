from __future__ import annotations
from action import PaintAction
from grid import Grid
from layer_store import *
from data_structures.stack_adt import *


class UndoTracker:

    def __init__(self) -> None:
        self.tree_of_actions = ArrayStack(10000)
        self.redo_branch = ArrayStack(10000)
        
    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """

        self.tree_of_actions.push(action)


    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """
        
        if self.tree_of_actions.is_empty():
            return None

        p_action:PaintAction = self.tree_of_actions.peek()

        if p_action == None:
            exit()
        
        for step in p_action.steps:
            x, y = step.affected_grid_square
            layer_state = grid[x][y]
            
            if layer_state.erase(step.affected_layer) == False:
                step.undo_apply(grid)
                layer_state.is_undone = True
        
        returned_action = self.tree_of_actions.pop()
        self.redo_branch.push(returned_action)
        return returned_action


    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """

        p_action:PaintAction = self.tree_of_actions.pop()


        if p_action == None:
            return

        for step in p_action.steps:
            x, y = step.affected_grid_square
            layer_state = grid[x][y]
            
            if layer_state.is_undone == True:
                step.redo_apply(grid)    

            else:
                return None
