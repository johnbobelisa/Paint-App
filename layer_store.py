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
        self.current_layers = None  #Keeps track of the current layer
        self.current_color = None   #Keeps track of the current color
        
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if self.current_layers == None: #If the color has no layers
            self.current_color = start  #we set the current color to the given start parameter
            return start                #and return start
        
        elif self.current_layers == invert:                       #If the current layer is invert
            new_layer = invert.apply(self.current_color, 0, 1, 1) #we apply it to the current color
            self.current_color = new_layer                        #and update it with the new color
            return self.current_color                             #and then we return the current color
            
        else:
            new_layer = self.current_layers.apply(start, timestamp, x, y) #Otherwise, we apply the layer to the start color
            self.current_color = new_layer                                #update the current color with the new one
            return new_layer                                              #and return it 
       

    def add(self, layer: Layer) -> bool: 
        if self.current_layers != layer: #If the layer we're adding is not the current layer,
            self.current_layers = layer  #it means that adding this layer will change the state of the layerstore
            return True                  #And so we return True
        else:
            return False                 #Otherwise, if the layerstore hasn't changed, return False
        
     
    def erase(self, layer: Layer) -> bool:
        if self.current_layers != None:  #Erasing a layer just means setting the current layer to None,
            self.current_layers = None   #so if there exists a current layer that is not None,  
            return True                  #We return True as we are changing the state of the layer
        else:
            return False                 #Otherwise, if the layerstore hasn't changed, return False
    
    def special(self):
        self.current_layers = invert     #Set the layer to invert
        


class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    

    def __init__(self) -> None:
        self.layer_counter = 0   #keep track of the amount of layers
        temp = get_layers()
        for layer in temp:      
            if layer == None:
                break
            self.layer_counter += 1  #Counts the amount of layer until it returns a None value,
                                #which means all the layers have been counted for 
        
        self.current_layers = CircularQueue(100*self.layer_counter) #Set the Queue capacity to 100 times the amount of layers
        self.current_color = None   #Keeps track of the current color
        super().__init__()

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:

        if self.current_layers.is_empty():  #If there are no layers,
            self.current_color = start      #Set the current color to the given start color
            return start                    #and return it

        else:
            for _ in range(self.current_layers.length):         #iterates over the amount of layers in the queue
                if self.current_color == None:                  #If there isn't a color yet, 
                    new_layer:Layer = self.current_layers.serve()     #we take the oldest remaining layer
                    self.current_layers.append(new_layer)       #then append it back to the queue
                    served_layer = new_layer.apply(start, timestamp , x, y) #apply the oldest remaining layer to the 'start' color
                    self.current_color = served_layer   #and update the current color with it 
                else:
                    new_layer:Layer = self.current_layers.serve()     #Otherwise, we follow the same set of instructions as above,
                    self.current_layers.append(new_layer)       #the only difference is that we apply the oldest remaning layer
                    served_layer = new_layer.apply(self.current_color, timestamp, x, y) #to the current color instead of
                    self.current_color = served_layer                                   #the 'start' color

            return self.current_color #return the current color


    def add(self, layer: Layer) -> bool:
        self.current_layers.append(layer) #set the current layer to the given layer
        return True
        
    def erase(self, layer: Layer) -> bool:
        self.current_layers.serve() #take out the oldest remaining layer
        return True
    
    def special(self):
        stack = ArrayStack(100*self.layer_counter)      #How special works:                                             
        while self.current_layers.is_empty() == False:  #1. Create a stack with the same capacity as the queue
            served_layer = self.current_layers.serve()  #2. take out all the elements in the queue until it's empty and push
            stack.push(served_layer)                    # all the elements into the stack
        
        while stack.is_empty() == False:                #3. take out all the elements in the stack until it's empty and push all
            peeked_layer = stack.peek()                 #the elements back into the queue. Now, all the elements in the queue,
            stack.pop()                                 #will be in a reversed order
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
        self.current_layers = ArraySortedList(1) #Keeps track of the current layers
        self.applying = BSet(10)    #Keeps track of the 'applying' layers
        self.not_applying = BSet(10)    #Keeps track of the 'non-applying' layers
        self.current_color = None   #Keeps track of the current color


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
                if items.value == layers.value: #if their layer.value is the same
                    temporary_layers.add(items) #we add the items to the temporary sorted list
                    
        n = temporary_layers.length 

        if n % 2 == 0:
            the_index = (n // 2) - 1 #if it's an even number of applying layers, select the lexicographically smaller of the two names
        else:
            the_index = n // 2 # Otherwise, select the median applying one


        temporary_layers.delete_at_index(the_index) #delete the median applying layer at the given index
        self.current_layers = ArraySortedList(0) #reset the current layers
        
        for elems in temporary_layers: #for items in the new sorted list
            elems:ListItem
            if elems == None:
                break
            new_layer = elems.value #get the layer value of the item
            self.add(new_layer) #call the add function to add it back to the current layers              

        
