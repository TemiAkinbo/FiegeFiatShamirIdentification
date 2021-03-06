import socket
import random
from mod_operations import square_ZnZ
import time

class ffs_verifier:
    def __init__(self,k,t):
        self.n= 0
        self.k=k
        self.t=t
        self.started=False
    
    def getModulus(self, port):
        mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        mysocket.connect(('localhost',port))
        sock= mysocket.makefile(mode='rw')
        sock.write("GET N\n")
        sock.flush()
        response = sock.readline()
        if response == "SENDING N\n" :
            self.n = int(sock.readline())
        sock.close
        print("n received: " + str(self.n))

    def stopTC(self, port):
        mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        mysocket.connect(('localhost',port))
        sock= mysocket.makefile(mode='rw')
        sock.write("STOP\n")
        sock.flush()
        sock.close



    def listen(self,port):
        self.sersock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sersock.bind(('127.0.0.1',port))
        self.sersock.listen(1)
        conn = self.sersock.accept()[0].makefile(mode='rw')
        
        start = time.time()
        while True:
            data=conn.readline()
            if data=="PKA\n":
                conn.write("OK PKA\n")
                conn.flush()
                self.handle_advertisment(conn)
            elif data=="START\n":
                conn.write("OK START "+str(self.t)+"\n")
                conn.flush()
                self.started=True
            elif data=="COMMIT\n":
                if (self.pub_key is None) or not (self.started):
                    conn.write("No public key registered for this connection\n")
                    conn.flush()
                    print("No pub key...")
                else:
                    conn.write("OK COMMIT\n")
                    conn.flush()
                    self.handle_challenge(conn)
            elif data=="DIE\n":
                conn.close()
                break
        
        end = time.time()
        print(f"verifier runtime: {end - start}")
        
    def handle_advertisment(self,sock):
        pub_key_as_string=sock.readline()
        print("Received public key: "+pub_key_as_string)
        self.pub_key = list(map(int,pub_key_as_string.split()))
        
    def handle_challenge(self,sock):
        x=int(sock.readline())
        print("Prover commited to: "+str(x))
        b=[None]*self.k
        for i in range(0,self.k):
            b[i] = (random.randint(0,1)==1)
            sock.write(str(b[i])+" ")
        sock.write("\n")
        sock.flush()
        y=int(sock.readline())
        expected_x=pow(y,2,self.n)
        for i in range(0,self.k):
            if b[i]:
                expected_x = expected_x * self.pub_key[i]
        expected_x = expected_x%self.n
        if (expected_x==x) or (expected_x==(-x%self.n)):
            print("Challenge correctly completed!\n")
        else:
            print("Failure in challenge")
        