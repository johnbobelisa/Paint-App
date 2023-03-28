from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import *
from layers import *
from data_structures.referential_array import *
from data_structures.queue_adt import *
from data_structures.stack_adt import *
from data_structures.array_sorted_list import *
from data_structures.sorted_list_adt import *
from data_structures.abstract_list import *
from data_structures.bset import *

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

    

    def __init__(self) -> None:
        super().__init__()
        self.current_layers = None
        self.current_color = None
        self.is_undone = False


    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if self.current_layers == None:
            self.current_color = start
            return start

        elif self.current_layers == invert:
            new_layer = invert.apply(self.current_color, 0, 1, 1)
            self.current_color = new_layer
            return self.current_color
            
        else:
            new_layer = self.current_layers.apply(start, timestamp, x, y)
            self.current_color = new_layer
            return new_layer
       

    def add(self, layer: Layer) -> bool:
        if self.current_layers != layer:
            self.current_layers = layer
            return True
        else:
            return False
        
     
    def erase(self, layer: Layer) -> bool:
        if self.current_layers != None:
            self.current_layers = None
            return True        
        else:
            return False
    
    def special(self):
        self.current_layers = invert
        


class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    

    def __init__(self) -> None:
        layer_counter = 0
        temp = get_layers()
        for layer in temp:
            if layer == None:
                break
            layer_counter += 1
        
        self.current_layers = CircularQueue(100*layer_counter)
        self.current_color = None
        self.is_undone = False
        super().__init__()

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:

        if self.current_layers.is_empty():
            self.current_color = start
            return start

        else:
            for _ in range(self.current_layers.length):
                if self.current_color == None:
                    new_layer = self.current_layers.serve()
                    self.current_layers.append(new_layer)
                    served_layer = new_layer.apply(start, timestamp , x, y)
                    self.current_color = served_layer
                else:
                    new_layer = self.current_layers.serve()
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
    
    

    def __init__(self) -> None:
        super().__init__()
        self.current_layers = ArraySortedList(1)
        self.applying = BSet(10)
        self.not_applying = BSet(10)
        self.is_undone = False
        self.current_color = None


    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:

        if self.current_layers.is_empty():
            self.current_color = start
            return start
        
        else:
            
            applied_layers = self.applying.difference(self.not_applying)
            
            
            for layers in self.current_layers:
                if layers == None:
                    break    
                
                layer_index = layers.key
                if layer_index in applied_layers:
                    
                    if self.current_color == None:
                        layer_color = layers.value
                        new_layers = layer_color.apply(start,timestamp,x,y)
                        self.current_color = new_layers
                        
                    else:
                        layer_color_ = layers.value
                        new_layers = layer_color_.apply(self.current_color, timestamp, x, y)
                        self.current_color = new_layers
            
            return self.current_color
            
            
                
    def add(self, layer: Layer) -> bool:
        element = ListItem(value=layer, key=layer.index+1)
        if element not in self.current_layers:
            self.current_layers.add(element)
        
        self.applying.add(layer.index+1)
        return True
        


    def erase(self, layer: Layer) -> bool:
        element = ListItem(value=layer, key=layer.index+1)
        self.not_applying.add(layer.index+1)
        return True

    def special(self):
        #black, blue, darken, green, invert, lighten, rainbow, red, sparkle
        temporary_layers = ArraySortedList(0)
        the_index = 0

        item1 = ListItem(black, 1)
        item2 = ListItem(blue, 2)
        item3 = ListItem(darken, 3)
        item4 = ListItem(green, 4)
        item5 = ListItem(invert, 5)
        item6 = ListItem(lighten, 6)
        item7 = ListItem(rainbow, 7)
        item8 = ListItem(red, 8)
        item9 = ListItem(sparkle, 9)

        elements = item1, item2, item3, item4, item5, item6, item7, item8, item9

        for layers in self.current_layers:
            if layers == None:
                    break
            for items in elements:
                if items.value == layers.value:
                    temporary_layers.add(items)
                    
        n = temporary_layers.length 

        if n % 2 == 0:
            the_index = (n // 2) - 1
        else:
            the_index = n // 2


        temporary_layers.delete_at_index(the_index)
        self.current_layers = ArraySortedList(0)
        
        for elems in temporary_layers:
            if elems == None:
                break
            new_layer = elems.value
            self.add(new_layer)                 

        
