"""
Authors: 	1) Tuan Muhammad Zafri
 		    2) Wang Qian
 		    3) Mohammed Salman Ulumuddin
		    4) Ally Teh Tze-Rou  
Last modified by: Ally Teh Tze-Rou on 29/05/2022 
"""

from primes import largest_prime

class Potion:

    def __init__(self, potion_type: str, name: str, buy_price: float, quantity: float) -> None:
        
        """
        A method to initialise the properties of the Potion object which are type, name, buy price and quantity of the potion

        Time complexity: O(1) as the method only intialise the properties of the potion
        """
        #raise NotImplementedError()
        self.potion_type = potion_type
        self.name = name
        self.buy_price = buy_price
        self.quantity = quantity
      
      

    @classmethod
    def create_empty(cls, potion_type: str, name: str, buy_price: float) -> 'Potion':

        """
        A method to create a potion object with 0 litres. (quantity = 0.0)

        Time complexity: O(1)
        """
        #raise NotImplementedError()
        cls.potion_type = potion_type
        cls.name = name
        cls.buy_price = buy_price
        cls.quantity = 0.0
        return Potion(cls.potion_type, cls.name, cls.buy_price, cls.quantity)



    @classmethod
    def good_hash(cls, potion_name: str, tablesize: int) -> int: #Ally did

        """
        1. The table size is ensured to be a prime number using the largest_prime() function. 
        This is to avoid sharing common factors with value.

        2. All ascii value of key(potion_name) is considered.

        3. This fucntion will use coefficients to multiply with value so that anagrams will not hash to the same position.
        The coefficient will also be different for every character in potion_name. To produce even sparse data.

        Time complexity: O(n log log n + k) where k is the length of the potion_name string and n is the integer tablesize 
                         Note that this is just time comlexity to produce the position to hash, how this function affects the complexity of inserting
                         an item is in hash analysis.pdf
        """
  
        cls.tablesize = largest_prime(tablesize)
        value = 0
        a = 31397
        b = 27179
        for char in potion_name:
            value = (value * a + ord(char)) % cls.tablesize
            a = a * b % (cls.tablesize-1)
        return value



    @classmethod
    def bad_hash(cls, potion_name: str, tablesize: int) -> int:

        """
        1. This bad_has function will only use the ascii value of the first character in the key, (potion_name).
        So all key ending with the same letter will be hashed to the same positon.

        2. The tablesize is also guarenteed to not be a prime number. When it is not a prime, there will be many values that 
        share a common factor with tablesize and will hash to the same position.

        For the reasons above, this will produce a hash function with huge clusters and results in many conflict and collision.
        
        Time complexity: O(n log log n + k) where k is the length of the potion_name string and n is the integer tablesize 
                         Note that this is just time comlexity to produce the position to hash, how this function affects the complexity of inserting
                         an item is in hash analysis.pdf
        """
        value = 0
        cls.tablesize = largest_prime(tablesize) + 1
        for char in potion_name:
            value = (ord(char)) % cls.tablesize
        return value



    def __str__(self):

        """
        A method to return the indication of the type, price and the quantity of the potion(s)
        Prints out the Potion object attribute, potion name, type, buy price and quantity.

        Time complexity: O(k) where k is the string created without formatting
        """

        return str("{}'s potion_type = {}, buy_price = {} and potion_quantity = {}").format(self.name, self.potion_type, self.buy_price, self.quantity) 

  
        

    
        
