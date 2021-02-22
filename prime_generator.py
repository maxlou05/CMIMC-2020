import numpy as np
import math
import sys

TASK_NUM = 6

def generate_primes(n):
    is_prime = np.ones(n+1,dtype=bool)
    is_prime[0:2] = False
    for i in range(int(n**0.5)+1):
        if is_prime[i]:
            is_prime[i*2::i]=False
    return np.where(is_prime)[0]

primes = generate_primes(200)
length = math.floor(len(primes)/8)

out = open('answer{}.txt'.format(TASK_NUM), 'w')
for i in range(8):
    n = primes[length*i:length*(i+1)]
    n = np.append(n, 1)
    for t in range(len(n)):
        out.write(str(n[t]) + " ")
    out.write("\n")
    print(len(n))

out.close()