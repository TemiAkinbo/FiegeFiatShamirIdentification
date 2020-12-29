from Crypto.Util.number import isPrime, GCD
import pickle
import sys
import random
import socket
import time

class ffs_trusted_center:
    def __init__(self):
        self.n = None
        self.primeList = None


    def listen(self, port): 
        self.sersock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sersock.bind(('127.0.0.1',port))
        self.sersock.listen()
        self.genPrime()

        while True:
            conn = self.sersock.accept()[0].makefile(mode='rw')
            data = conn.readline()
            if data == "GET N\n":
                print("received request")
                conn.write("SENDING N\n")
                conn.flush()
                conn.write(str(self.n) + "\n")
                debug = "sent random prime n: " + str(self.n)
                print(debug)
                conn.flush()
                conn.close()
            elif data == "STOP\n":
                conn.close
                break          


    def genPrime(self):
        p = self.getPrime()
        q = self.getPrime()

        # ensure that p != q, which is true in most cases
        while p == q:
            q = self.getPrime()
        
        self.n = p*q
    
    """Generate Blum integer primes that are 128 bits"""
    def getPrime(self):
        while True:
            p = random.getrandbits(128)
            if isPrime(p) and p%4 == 3:
                break
        return p