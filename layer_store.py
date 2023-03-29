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
        """
        The time complexity for initializing self.current_layers and self.current_color is O(1)
        self.current_layers keeps track of the current layer
        self.current_color keeps track of the current color
        
        The time complexity is O(1), we are just initializing variables.
        """
        super().__init__()
        self.current_layers = None  #O(1)
        self.current_color = None   #O(1)
        
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        The time complexity of get_color is O(1)

        How get_color works:
        1. If the color has no layers, we set the current color to the given start parameter, and return start. 
        2. If the current layer is invert, we apply it to the current color, and update the current color with the new color,
        and then we return the current color.
        3. Otherwise, we apply the layer to the start color, update the current color with the new one, and return it.

        The time complexity for get_color, for all the conditions/steps above is O(1), the most we are doing is updating
        a variable and returning it. The apply method has constant time complexity as it will always apply to a tuple of 
        (r,g,b) values or applying a layer like 'black' just means we are drawing black.

        """
        if self.current_layers == None: 
            self.current_color = start      #O(1)
            return start                    #O(1)
        
        elif self.current_layers == invert:                       
            new_layer = invert.apply(self.current_color, timestamp, x, y) #O(1)
            self.current_color = new_layer                                #O(1)
            return self.current_color                                     #O(1)
            
        else:
            new_layer = self.current_layers.apply(start, timestamp, x, y) #O(1)
            self.current_color = new_layer                                #O(1)
            return new_layer                                              #O(1)
       

    def add(self, layer: Layer) -> bool:
        """
        If the layer we're adding is not the current layer, it means that adding this layer will 
        change the state of the layerstore, And so we return True. Otherwise, if the layerstore hasn't changed, return False.

        The time complexity is O(1), we are not doing any iterations or complex functions, we are just updating and checking
        a variable and returning a boolean. 
        """ 
        if self.current_layers != layer: #O(1)
            self.current_layers = layer  #O(1)
            return True                  #O(1)
        else:
            return False                 #O(1)
        
     
    def erase(self, layer: Layer) -> bool:
        """
        Erasing a layer just means setting the current layer to None,
        so if there exists a current layer that is not None, We return True as we are changing the state of the layer.
        Otherwise, if the layerstore hasn't changed, return False

        The time complexity is O(1) since we are just updating a variable and returning 
        a boolean without doing any iterations, etc.
        """
        if self.current_layers != None:  
            self.current_layers = None   #O(1)
            return True                  #O(1)
        else:
            return False                 #O(1)
    
    def special(self):
        """
        Set the current layer to invert.

        The time complexity is O(1) since we are just updating a variable without doing any iterations, etc.
        """
        if self.current_layers != invert:
            self.current_layers = invert     #O(1)
        


class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    

    def __init__(self) -> None:
        """
        self.layer_counter: keeps track of the amount of layers, Counts the amount of layers until it returns a None value,
        which means all the layers have been counted for.

        self.current_layers: A CircularQueue where the capacity is set to 100 times the amount of layers
        self.current_color: Keeps track of the current color. Initially None

        The time complexity is O(n). the iteration has a linear time complexity proportional to the number of layers.
        """
        self.layer_counter = 0  #O(1)
        temp = get_layers()     
        for layer in temp:      #O(n), where n is the amount of layers in the collection
            if layer == None:
                break
            self.layer_counter += 1  #O(1)
                                
        
        self.current_layers = CircularQueue(100*self.layer_counter) #O(1)
        self.current_color = None   #O(1)
        super().__init__() 

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        If there are no layers, set the current color to the given start color and return it.

        Otherwise, we iterate over the amount of layers in the queue. 

        If there isn't a color yet,  we remove and take the oldest remaining layer, then append it back to the queue. 
        Then, apply the oldest remaining layer to the 'start' color, and update the current color with it.

        else, we follow the same set of instructions as above, the only difference is that we apply the oldest remaning layer
        to the current color instead of the 'start' color.

        Finally, return the current color.

        The time complexity of get_color is O(n), where n is the number of layers in the queue. 
        he code iterates over the number of layers in the queue and performs a constant amount of operations.

        """

        if self.current_layers.is_empty():  
            self.current_color = start      #O(1)
            return start                    #O(1)

        else:
            for _ in range(self.current_layers.length):  #O(n)       
                if self.current_color == None:                      
                    new_layer:Layer = self.current_layers.serve()     #O(1)
                    self.current_layers.append(new_layer)              #O(1)
                    served_layer = new_layer.apply(start, timestamp , x, y) #O(1) 
                    self.current_color = served_layer   #O(1)
                else:
                    new_layer:Layer = self.current_layers.serve()               #O(1)     
                    self.current_layers.append(new_layer)                       #O(1)
                    served_layer = new_layer.apply(self.current_color, timestamp, x, y) #O(1)
                    self.current_color = served_layer   #O(1)                                

            return self.current_color #O(1)


    def add(self, layer: Layer) -> bool:
        """
        Set the current layer to the given layer if layer is a valid parameter, and return True.
        Otherwise, return False.

        The time complexity is O(1), we are only appending an item into the rear of the queue and returning
        a boolean.
        """
        if layer:
            self.current_layers.append(layer) 
            return True
        else:
            return False
    def erase(self, layer: Layer) -> bool:
        """
        Remove the oldest remaining layer in the self.current_layers queue.

        The time complexity is O(1), we are only removing a layer from the front of the queue.
        """
        self.current_layers.serve() 
        return True
    
    def special(self):
        """
        Create a stack with the same capacity as the queue, take out all the elements in the queue until it's empty and push
        all the elements into the stack. Then, take out all the elements in the stack until it's empty, and push all the 
        elements back into the queue. Now, all the elements in the queue will be in a reversed order.

        The time complexity is O(n), where n is the number of layers in the queue.
        This is because the code iterates over the entire queue twice: once to empty the queue and push 
        all the elements into the stack, and a second time to empty the stack and push it back into the queue to reverse it. 

        Although we are iterating over the queue twice, the size of the queue is still n, and therefore, the time complexity is O(n).

        """
        stack = ArrayStack(100*self.layer_counter)                                           
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
        """
        self.current_layers: Keeps track of the current layers using an array sorted list
        self.applying: Keeps track of the 'applying' layers using a set
        self.not_applying: Keeps track of the 'non-applying' layers using a set
        self.current_color: Keeps track of the current color

        The time complexity of initialising all these variables are O(1)
        """
        super().__init__()
        self.current_layers = ArraySortedList(1) 
        self.applying = BSet(10)    
        self.not_applying = BSet(10)    
        self.current_color = None   


    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:

        if self.current_layers.is_empty(): #If there are no layers currently,
            self.current_color = start     #set the current color to the start color
            return start                   #and return it 
        
        else:
            
            applied_layers = self.applying.difference(self.not_applying) #To find out what layers should be applied, 
                                                                         #we use the difference function where we take
                                                                         #all the layers that are in 'applying' but not
                                                                         #in 'not applying'
            for layers in self.current_layers:  #for all the items in the list
                layers:ListItem                          
                if layers == None:  
                    break    #break out of the loop if we've accounted for all the layers
                
                layer_index = layers.key           #if the layer's index is in 
                if layer_index in applied_layers:  #the applied layers set, 
                    
                    if self.current_color == None:                          #then we apply it to the 'start' color if
                        layer_color:Layer = layers.value                          #the current color doesn't exist
                        new_layers = layer_color.apply(start,timestamp,x,y) 
                        self.current_color = new_layers                     #and update the current color to the new one
                        
                    else:
                        layer_color_:Layer = layers.value                                          #Otherwise, we just take the layer
                        new_layers = layer_color_.apply(self.current_color, timestamp, x, y) #and apply it to the current color
                        self.current_color = new_layers                                      #and update the current color
            
            return self.current_color #return the current color
            
            
                
    def add(self, layer: Layer) -> bool:
        element = ListItem(value=layer, key=layer.index+1) #create an element of a ListItem() type
        if element not in self.current_layers:             #Check if the layer exists already, 
            self.current_layers.add(element)               #if it doesn't exist yet, add it to the list.
        
        self.applying.add(layer.index+1)                   #Makes the layer applying
        return True                                        #add the index of the layer, the additional "+1" here
                                                           #is to avoid TypeError('Set elements should be integers')


    def erase(self, layer: Layer) -> bool:                    
        self.not_applying.add(layer.index+1)                #Makes the layer not applying
        return True

    def special(self):
        #black, blue, darken, green, invert, lighten, rainbow, red, sparkle
        temporary_layers = ArraySortedList(0) #create a temporary sorted list
        the_index = 0                       

        item1 = ListItem(black, 1) 
        item2 = ListItem(blue, 2)
        item3 = ListItem(darken, 3)
        item4 = ListItem(green, 4)
        item5 = ListItem(invert, 5)         #layers in a lexicographical order
        item6 = ListItem(lighten, 6)
        item7 = ListItem(rainbow, 7)
        item8 = ListItem(red, 8)
        item9 = ListItem(sparkle, 9)

        elements = item1, item2, item3, item4, item5, item6, item7, item8, item9

        for layers in self.current_layers: #For all the layers in the list
            layers:ListItem
            if layers == None:  #if condition is met then we have accounted for all the layers
                    break
            for items in elements:  #for all the items in the element
                if layers.value == items.value: #if their layer.value is the same
                    temporary_layers.add(items) #we add the items to the temporary sorted list
                    
        n = len(temporary_layers)

        if n % 2 == 0:
            the_index = (n // 2) - 1 #if it's an even number of applying layers, select the lexicographically smaller of the two names
        else:
            the_index = n // 2 # Otherwise, select the median applying one

        if temporary_layers.is_empty():
            return
        
        temporary_layers.delete_at_index(the_index) #delete the median applying layer at the given index
        self.current_layers = ArraySortedList(0) #reset the current layers
        
        

        for elems in temporary_layers: #for items in the new sorted list
            elems:ListItem
            if elems == None:
                break
            new_layer = elems.value #get the layer value of the item
            self.add(new_layer) #call the add function to add it back to the current layers              

        
