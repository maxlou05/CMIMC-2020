import numpy as np
import math
import sys

TASK_NUM = 6
M = 200
N = 8

# Sieve of Eratosthenes - not mine
def generate_primes(n):
    is_prime = np.ones(n+1,dtype=bool)
    is_prime[0:2] = False
    for i in range(int(n**0.5)+1):
        if is_prime[i]:
            is_prime[i*2::i]=False
    return np.where(is_prime)[0]

# This simple program just fills the lists with unique primes and a 1
# This is guaranteed to satisfy the requirements, but it is not the best answer, of course
primes = generate_primes(M)
length = math.floor(len(primes)/N)

out = open('answer{}.txt'.format(TASK_NUM), 'w')
for i in range(N):
    n = primes[length*i:length*(i+1)]
    n = np.append(n, 1)
    for t in range(len(n)):
        out.write(str(n[t]) + " ")
    out.write("\n")
    print(len(n))

out.close()
