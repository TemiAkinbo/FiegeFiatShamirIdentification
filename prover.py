import random
import socket
import pickle
from Crypto.Util.number import GCD, inverse
from mod_operations import coin_flip
import time

def str_to_bool(string):
    if string=='True':
        return True
    elif string=='False':
        return False
    else:
        return None

class ffs_prover:   
    #Initialize the prover's key
    #n: Agreed upon large integer
    #k: key size
    #t: number of challenges --> Should be specified by the verifier...
    def __init__(self, k):
        self.n= None
        self.t= None
        self.k = k
        self.s=[None]*k
        self.p=[None]*k
    
    def genKeys(self):
        start = time.time()
        for i in range(0,self.k):
            while True:
                self.s[i] = random.randint(0,self.n-1)
                #ensure that secret keys are coprime with n
                if GCD(self.s[i], self.n) == 1:
                    break
            
            self.p[i]= inverse(pow(self.s[i],2,self.n),self.n)
            self.p[i]=self.p[i] % self.n
        end = time.time()
        self.keygenTime = end - start
        print("Prover initialized...")
        print("\tPrivate key: "+",".join(map(str,self.s)))
        print("\tPublic key: "+",".join(map(str,self.p)))
        print(f"Time taken to generate keys {self.keygenTime}")


    def getModulus(self, port):
        mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        mysocket.connect(('127.0.0.1',port))
        sock= mysocket.makefile(mode='rw')
        sock.write("GET N\n")
        sock.flush()
        response = sock.readline()
        if response == "SENDING N\n" :
            self.n = int(sock.readline())
        sock.close()
        print("n received: " + str(self.n))
    
    #open a socket to the verifier
    def register_verifier(self,ip,port):
        mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        mysocket.connect((ip,port))
        return mysocket.makefile(mode='rw')
    
    #Sends the public key to the verifier --> should use TLS?
    def advertise_key(self,mysocket):
        mysocket.write("PKA\n")
        mysocket.flush()
        response=mysocket.readline()
        if response == "OK PKA\n":
            for value in self.p:
                mysocket.write(str(value)+" ")
            mysocket.write("\n")
            mysocket.flush()
        else:
            mysocket.write("DIE\n")
            mysocket.flush()
            print("Protocol failure during key advertisment")
            exit()
    
    def start_auth(self,mysocket):
        mysocket.write("START\n")
        mysocket.flush()
        response=mysocket.readline()
        if response.split()[0:2] == ["OK","START"]:  #TODO: match pattern "OK START [0-9]+\n"
            self.t = int(response.split()[2])
            print("Verifier asked for "+str(self.t)+" challenges")           
    
    #Commit to R as described in Feige-Fiat-Shamir        
    def initiate_challenge(self,mysocket):
        mysocket.write("COMMIT\n")
        mysocket.flush()
        response=mysocket.readline()
        r=0
        b=[]
        if response == "OK COMMIT\n":
            r=random.randint(0,self.n-1)
            mysocket.write(str((coin_flip()*pow(r, 2, self.n)) %self.n) + " ")
            mysocket.write("\n")
            mysocket.flush()
            b=list(map(str_to_bool,mysocket.readline().split()))
            return r,b
        else:
            mysocket.write("DIE\n")
            mysocket.flush()
            print("Protocol failure during challenge initiation")
            exit()
    
    #Computes and sends the response from the challenge    
    def challenge_response(self,r,b,mysocket):
        y=r
        for i in range(0,self.k):
            if b[i]:
                y *= self.s[i]
        mysocket.write(str(y%self.n)+"\n")
        mysocket.flush()
        
    def run(self,port):
        start = time.time()
        verifiersocket=self.register_verifier("localhost",port)
        self.advertise_key(verifiersocket)
        self.start_auth(verifiersocket)
        for i in range(0,self.t):
            r,b = self.initiate_challenge(verifiersocket)
            self.challenge_response(r, b, verifiersocket)
        end = time.time()
        proverRuntime = end - start
        print(f"prover protocol runtime: {proverRuntime}")
        print(f"total runtime: {self.keygenTime + proverRuntime}")
        verifiersocket.write("DIE\n")
        verifiersocket.flush()
