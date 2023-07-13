"""
Authors: 	1) Tuan Muhammad Zafri
 		    2) Wang Qian
 		    3) Mohammed Salman Ulumuddin
		    4) Ally Teh Tze-Rou  
Last modified by: Tuan Muhammad Zafri on 29/05/2022 
"""

from math import isqrt



def largest_prime(k: int) -> int:
    """
    Returns the largest prime number strictly less than k. 
    The point of this mehtod is to mark the multiples of the numbers from 2 to isqrt(k) to False, The numbers that are left True will
    mean that they only have 2 factors, which is 1 and itself. 

    Time complexity: O(n*log(log n)) 
                     The number of times the loop runs is n*(1/2 + 1/3 + 1/5 +.....p) where p is prime
                     The prove of harmonic progression of summation prime using Euler's product formula is equals to log(log n)
                     So substituting it into the equation, we get n log(log n). 
                     
                     We refered to the link in the assignment specification for the pseudocode and time complexity.
                     To be honest, we are not 100 clear of the mathematical operations behind this algorithm
                     but we know how the code works. It is explained in the inline comments.

    """
    if k <= 2:      
        return []   

    arr_prime = [True]*k    # a list that contains k numbers of True
    arr_prime[0] = False    # Although k is bigger than 2 but just to set that 0 and 1 are not prime numbers
    arr_prime[1] = False
    for i in range (2,isqrt(k)+1):  # composite numbers will contain at least 1 factor that is less than its square root
        if arr_prime[i]:            # if condition to check arr_prime[i] equals to True

            for j in range (i**2, k, i):  # starts i^2 because the numbers before it should be marked as False already, jumps i to check all multiples of i
                arr_prime[j] = False      #mark all multiples of i to False

    return max([i for i in range(k) if arr_prime[i]])     # returns the largest number value of i if arr_prime[i] is True



