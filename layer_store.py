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
    What it does:
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self) -> None:
        """
        Args:
            self
        Raises:
            None
        Returns:
            None
        What it does:
            Intitialize variables:
                -self.current_layers = None - keeps track of the current layer  
                -self.current_color = None - keeps track of the current color
                -self.is_special = False - keeps track if special is called or not  

        Complexity:
            The time complexity for initializing self.current_layers and self.current_color is O(1)
            self.current_layers: keeps track of the current layer
            self.current_color: keeps track of the current color
        
        Best case complexity == Worst case complexity == O(1), we are just initializing variables.
        """
        super().__init__()
        self.current_layers = None  #O(1)
        self.current_color = None #O(1)
        self.is_special = False   #O(1)
        
    def get_color(self, start:tuple[int, int, int], timestamp:int, x:int, y:int) -> tuple[int, int, int]:
        """
        Args:
            start: A tuple of (r,g,b) colors
            timestamp: int
            x: int - position from width dimension
            y: int - position from height dimension

        Raises:
            TypeError: if timestamp, x or y is not an integer and if start not a tuple of a tuple of (r,g,b) integers

        Returns:
            start:(r,g,b)-- if there are no layers currently
            self.current_color:(r,g,b) -- if there is a layer 

        What it does:
            if self.current_layers == None: 
            If the color has no layers, we set the current color to the given start parameter, and return start. 

            elif self.current_layers == invert:
            If the current layer is invert, we apply it to the current color, and update the current color with the new color,
            and then we return the current color.

            Otherwise, we apply the layer to the start color, update the current color with the new one, and return it.

        Complexity:
            The time complexity of get_color is O(1)
            Best case complexity == Worst case complexity == O(1), the most we are doing is updating a variable and returning it. 
            The apply method has constant time complexity as it will always apply to a fixed tuple of (r,g,b) values.

        """
        if not isinstance(start, tuple) and len(start) == 3 and all(isinstance(i, int) for i in start): #O(1)
            raise TypeError("start must be a tuple of (r,g,b) integers") 
        if not isinstance(timestamp, int): #O(1)
            raise TypeError("timestamp must be an integer")
        if not isinstance(x, int): #O(1)
            raise TypeError("x must be an integer")
        if not isinstance(y, int): #O(1)
            raise TypeError("y must be an integer")

        if self.current_layers == None: #O(1)
            self.current_color = start  #O(1)
            return start #O(1)
        
        else:
            if self.is_special == True: #O(1)
                return self.current_color #O(1)
            else:
                new_layer = self.current_layers.apply(start, timestamp, x, y) #O(1)
                self.current_color = new_layer #O(1)
                return self.current_color  #O(1)
       

    def add(self, layer: Layer) -> bool:
        """
        Args:
            layer:Layer - the layer to add
        Raises:
            TypeError: if layer isn't a Layer class type
        Returns:
            bool: True if state of layer has changed, False otherwise.

        What it does:
            If the layer we're adding is not the current layer, it means that adding this layer will 
            change the state of the layerstore, And so we return True. Otherwise, if the layerstore hasn't changed, return False.

        Complexity:
            Best case complexity == Worst case complexity == O(1), we are not doing any iterations or complex functions, 
            we are just updating and checking a variable and returning a boolean. 
        """ 
        if not isinstance(layer, Layer): #O(1)
            return TypeError("layer must be a Layer Class type")

        if self.current_layers != layer: #O(1)
            self.current_layers = layer  #O(1)
            return True  #O(1)
        else:
            return False #O(1)
        
     
    def erase(self, layer: Layer) -> bool:
        """
        Args:
            layer:Layer -- Irrelavant as erasing a layer just makes it None

        Raises:
            None

        Returns:
            bool: True if state of layer has changed, False otherwise.

        What it does:
            Erasing a layer just means setting the current layer to None,
            so if there exists a current layer that is not None, We return True as we are changing the state of the layer.
            Otherwise, if the layerstore hasn't changed, return False
        Complexity:
            Best case complexity == Worst case complexity == O(1), since we are just updating a variable and returning 
            a boolean without doing any iterations, etc.
        """
        if self.current_layers != None:  #O(1)
            self.current_layers = None   #O(1)
            return True   #O(1)
        else:
            return False  #O(1)
    
    def special(self):
        """
        Args:
            None

        Raises:
            None

        Returns:
            None

        What it does:
            Invert the current color without changing the current layer

        Best case complexity == Worst case complexity == O(1), since we are just 
        updating a variable without doing any iterations and apply is constant time
        because it always applies to a fixed (r,g,b) value tuple
        """
        special_layer = invert.apply(self.current_color, 0 , 0, 0) #O(1)
        self.is_special = True #O(1)
        self.current_color = special_layer #O(1)
                                                               
class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    
    def __init__(self) -> None:
        """
        Args:
            self
        Raises:
            None
        Returns:
            None

        What it does:
            self.layer_counter: keeps track of the amount of layers. 

            for layer in temp: Counts the amount of layers until it returns a None value,
            which means all the layers have been counted for, and increment self.layer_counter

            self.current_layers: A CircularQueue where the capacity is set to 100 times the amount of layers
            self.current_color: Keeps track of the current color. Initially None

        Complexity:
            Best case complexity == Worst case complexity == O(n). Where n is the amount of layers.
            The time complexity is O(n). the iteration has a linear time complexity proportional to the number of layers.
            All the other operations (initializing variable, etc) are constant.           
        """
        self.layer_counter = 0  #O(1)
        temp = get_layers()     #O(1)
        for layer in temp:      #O(n), where n is the amount of layers in the 'temp' collection
            if layer == None:   #O(1)
                break 
            self.layer_counter += 1  #O(1)
                                
        
        self.current_layers = CircularQueue(100*self.layer_counter) #O(1)
        self.current_color = None   #O(1)
        super().__init__() #O(1)

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Args:
            start: A tuple of (r,g,b) colors
            timestamp: int
            x: int - position from width dimension
            y: int - position from height dimension

        Raises:
            TypeError: if timestamp, x or y is not an integer and if start not a tuple of a tuple of (r,g,b) integers

        Returns:
            self.current_color: tuple[int, int, int] --  (r,g,b) color

        What it does:
            If there are no layers, set the current color to the given start color and return it.

            Otherwise, we iterate over the amount of layers in the queue. 

            If there isn't a color yet, we remove and take the oldest remaining layer, then append it back to the queue. 
            Then, apply the oldest remaining layer to the 'start' color, and update the current color with it.

            else, we follow the same set of instructions as above, the only difference is that we apply the oldest remaning layer
            to the current color instead of the 'start' color.

            Finally, return the current color.

        Complexity:
            Best case complexity = O(n) == Worst case complexity = O(n) -- when there 
            are n layers in the queue, and we need to iterate over all of them to apply each layer to the current color. 

            The time complexity of get_color is O(n), where n is the number of layers in the queue. 
            The code iterates over the number of layers in the queue and performs a constant amount of operations.

        """

        if not isinstance(start, tuple) and len(start) == 3 and all(isinstance(i, int) for i in start): #O(1)
            raise TypeError("start must be a tuple of (r,g,b) integers") 
        if not isinstance(timestamp, int): #O(1)
            raise TypeError("timestamp must be an integer")
        if not isinstance(x, int): #O(1)
            raise TypeError("x must be an integer")
        if not isinstance(y, int): #O(1)
            raise TypeError("y must be an integer")

        if self.current_layers.is_empty(): #O(1)
            self.current_color = start #O(1)
            return start #O(1)

        else:
            for _ in range(self.current_layers.length):  #O(n) - where n is the number of layers in the queue    
                if self.current_color == None: #O(1)                    
                    new_layer:Layer = self.current_layers.serve() #O(1)
                    self.current_layers.append(new_layer) #O(1)
                    served_layer = new_layer.apply(start, timestamp , x, y) #O(1) 
                    self.current_color = served_layer   #O(1)
                else:
                    new_layer:Layer = self.current_layers.serve() #O(1)     
                    self.current_layers.append(new_layer) #O(1)
                    served_layer = new_layer.apply(self.current_color, timestamp, x, y) #O(1)
                    self.current_color = served_layer   #O(1)                                

            return self.current_color #O(1)


    def add(self, layer: Layer) -> bool:
        """
        Args:
            layer:Layer - the layer to add
        Raises:
            TypeError -- If layer not a Layer Class type
        Returns:
            bool
        What it does:
            Adds the current layer to the CircularQueue if layer is a valid parameter, and return True.
        Complexity:
            Best case complexity == Worst case complexity == O(1), we are only appending an item into 
            the rear of the queue and returning a boolean.
        """
        if not isinstance(layer, Layer): #O(1)
            return TypeError("layer must be a Layer Class type")
        
        self.current_layers.append(layer) #O(1), Queue implementation doesn't have resize
        return True
        
    def erase(self, layer: Layer) -> bool:
        """
        Args:
            layer:Layer -- Irrelavant as erasing just removes the layer from the Queue's front
        
        Raises:
            None    

        Returns:
            bool    
                
        What it does:    
            Remove the oldest remaining layer in the self.current_layers queue.

        Complexity:
            Best case complexity == Worst case complexity == O(1), we are only removing a layer from the front of the queue.
        """
        self.current_layers.serve() #O(1)
        return True
    
    def special(self):
        """
        Args:
            self
        Raises:
            None
        Returns:
            None
        What it does:
            The special mode on an additive layer reverses the "ages" of each layer, so the oldest layer is now the youngest 
            layer, and so on.

            First, Create a stack with the same capacity as the queue, take out all the elements in the queue until it's empty and push
            all the elements into the stack. Then, take out all the elements in the stack until it's empty, and push all the 
            elements back into the queue. Now, all the elements in the queue will be in a reversed order.
        Complexity:

            Best case complexity == Worst case complexity == O(n)

            The time complexity is O(n), where n is the number of layers in the queue.
            This is because the code iterates over the entire queue twice: once to empty the queue and push 
            all the elements into the stack, and a second time to empty the stack and push it back into the queue to reverse it. 

            In the second iteration, the code iterates over the number of layers in the stack, 
            which is equal to the number of layers in the queue. So the overall time complexity 
            of the function is O(n + n), which simplifies to O(n).

        """
        stack = ArrayStack(100*self.layer_counter)                                           
        while self.current_layers.is_empty() == False: #O(1)
            served_layer = self.current_layers.serve() #O(1)
            stack.push(served_layer) #O(1) -- stack doesn't have resize implementation                  
        
        while stack.is_empty() == False: #O(1)               
            peeked_layer = stack.peek() #O(1)                
            stack.pop() #O(1)                                
            self.current_layers.append(peeked_layer) #O(1)
        
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
        Args:
            self
        Raises: 
            None
        Returns:
            None
        What it does:
            self.current_layers: Keeps track of the current layers using an array sorted list
            self.applying: Keeps track of the 'applying' layers using a set
            self.not_applying: Keeps track of the 'non-applying' layers using a set
            self.current_color: Keeps track of the current color

        Complexity:
            Best case complexity == Worst case complexity == O(1)

            The time complexity of initialising all these variables are O(1)
        """
        super().__init__()
        self.current_layers = ArraySortedList(1) 
        self.applying = BSet(10)    
        self.not_applying = BSet(10)    
        self.current_color = None   


    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """

        Args:
            start: A tuple of (r,g,b) colors
            timestamp: int
            x: int - position from width dimension
            y: int - position from height dimension

        Raises:
            TypeError: if timestamp, x or y is not an integer and if start not a tuple of a tuple of (r,g,b) integers

        What it does:   
            if self.current_layers.is_empty(): If there are no layers currently, 
            set the current color to the start color and return it.

            Otherwise, 
            aplied_layers = self.applying.difference(self.not_applying): To find out what layers should 
            be applied, we use the difference method where we take all the layers that are in 'applying' 
            but not in 'not applying'

            for layers in self.current_layers: for all the items in the list
            if layers == None: break out of the loop if we've accounted for all the layers
            layer_index = layers.key: take the layer.key value out of the ListItem() object 
            if layer_index in applied_layers: if the layer's index is in the applied layers set

            if self.current_color == None: then we apply it to the 'start' color if the current color doesn't exist
            and update the current color to the new one

            Otherwise, we just take the layer and apply it to the current color and update the current color.

            Finally, return the current color
        Complexity:
            Best case complexity = O(1). when the first element of the input array is the target value.
            the function would return immediately without iterating over any of the remaining elements. 
            In this case, the time complexity would be O(1).

            Worst case complexity = O(n+m). where n is the number of layers in the self.current_layers and m is the
            amount of elements in the applied_layers set. 
        """

        if not isinstance(start, tuple) and len(start) == 3 and all(isinstance(i, int) for i in start): #O(1)
            raise TypeError("start must be a tuple of (r,g,b) integers") 
        if not isinstance(timestamp, int): #O(1)
            raise TypeError("timestamp must be an integer")
        if not isinstance(x, int): #O(1)
            raise TypeError("x must be an integer")
        if not isinstance(y, int): #O(1)
            raise TypeError("y must be an integer")

        if self.current_layers.is_empty(): #O(1)
            self.current_color = start #O(1)
            return start #O(1)                 
        
        else:
            
            applied_layers:BSet = self.applying.difference(self.not_applying) #O(n+m)
                                                    
            for layers in self.current_layers:#O(n) - where n is the amount of elements in the list
                layers:ListItem  #O(1)                        
                if layers == None:  #O(1)
                    break    
                layers.key:int
                layer_index:int = layers.key #O(1)          
                if layer_index in applied_layers: #O(m) - where m is the amount of elements in the set
                    
                    if self.current_color == None: #O(1)                       
                        layer_color:Layer = layers.value #O(1)                          
                        new_layers = layer_color.apply(start,timestamp,x,y) #O(1)
                        self.current_color = new_layers #O(1)                    
                        
                    else:
                        layer_color_:Layer = layers.value #O(1)                                       
                        new_layers = layer_color_.apply(self.current_color, timestamp, x, y) #O(1)
                        self.current_color = new_layers #O(1)                                     
            
            return self.current_color #O(1) 
            
    def add(self, layer: Layer) -> bool:
        """
        Args:
            layer:Layer - the layer to add
        Raises:
            TypeError -- If layer not a Layer Class type
        Returns:
            bool -- True
        What it does:
            Create an element of a ListItem() type, Check if the layer exists already, 
        if it doesn't exist yet, add it to the list. Makes the layer applying by adding the index
        of the layer to the applying Bset. the additional "+1" here is to avoid "TypeError ('
        Set elements should be integers')"

        Complexity:
        Best case complexity = O(1) --  if the layer already exists in self.current_layers 
        Worst case complexity = O(n) -- if when adding, the list is full and needs to be resized

        The average time complexity is O(n) as we are on average traversing through self.current_layers
        to check whether element is in it or not.
        """
        if not isinstance(layer, Layer): #O(1)
            return TypeError("layer must be a Layer Class type")

        element = ListItem(value=layer, key=layer.index+1) #O(1)
        if element not in self.current_layers: #O(n)             
            self.current_layers.add(element) #O(log n)              
        
        self.applying.add(layer.index+1) #O(1)                   
        return True

    def erase(self, layer: Layer) -> bool:
        """
        Args:
            layer -- the layer to be erased
        Raises:
            TypeError -- If layer not a Layer Class type
        Returns:
            bool
        What it does:
            Makes the layer non applying by adding it to the not-applying Bset.
        Complexity:
            Best case complexity == Worst case complexity == O(1)
        """
        if not isinstance(layer, Layer): #O(1)
            return TypeError("layer must be a Layer Class type")

        self.not_applying.add(layer.index+1) #O(1)                
        return True

    def special(self):
        """
        Args:
            self
        Raises:
            None
        Returns:
            None
        What it does:
            Sort the layers in a lexicographical order by creating a ListItem() instance for each
        layer along with their ordered keys. 

        the_index: variable that holds the index for the median applying layer
        temporary_layers = ArraySortedList(0): Create a temporary sorted list
        elements: variable that holds all ListItem instances made

        for layers in self.current_layers: For all the items in the list, if layers is None then we have 
        accounted for all the layers.

        for items in elements: for all the items in the element variable, if their item.value(layer) is the same,
        then we add the items to the temporary sorted list.

        if n % 2 == 0: if it's an even number of applying layers, select the lexicographically smaller of the two names.
        Otherwise, select the median applying one.

        temporary_layers.delete_at_index(the_index): delete the median applying layer at the given index
        self.current_layers = ArraySortedList(0): reset the current layers

        for elems in temporary_layers: #for items in the new sorted list, get the layer value of the item
        and call the add function to add it back to the recently reset current layers.

        Complexity:
        Best-case complexity: O(n log n) -- when the input layers are already sorted lexicographically, 
        resulting in no swaps during sorting.

        Worst-case complexity: O(n^2 log n) -- when the input layers are reverse sorted lexicographically, 
        resulting in n^2 swaps.   
        """
        #black, blue, darken, green, invert, lighten, rainbow, red, sparkle
        temporary_layers = ArraySortedList(0) #O(1)
        the_index:int = 0  #O(1)                     

        item1 = ListItem(black, 1) 
        item2 = ListItem(blue, 2)
        item3 = ListItem(darken, 3)
        item4 = ListItem(green, 4)
        item5 = ListItem(invert, 5)         
        item6 = ListItem(lighten, 6)
        item7 = ListItem(rainbow, 7)
        item8 = ListItem(red, 8)
        item9 = ListItem(sparkle, 9)

        elements = item1, item2, item3, item4, item5, item6, item7, item8, item9 #O(1)

        for layers in self.current_layers: #O(n) where n is the amount of elements in self.current_layers list
            layers:ListItem
            if layers == None: #O(1) 
                    break
            for items in elements: #O(1)  
                if layers.value == items.value: #O(1)
                    temporary_layers.add(items) #O(log n) 
                    
        n = temporary_layers.length #O(1)

        if n % 2 == 0: #O(1)
            the_index = (n // 2) - 1 #O(1)
        else: 
            the_index = n // 2 #O(1)

        if temporary_layers.is_empty(): #O(1)
            return
        
        temporary_layers.delete_at_index(the_index) #O(log n) -- n is the length of temporary_layers
        self.current_layers = ArraySortedList(0) #O(1)
        
        for elems in temporary_layers: #O(n)
            elems:ListItem
            if elems == None:#O(1)
                break
            new_layer = elems.value #O(1)
            self.add(new_layer)  #O(log n)           

        
