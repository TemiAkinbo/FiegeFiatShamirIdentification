from prover import ffs_prover
from verifier import ffs_verifier
from trusted_centre import ffs_trusted_center
import sys

def lightmode(mode,k,t,final_run):
    if mode=='trusted_center':
        t_center = ffs_trusted_center()
        t_center.listen(42423)
    if mode=='prover':
        prover=ffs_prover(k)
        prover.getModulus(42423)
        prover.genKeys()
        prover.run(42424)
    elif mode=='verifier':
        verifier=ffs_verifier(k,t)
        verifier.getModulus(42423)
        verifier.listen(42424)
        if final_run == 'True':          
            verifier.stopTC(42423)
    else:
        print ("Wrong argument")

# def largetest(t):



if len(sys.argv) >= 3:
    testmode = sys.argv[1]
    if testmode == "light":
        mode = sys.argv[2]
        k = int(sys.argv[3])
        t = int(sys.argv[4])
        final_run = sys.argv[5]
        lightmode(mode,k,t, final_run)
    else:
        t = int(sys.argv[2]) 
else:
    mode=input("Enter the mode to run in: ")
    if mode != "trusted_center":
        k=int(input("Enter the key size: "))
    if mode == "verifier":    
        t=int(input("Enter the number of rounds: "))
    final_run = 'True'
    lightmode(mode,k,t, final_run)
