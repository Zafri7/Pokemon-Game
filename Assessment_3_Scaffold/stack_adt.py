"""
    Stack ADT and an array implementation. Defines a generic abstract
    stack with the usual methods.
"""

__author__ = 'Maria Garcia de la Banda, modified by Brendon Taylor and Alexey Ignatiev'
__docformat__ = 'reStructuredText'

"""
Authors: 	1) Tuan Muhammad Zafri
 		    2) Wang Qian
 		    3) Mohammed Salman Ulumuddin
		    4) Ally Teh Tze-Rou  
Last modified by: Tuan Muhammad Zafri on 26/05/2022 
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic
T = TypeVar('T')
from referential_array import ArrayR


class Stack(ABC, Generic[T]):
    """ Abstract Stack class. """
    def __init__(self) -> None:
        """ Object initializer. """
        self.length = 0

    @abstractmethod
    def push(self, item: T) -> None:
        """ Pushes an element to the top of the stack."""
        pass

    @abstractmethod
    def pop(self) -> T:
        """ Pops an element from the top of the stack."""
        pass

    @abstractmethod
    def peek(self) -> T:
        """ Pops the element at the top of the stack."""
        pass

    def __len__(self) -> int:
        """ Returns the number of elements in the stack."""
        return self.length

    def is_empty(self) -> bool:
        """ Returns True iff the stack is empty. """
        return len(self) == 0

    @abstractmethod
    def is_full(self) -> bool:
        """ Returns True iff the stack is full and no element can be pushed. """
        pass

    def clear(self):
        """ Clears all elements from the stack. """
        self.length = 0
    

class ArrayStack(Stack[T]):
    """ Implementation of a stack with arrays.
    
    Attributes:
         length (int): number of elements in the stack (inherited)
         array (ArrayR[T]): array storing the elements of the queue

    ArrayR cannot create empty arrays. So MIN_CAPCITY used to avoid this.
    """
    MIN_CAPACITY = 1 

    def __init__(self, max_capacity: int) -> None:
        """ Initialises the length and the array with the given capacity.
            If max_capacity is 0, the array is created with MIN_CAPACITY.
        """
        Stack.__init__(self)
        self.array = ArrayR(max(self.MIN_CAPACITY, max_capacity))
        
    def is_full(self) -> bool:
        """ True if the stack is full and no element can be pushed. """
        return len(self) == len(self.array)

    def push(self, item: T) -> None:
        """ Pushes an element to the top of the stack.
        :pre: stack is not full
        :raises Exception: if the stack is full
        """
        if self.is_full():
            raise Exception("Stack is full")
        self.array[len(self)] = item
        self.length += 1

    def pop(self) -> T:
        """ Pops the element at the top of the stack.
        :pre: stack is not empty
        :raises Exception: if the stack is empty
        """
        if self.is_empty():
            raise Exception("Stack is empty")
        self.length -= 1
        return self.array[self.length]

    def peek(self) -> T:
        """ Returns the element at the top, without popping it from stack.
        :pre: stack is not empty
        :raises Exception: if the stack is empty
        """
        if self.is_empty():
            raise Exception("Stack is empty")
        return self.array[self.length-1]

    def __str__(self) -> str:               
        """
        A method that creates and defines the str function (format) for the team when using arraystack.

        Time complexity: O(n) where n is the length of team because it loop to print all the pokemons
        """
        string = ""
        for i in range(len(self)-1,-1,-1):  #This loop is to print out all the pokemons in the stack
            string += str(self.array[i])
            if i > 0:
                string += ", "               #add a comma after a pokemon is printed out except the last one
        return string