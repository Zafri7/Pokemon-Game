"""
Authors: 	1) Tuan Muhammad Zafri
 		    2) Wang Qian
 		    3) Mohammed Salman Ulumuddin
		    4) Ally Teh Tze-Rou  
Last modified by: Tuan Muhammad Zafri on 29/05/2022 
"""

from typing import Generator

def lcg(modulus: int, a: int, c: int, seed: int) -> Generator[int, None, None]:
    """
    Linear congruential generator.
    
    Time complexity: O(1) due to fixed input from the parameter and there will be no repeated loop
                     as the while loop will never return False. 
                     The time it takes does not increase as you have more random numbers.
    """
    while True:
        seed = (a * seed + c) % modulus
        yield seed



class RandomGen:
    """A class for random number generation"""
    # class variable
    record = 0    #record is initialise to 0
    
    def __init__(self, seed: int=0) -> None:
        """
        A method is to initialise seed with the value from the parameter
        
        Time complexity: O(1) because it only initialise seed with the value from the parameter
        """
        self.seed = seed
        


    def randint(self, k: int) -> int:
        """
        A method to generate a random number from 1 to k inclusive with the following approach
        First, generate 5 random numbers using the lcg method above, dropping the 16 least
        significant bits of each number. It will generate a new number, 
        which is 16 bits long and has a 1 in each bit if at least 3 of the 5 generated numbers have a 1 in this bit.
        Return the new number, modulo k, plus 1

        Time complexity: O(1) since initialising the variables and looping in the range of a fixed variable are O(1).
                         The second and third for-loop is also looping in the range of 6 and 16, which is a fixed input.
                         Therefore the time complexity is O(1) 
        """
        arr=[]
        new_num_arr = [0] * 16
        new_num = '0b'
        power = pow(2,16) 
        Random_gen = lcg(pow(2,32), 134775813, 1, self.seed) 
        for _ in range(self.record): #keep track of next() so it wont restart when randint is called everytime
            next(Random_gen)
        for i in range (6):
            arr += [format(next(Random_gen)//power, "016b")] # remove 16 least significant bits
        for i in range(16):
            a=arr[0][i]
            b=arr[1][i]
            c=arr[2][i]
            d=arr[3][i]
            e=arr[4][i]
            if eval(a + '+' + b + '+' + c + '+' + d + '+' + e) >= 3: # check if there are at least 3 numbers that have 1 bit
                new_num_arr[i] = 1
            new_num += str(new_num_arr[i])
        self.record += 5
        return int(eval(new_num)) % k + 1
 
           
        
       

                


       

       


     
        

if __name__ == "__main__":
    Random_gen = lcg(pow(2,32), 134775813, 1, 0)

