import subprocess
import sys

if len(sys.argv) < 3:
    exit()
else:
    n_runs = int(sys.argv[1])
    key_size = sys.argv[2]
    n_challenges = sys.argv[3]

tc_output = subprocess.Popen('python main.py light trusted_center ' + key_size + ' ' + n_challenges + ' False', shell=True)

for i in range(n_runs):
    print("Run" + str(i))
    if i == n_runs - 1 or n_runs == 1:
        v_output = subprocess.Popen('python main.py light verifier ' + key_size + ' ' + n_challenges + ' True', shell=True)
        p_output = subprocess.Popen('python main.py light prover ' + key_size + ' ' + n_challenges + ' False', shell=True)
        v_output.wait()
        p_output.wait()
    else:
        v_output = subprocess.Popen('python main.py light verifier ' + key_size + ' ' + n_challenges + ' False', shell=True)
        p_output = subprocess.Popen('python main.py light prover ' + key_size + ' ' + n_challenges + ' False', shell=True)
        v_output.wait()
        p_output.wait()
     


