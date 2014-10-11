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



class TimePoints(list): #list of list of observations

    @staticmethod
    def get_values(timepoint):
        return [o.value for o in  timepoint]

    def independent_sample_variance_estimator(self):
        return  [np.var( TimePoints.get_values(timepoint) ) for timepoint in self]

    def correlated_variance_estimator(self):
        variance_timesteps = []
        for t in range(0, len(self)):
            values = self.common_values(t)
            values = values[min(t-1, 0): t] # is this necessary?
            cov_matrix = np.cov(values, bias=1)

            C = np.sum(cov_matrix)
            variance_timesteps.append( C)
        return variance_timesteps
            #print sum(cov_matrix)

    def common_values(self, timestep):
        '''
        Returns a subset of the list only containing students that appear at timestep
        :param timestep: The timestep to get common values from
        :return:
        '''
        ids = set( [o.id for o in self[timestep]]  )

        answer = []
        for t in range(0, len(self)):
            timepoint = self[t]
            selected  = [o.value for o in timepoint if o.id in ids]

            answer.append(selected)
        return answer




def main():
    a = TimePoints([ [  Observation(1, 1), Observation(2, 0), Observation(3, 0), Observation(4, 0)],
                     [  Observation(1, 1), Observation(2, 1), Observation(3, 1), Observation(4, 1)] ])
    print a.independent_sample_variance_estimator()
    print a.correlated_variance_estimator()



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