__author__ = 'Jose'

import numpy as np
import random
import math

def main(students_k0 = 10, decay=0.8, learning_rate=1.2, timesteps=2, a=10, b=5):
    random.seed(0)
    np.random.seed(0)

    k0 = np.random.beta(a, b, students_k0)
    ids = range(0, students_k0)
    students_k0 = zip(ids, k0)
    for t in range(0, timesteps):
        students_kt = [ (id, sigmoid(learning_rate,t, k_0))    for (id, k_0) in students_k0]
        for id, k_t in students_kt:
            print t, id, np.random.binomial(1, k_t, 1)[0]
        new_size = int(decay * len(students_k0))
        print new_size
        students_k0 = random.sample(students_k0, new_size)

def sigmoid(beta, x, dummy):
  return 1 / (1 + math.exp(- beta * x + dummy))

if __name__ == "__main__":
    import sys

    args = sys.argv
    print args
    cl = {}
    for i in range(1, len(args)):  # index 0 is the filename
        pair = args[i].split('=')
        if pair[1].isdigit():
            cl[pair[0]] = int(pair[1])
        elif pair[1].lower() in ("true", "false"):
            cl[pair[0]] = (pair[1].lower() == 'true')
        else:
            cl[pair[0]] = pair[1]

    main(**cl)