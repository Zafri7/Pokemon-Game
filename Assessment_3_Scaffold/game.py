"""
Authors: 	1) Tuan Muhammad Zafri
 		    2) Wang Qian
 		    3) Mohammed Salman Ulumuddin
		    4) Ally Teh Tze-Rou  
Last modified by: Tuan Muhammad Zafri on 29/05/2022 
"""

from __future__ import annotations
from potion import Potion
from hash_table import LinearProbePotionTable
from random_gen import RandomGen
from avl import AVLTree
# ^ In case you aren't on Python 3.10
from random_gen import RandomGen

class Game:
    

    def __init__(self, seed=0) -> None:

        """
        This method initialises the instance variables rand, hashtable, tree, length_potion_with_quantity, and tree_solvegame.

        Time complexity: O(1) as it only calls the function RandomGen and initialises the values to the variable.
        """
        self.rand = RandomGen(seed=seed)
        self.hashtable = None
        self.tree = None 
        self.length_potion_with_quantity = 0
        self.tree_solvegame = None
      
    

    def set_total_potion_data(self, potion_data: list) -> None:

        """
        A method to set total potion data in the hash table, it will call the insert function and insert the data into the hash table.
        
        Time complexity: O(2n + n) where n is the size of potion_data, 
                         O(2n) when calling the LinearProbePotionTable class, it will initialise
                         an array with size of len(potion_data)*2. O(n) is the for loop that loops n times. 
                         create_empty method creates a Potion object with quantity 0 and this is O(1),
                         inserting an item into a hash table is also O(1).
        """
        self.hashtable = LinearProbePotionTable(len(potion_data), True, len(potion_data)*2)
        for i in range (len(potion_data)):
            p = Potion.create_empty(potion_data[i][0],potion_data[i][1],potion_data[i][2])
            self.hashtable.insert(potion_data[i][1],p)
          




    def add_potions_to_inventory(self, potion_name_amount_pairs: list[tuple[str, float]]) -> None:

        """
        I updated the quantity of potions in the hashtable for the potion_name that are in the list potion_name_amount_pairs.
        Next, I created an avl tree to store the potions that are only in potion_name_amount_pairs list because the vendors can only
        sell potions with positive quantity. This avl tree will use the buy price of the potion as the key and the Potion objecy as the data.


        Time complexity: O(C * log N)
                        where C is the length of potion_name_amount_pairs, N is the number of potions provided in set_total_potion_data.
                        The for loop will run C times and the log N comes from inserting items into the avl tree. It is log N instead of log C
                        because only potions from the set_total_potion_data method can be added into the avl tree and the worst case is when all
                        potion in potion_data has positive quantity.

        """
        self.length_potion_with_quantity = len(potion_name_amount_pairs)
        self.tree = AVLTree()

        for i in range(len(potion_name_amount_pairs)):
            self.hashtable[potion_name_amount_pairs[i][0]].quantity = potion_name_amount_pairs[i][1] #Update quantity of potions in inventory
        
            self.tree[self.hashtable[potion_name_amount_pairs[i][0]].buy_price] = self.hashtable[potion_name_amount_pairs[i][0]]# insert potions with stock into an avl tree
            
       
        
 



    def choose_potions_for_vendors(self, num_vendors: int) -> list:

        """
        This method lets the vendor selects the pth expensive potion in the inventory where p is a random number between 1 and total number
        of potions in stock. Then the name and quantity of the potion chosen will be added to lst. The potion is then deleted from the avl tree
        so that the other vendors cannot select it. After the whole process, the potions are added back using temp. 

        Time complexity: O(C * log(N)) Where C is equal to num_vendors, and N is the number of potions provided in set_total_potion_data. 
                         The first for loop will run C times and the log N comes from calling the kth largest method and 
                         getting the pth_expensive node from the tree. So it is 2log(N) but we drop the constant when considering big O.
                         The second for loop will run C times also but is not considered in Big O because C*log(N) dominates.
    
        """
        if num_vendors > self.length_potion_with_quantity or num_vendors < 1: # Only potions in stock(quantity > 0) is available in inventory
            raise ValueError("num_vendors is invalid")
            
        lst = []
        temp = [] #to hold potions that will be deleted and add them back after the process is finished
        for i in range (num_vendors):
            randnum = self.rand.randint(self.length_potion_with_quantity - i) # c-i
            pth_expensive = self.tree.kth_largest(randnum).key #gets the key of the pth largest node
            temp += [(pth_expensive,self.tree[pth_expensive])] 
            lst += [(self.tree[pth_expensive].name, self.tree[pth_expensive].quantity)] #store the name and quantity of selected potions
            del(self.tree[pth_expensive])
           
        for i in range (len(temp)): #add back after delete
            self.tree[temp[i][0]] = temp[i][1]
        return lst



    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[int]) -> list[float]:

        """
        A method to solve the game, more explanation are given below this method

        Time complexity: O(N * log(N) + M * N) where N is the length of potion_valuations, 
                         and M is the length of starting_money.
        """
        times = [] # a part of the key for the avl tree
        final_ans = [] # the final output of max money of each attempt
        self.tree_solvegame = AVLTree()
        for i in range (len(potion_valuations)):
            times += [potion_valuations[i][1] / self.hashtable[potion_valuations[i][0]].buy_price] # how many times more the adventure is willing to pay
            if times[i] > 1: # Greater than 1 so that any potions that do not make profit wont be considered
                self.tree_solvegame[str(times[i]) + self.hashtable[potion_valuations[i][0]].name] = (self.hashtable[potion_valuations[i][0]], potion_valuations[i][1])
                # for the above line, the key and data is explained below
        for i in range (len(starting_money)):
            sum = 0 # reset the sum for each attempt
            for j in range(len(self.tree_solvegame)): # all are explained below
                buy_potion_litre = min(starting_money[i]/self.tree_solvegame.kth_largest(j+1).item[0].buy_price, self.tree_solvegame.kth_largest(j+1).item[0].quantity)
                starting_money[i] -= buy_potion_litre * self.tree_solvegame.kth_largest(j+1).item[0].buy_price # due to the above line, starting_money will never go below 0
                sum += (buy_potion_litre * self.tree_solvegame.kth_largest(j+1).item[1]) # adds the sum of money earned for 1 attempt
                
            final_ans.append(sum) # append the sum of money earned for each attempt
        return final_ans


"""
Selection of ADT
For the methods in Game class, I used 2 ADTs, which is hash table and avl tree.
For the first method, set_total_potion_data, I used a hash table to store the potion objects. This is because we can use the potion name 
that is in the list potion_data as the key to store the potion objects. The time complexity of setting and getting an item using hash table
is O(1), so storing, searching, getting the potion objects in a hash table is very fast compared to using an array. if we use an array to store the objects, 
the worst case will be O(n) where n is the length of potion_data.

For the methods add_potions_to_inventory and solve_game, I used 2 seperate avl trees. The choose_potions_for_vendors uses the same avl tree with
the add_potions_to_inventory method.
The first method uses the buy price of potions as the key whereas the second method uses the times as the key. 
The main reason to use avl trees is because it can sort the items based on the keys and the time complexity of inserting is always log(n)
where n is the total number of nodes in the tree. Furthermore, the key is flexible, as it can be an integer or string. 

The Hash table will contain all possible potions that exist in this game,
the first avl tree will contain all potions from the hash table that has quantity > 0 and sorted according to potion buy_price,
the solve game avl tree contains potion from potion_valuations and it is sorted according to times.
"""

"""
Explanation for solve_game (based on the full_vendor_info data in the specification)

My approach is to first sort the potions according to the potion that makes the most profit.
The most profit means that how many times more is the adventure willing to pay compared to the the vendor's but price.
For example, “Potion of Instant Health” buy price from vendor is $5 where adventure is willing to buy for $15, so 
this means the adventure is willing to pay 3 times more for this potion.

I will create a new AVLTree(), self.tree_solvegame to store the potions according to the key explained above. However, I will not
consider any potion that does not make any profit, so I will only store potions that has profit > 1 times into this AVL tree.
Furthermore, I will use the key as a string of "Potion name" + "times", this is to avoid cases where 2 potions have the same times.
The data in the tree will be a tuple (Potion(), the price adventure willing to pay)

Next approach is to use the starting money to buy all possible litres of the potion that has most times. Then if there are still money,
I will buy all possible litres of the potion that has second most times. I will use kth largest() to do this.

How to decide how many litres to buy
For this part, I will find the minimum of the 2 condition below,
1. how many possible litres I could buy with current money 
2. the available litres the vendor has

Example, when starting money = 80
The first potion I would try to buy is “Potion of Instant Health” because it is the most times (x3).
1. 80 / 5 = 16 litres (I can buy 16 litres with all money)
2. The vendor only has 3 litres
So the min(1,2) is 3 litres.

After buying 3 litres
starting money = 80 - (5*3) = 65
The next potion I will buy is “Potion of Health Regeneration” because it is second most times (x1.5),
althought the “Potion of Extreme Speed” is also (x1.5) but according to my key, kth largest will find the above potion first 
simply because the length of string is longer.
1. 65 / 20 = 3.25 litres
2. The vendor has 4 litres
So the min(1,2) is 3.25 litres

starting money = 65 - (20*3.25) = 0
so min(0,2) will always be zero as vendors can only sell potions with +ve quantity(litres).

For the sum of final money a player has, simply use (buy_potion_litre * the price the adventure is willing to pay).
the final_ans returns a list containing the sum of final money for every attempt.







"""
          
        



