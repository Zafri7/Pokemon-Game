""" Hash Table ADT

Defines a Hash Table using Linear Probing for conflict resolution.
It currently rehashes the primary cluster to handle deletion.
"""
__author__ = 'Brendon Taylor, modified by Jackson Goerner'
__docformat__ = 'reStructuredText'
__modified__ = '21/05/2020'
__since__ = '14/05/2020'

"""
Authors: 	1) Tuan Muhammad Zafri
 		    2) Wang Qian
 		    3) Mohammed Salman Ulumuddin
		    4) Ally Teh Tze-Rou  
Last modified by: Tuan Muhammad Zafri on 29/05/2022 
"""

from referential_array import ArrayR
from typing import TypeVar, Generic
from potion import Potion
T = TypeVar('T')


class LinearProbePotionTable(Generic[T]):
    """
    Linear Probe Potion Table

    This potion table does not support deletion.

    attributes:
        count: number of elements in the hash table
        table: used to represent our internal array
        table_size: current size of the hash table
    """
    MIN_CAPACITY = 1 
    def __init__(self, max_potions: int, good_hash: bool=True, tablesize_override: int=-1) -> None:

        """
        A method to initialise the variables, conflict_count, probe_max, probe_total, count, max_potions, and good_hash
        
        Time complexity: O(max capacity) where max capacity is self.tablesize. Its default is set to double the max_potions but it will 
        accept any size that is >= max_potions and use that input as tablesize. 
        """
       
        # Statistic setting
        self.conflict_count = 0
        self.probe_max = 0
        self.probe_total = 0
        
        self.count = 0
        self.max_potions = max_potions
        self.good_hash = good_hash
        
        
        if tablesize_override == -1:
            self.tablesize = max_potions * 2
        else:
            self.tablesize = tablesize_override

        if self.tablesize < max_potions:
            raise ValueError("Not enough table size to contain all items")

        self.table = ArrayR (max(self.MIN_CAPACITY, self.tablesize))


        # raise NotImplementedError()



    def hash(self, potion_name: str) -> int: 

        """
        Choose to use good_hash or bad_hash function, use good_hash by default
        :post: returns a valid position (0 <= value < table_size)

        Time complexity: O(good_hash or bad_hash method), refer to potion.py
        """
        if self.good_hash:
            return Potion.good_hash(potion_name, self.tablesize)
         
        else:
            return Potion.bad_hash(potion_name, self.tablesize)



    def statistics(self) -> tuple:

        """
        A method to return the variables conflict_count, probe_total, and probe_max

        Time complexity: O(1) because it is only returning the values of the variables
        """
        return self.conflict_count, self.probe_total, self.probe_max



    def __len__(self) -> int:

        """
        A method to return number of elements in the hash table

        Time complexity: O(1) because it is only returning the variable count
        """
        return self.count



    def __linear_probe(self, key: str, is_insert: bool) -> int:

        """
        A method to find the correct position for this key in the hash table using linear probing

        Time complexity: The best case is O(K) first position is empty, 
                         where K is the size of the key
                         where O(K + N) when we've searched the entire table, 
                         where N is the table_size
        :raises KeyError: When a position can't be found
        """
        position = self.hash(key)  # get the position using hash
        probe_count = 0
        if is_insert and self.is_full():
            raise KeyError(key)

        for _ in range(len(self.table)):  # start traversing
            if self.table[position] is None:  # found empty slot
                if is_insert:
                    return position
                else:
                    raise KeyError(key)  # so the key is not in
            elif self.table[position][0] == key:  # found key
                return position
            else:  # there is something but not the key, try next
                position = (position + 1) % len(self.table)
                if probe_count == 0:
                    self.conflict_count += 1 
                self.probe_total += 1
                probe_count += 1
                self.probe_max = max(self.probe_max, probe_count)

        raise KeyError(key)



    def __contains__(self, key: str) -> bool:

        """
        A method to check if the given key is in the Hash Table. Will return True if the key is in the hash table,
        or else it will return False
        :see: #self.__getitem__(self, key: str)
        
        Time complexity: O(1) because it is only chekcing if the item is in the hash table
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True



    def __getitem__(self, key: str) -> T:

        """
        A method to get the item at a certain key
        :see: #self.__linear_probe(key: str, is_insert: bool)
        :raises KeyError: when the item doesn't exist

        Time complexity: O(1) for good_hash and O(n) for bad_hash where n is the number of items in hash table, refer hash_analysis.pdf
        """
        position = self.__linear_probe(key, False)
        return self.table[position][1]



    def __setitem__(self, key: str, data: T) -> None:

        """
        A method to get a (key, data) pair in our hash table
        :see: #self.__linear_probe(key: str, is_insert: bool)
        :see: #self.__contains__(key: str)
        pre condition is that the type of key needs to be a string

        Time complexity: O(1) for good_hash and O(n) for bad_hash where n is the number of items in hash table, refer hash_analysis.pdf
        """
        if type(key) != str:
            raise TypeError("key needs to be a string")
        if len(self) == len(self.table) and key not in self:
            raise ValueError("Cannot insert into a full table.")
        position = self.__linear_probe(key, True)

        if self.table[position] is None:
            self.count += 1
        self.table[position] = (key, data)



    def initalise_with_tablesize(self, tablesize: int) -> None:

        """
        A method to initialise a new array, with table size given by tablesize.
        
        Time complexity: O(n), where n is len(tablesize)
        """
        self.count = 0
        self.table = ArrayR(tablesize)



    def is_empty(self):

        """
        A method that returns whether the hash table is empty

        Time complexity: O(1) because it only returns True if hash table is empty
        """
        return self.count == 0



    def is_full(self):

        """
        A mehtod that returns whether the hash table is full

        Time complexity: O(1) because it returns True when hash table is full
        """
        return self.count == len(self.table)



    def insert(self, key: str, data: T) -> None:

        """
        Utility method to call our setitem method
        :see: #__setitem__(self, key: str, data: T)

        Time complexity: O(1) because it only initialise self[key] the value from the variabel, data
        """
        self[key] = data



    def __str__(self) -> str:

        """
        A method that returns all they key/value pairs in our hash table (no particular order)

        Time complexity: O(1) + O(N) where N is the table size because initialising result is 0(1) and O(N) as it will loop into the hash table
        """
        result = ""
        for item in self.table:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result

