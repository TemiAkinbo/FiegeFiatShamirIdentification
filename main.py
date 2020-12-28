'''
Created on Dec 18, 2014

@author: marcel
'''
from prover import ffs_prover
from verifier import ffs_verifier
from trusted_centre import ffs_trusted_center

mode=input("Enter the mode to run in: ")
if mode != "trusted_center":
    k=int(input("Enter the key size: "))
if mode == "verifier":    
    t=int(input("Enter the number of rounds: "))


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
# elif mode=='cheater':
#     cheater=dishonest_ffs_prover()
#     cheater.run(42424)
else:
    print ("Wrong argument")
