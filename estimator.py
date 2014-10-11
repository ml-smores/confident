__author__ = 'Jose'

import numpy as np
from collections import Counter
import operator

class Observation:
    def __init__(self, id, value):
        self.id = id
        self.value  = value

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.value)

class VarianceEstimator:
    @staticmethod
    def bernoulli(l, type="mle"):
        cnt = Counter(l)
        if   len(cnt.keys()) > 2:
            raise RuntimeError("List includes observations that are not sampled from a binomial " + str(cnt))

        ps = [ count / float(len(l)) for (item, count) in cnt.items() ]
        ps.append(1)

        n = len(l)
        if type == "unbiased":
            z = n / (n -1.0)
        elif type == "mle":
            z = 1.0 / n
        else:
            raise RuntimeError("Unknown estimator type" + type)

        return  apply(operator.mul, ps) * z

    @staticmethod
    def sample_variance(l, ddof=0):
        return np.var(l, ddof=ddof)





class TimePoints(list): #list of list of observations
    def calc(self, foo):  # list of observations
        return [foo( [o.value for o in timepoint ] ) for timepoint in self]


    def independent_sample_variance(self):
        return self.calc(VarianceEstimator.sample_variance)

    def independent_bernoulli_variance(self):
        return self.calc(VarianceEstimator.bernoulli)

    def covariance(self):
        for idx1, timepoint1 in enumerate(self):
            for idx2, timepoint2 in enumerate(self):
                tp1, tp2 = TimePoints.intersection(timepoint1, timepoint2)


    @staticmethod
    def intersection(timepoint1, timepoint2):
        ids1 = [o.id for o in timepoint1]
        ids2 = [o.id for o in timepoint2]
        common_ids = set(ids1).intersection(set(ids2))
        iscommon = lambda x : x.id in common_ids
        ctp1 =  filter(iscommon, timepoint1)
        ctp2 = filter(iscommon, timepoint2)
        return ctp1, ctp2



def main():
    a = TimePoints([ [  Observation(1, 1)] ])
    print a.independent_sample_variance()
    print a.independent_bernoulli_variance()
    #Estimator.covariance([], [])



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