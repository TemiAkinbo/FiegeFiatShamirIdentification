'''
Created on Dec 18, 2014

@author: marcel
'''
import random

def coin_flip():
    if random.randint(0,1) == 1:
        return 1
    else:
        return -1

#Returns m^2 mod n
def square_ZnZ(m,n):
    return (m*m)%n