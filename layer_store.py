from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import *
from layers import *
from referential_array import *
from queue_adt import *
from stack_adt import *
from array_sorted_list import *
from sorted_list_adt import *

class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """ 
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    current_layer = None
    current_color = None

    def __init__(self) -> None:
        super().__init__()


    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if self.current_layer == None:
            self.current_color = start
            return start

        elif self.current_layer == invert:
            new_layer = invert.apply(self.current_color, 0, 1, 1)
            self.current_color = new_layer
            return self.current_color
            
        else:
            new_layer = self.current_layer.apply(start, timestamp, x, y)
            self.current_color = new_layer
            return new_layer
       

    def add(self, layer: Layer) -> bool:
        self.current_layer = layer
        return True
        
     
    def erase(self, layer: Layer) -> bool:
        self.current_layer = None
        return True
    
    def special(self):
        self.current_layer = invert
        


class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    
    current_layers = CircularQueue(100)
    current_color = None

    def __init__(self) -> None:
        super().__init__()

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:

        if self.current_layers.is_empty():
            self.current_color = start
            return start

        elif self.current_color == None:
            for _  in range(self.current_layers.length):
                new_layer = self.current_layers.serve()
                self.current_layers.append(new_layer)
                served_layer = new_layer.apply(start, timestamp , x, y)
                self.current_color = served_layer
            return self.current_color

        else:
            for _ in range(self.current_layers.length):
                new_layer:Layer = self.current_layers.serve()
                self.current_layers.append(new_layer)
                served_layer = new_layer.apply(self.current_color, timestamp, x, y)
                self.current_color = served_layer
            return self.current_color

    def add(self, layer: Layer) -> bool:
        self.current_layers.append(layer)
        return True
        
    def erase(self, layer: Layer) -> bool:
        self.current_layers.serve()
        return True
    
    def special(self):
        stack = ArrayStack(100)

        while self.current_layers.is_empty() == False:
            served_layer = self.current_layers.serve()
            stack.push(served_layer)
        
        while stack.is_empty() == False:
            peeked_layer = stack.peek()
            stack.pop()
            self.current_layers.append(peeked_layer)
        

    

class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    current_layers = ArraySortedList(1)
    current_color = None

    def __init__(self) -> None:
        super().__init__()

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if self.current_layers.is_empty():
            self.current_color = start
            return start
        
        else:
            for layer in self.current_layers:
                if layer.applying == True:
                    layer_value = layer.value
                    if self.current_color == None:
                        new_layer = layer_value.apply(start, timestamp, x, y)
                        self.current_color = new_layer
                    
                    else:
                        new_layer = layer_value.apply(self.current_color, timestamp, x, y)
                        self.current_color = new_layer
                
                continue
                        
            return self.current_color
            
                
    def add(self, layer: Layer) -> bool:
        element = ListItem(layer, layer.index)
        element.applying = True
        self.current_layers.add(element)
        return True

    def erase(self, layer: Layer) -> bool:
        element = ListItem(layer, layer.index)
        for e in self.current_layers:
            if e == element:
                e.applying = False
                break
            continue
        return True
    
    def special(self):
        pass
    
        
    # def index_sort(lst:ArraySortedList(ListItem)):
    #     n = len(lst)
    #     for i in range(n):
    #         for j in range(n-i-1):
    #             if lst[j].key > lst[j+1].key:
    #                 lst[j], lst[j+1] = lst[j+1], lst[j]
    #     return lst
    
    
    # def alphabetical_sort(lst):
    #     n = len(lst)
    #     for i in range(n):
    #         for j in range(n-i-1):
    #             if lst[j] > lst[j+1]:
    #                 lst[j], lst[j+1] = lst[j+1], lst[j]
    #     return lst
