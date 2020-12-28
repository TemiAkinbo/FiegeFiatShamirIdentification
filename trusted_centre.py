"""large random prime number generator"""
from Crypto.Util.number import isPrime, GCD
import pickle
import sys
import random
import socket
import threading

class ffs_trusted_center:
    def __init__(self):
        self.n = None
        self.primeList = None

    def on_new_client(self,sock):
        conn = sock.accept()[0].makefile(mode='rw')
        data = conn.readline()
        if data == "GET N\n":
            print("received request")
            conn.write("SENDING N\n")
            conn.flush()
            conn.write(str(self.n) + "\n")
            print("sent random prime n: " + str(self.n))
            conn.flush()




    def listen(self, port): 
        self.sersock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sersock.bind(('127.0.0.1',port))
        self.sersock.listen()
        self.genPrime()

        while True:
            self.on_new_client(self.sersock)

        self.sersock.close()
                        
            


    def genPrime(self):
        while True:
            n = random.randint(3000, 10000)
            if isPrime(n):
                self.n = n
                break
    

