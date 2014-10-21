__author__ = 'Jose'

import numpy as np
import random
import math
from confident.estimator import *

def synthetic_data(students, decay, learning_rate, timesteps, a, b):
    k0 = np.random.beta(a, b, students)
    ids = range(0, students)

    p_k0 = zip(ids, k0)
    ans = TimePoints([])
    for t in range(0, timesteps):
        p_kt = [ (id, sigmoid(learning_rate, t, k_t))  for (id, k_t) in p_k0]

        ans.append( [Observation(id, np.random.binomial(1, k_t, 1)[0]) for id, k_t in p_kt] )

        new_size = int(decay * len(p_k0))
        p_k0 = random.sample(p_k0, new_size)

    return ans

def main(students = 200, decay=0.8, learning_rate=1.2, timesteps=2, a=10, b=5):
    random.seed(0)
    np.random.seed(0)
    a = synthetic_data(students, decay, learning_rate, timesteps, a, b)


    #a = TimePoints([ [  Observation("a", 1), Observation("b", 0), Observation("c", 0), Observation("d", 0)],
    #                 [  Observation("a", 1), Observation("b", 1), Observation("c", 0), Observation("d", 0)] ])
    print "Independent:", a.independent_sample_variance_estimator()
    print "Dependent:", a.foo(True)



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