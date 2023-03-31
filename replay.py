from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.queue_adt import *

class ReplayTracker:

    def __init__(self):
        """
        Args:
            self
        Raises:
            None
        Returns:
            None
        What it does:
            self.replay_actions: Queue to store replay actions
            self.is_replay: bool to determine whether replay is happening or not
        Complexity:
            Best case complexity == Worst case complexity == O(1)
        """
        self.replay_actions = CircularQueue(10000) #O(1)
        self.is_replay = False #O(1)

    def start_replay(self) -> None:
        """
        Args:
            self
        Raises:
            None
        Returns:
            None
        What it does:
            updates self.is_replay to True so no more actions can be added
            Called whenever we should stop taking actions, and start playing them back.
            Useful if you have any setup to do before `play_next_action` should be called.
        Complexity:
            Best case complexity == Worst case complexity == O(1)
        """
        self.is_replay = True #O(1)
            
    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """

        Args:
            action:PaintAction
            is_undo: bool
        Raises:
            TypeError: if action isn't of PaintAction type, and if is_undo isn't a boolean
        Returns:
            None
        What it does:
            Adds an action to the replay.

            `is_undo` specifies whether the action was an undo action or not.
            Special, Redo, and Draw all have this is False.

            Check if start_replay has been called, if it hasn't, add action and is_undo
            to self.replay_actions.

        Complexity:
            Best case complexity == Worst case complexity == O(1)

            The time complexity is O(1)        
        """
        
        if self.is_replay: #O(1)
            return
        
        if not isinstance(action, PaintAction):
            raise TypeError("action must be of PaintAction type")
        
        if not isinstance(is_undo, bool):
            raise TypeError("is_undo must be a boolean value")

        self.replay_actions.append((action, is_undo)) #O(1)

    def play_next_action(self, grid: Grid) -> bool:
        """
        Args:
            grid: Grid
        Raises:
            TypeError: if grid isn't of Grid() type
        Returns:
            bool
        What it does:
            Plays the next replay action on the grid.
            Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.
        Complexity:
            Best case complexity == Worst case complexity: O(n).
            the function has to apply undo or apply redo which is O(n) complexity.
        """

        if not isinstance(grid, Grid):
            raise TypeError("grid input must be of Grid() type")

        if not self.replay_actions.is_empty(): #O(1)
            action, is_undo = self.replay_actions.serve() #O(1)
            action:PaintAction

            if action == None: #O(1)
                return

            if is_undo: #O(1)
                action.undo_apply(grid) #O(n) -- Where n is the amount of element in the PaintAction Steps
            else:
                action.redo_apply(grid) #O(n) -- Where n is the amount of element in the PaintAction Steps
            return False
        return True

            
if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

