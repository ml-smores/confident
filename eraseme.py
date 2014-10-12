__author__ = 'Jose'

import numpy as np
from collections import Counter
import operator

class Observation:
    def __init__(self, id, value):
        '''

        :param id: The id of the subject (student)
        :param value: The value of the observation
        :return:
        '''
        self.id = id
        self.value  = value

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.value)



class TimePoints(list): #list of list of observations



    def independent_sample_variance_estimator(self):
        '''
        Calculates the variance of a learning curve assuming every point is independent
        :return: variance estimator
        '''
        return  [np.var( TimePoints.get_values(timepoint) ) for timepoint in self]

    def correlated_variance_estimator(self, previous=1):
        '''
        Calculates the variance of a learning curve assuming dependence of previous timesteps
        :return: variance estimator
        '''
        variance_timesteps = []
        for t in range(0, len(self)):
            ids = set( [o.id for o in self[t]] )
            values = self.common_values_for_id(ids)

            if previous != None:
                values = values[max(t-previous, 0): t+1] #TODO: How would it look like this?

            cov_matrix = np.cov(values, bias=1)
            C = np.sum(cov_matrix) / len(values)
            #print cov_matrix
            variance_timesteps.append( C)
        return variance_timesteps
            #print sum(cov_matrix)

    def common_values_for_id(self, ids):
        '''
        Returns the values of the observations that appear in id
        :param ids: The ids that are selected
        :return:
        '''

        answer = []
        for timepoint in self:
            selected  = [o.value for o in timepoint if o.id in ids]
            answer.append(selected)

        return answer

    @staticmethod
    def get_values(timepoint):
        return [o.value for o in  timepoint]


def main():
    a = TimePoints([ [  Observation(1, 1), Observation(2, 0), Observation(3, 0), Observation(4, 0)],
                     [  Observation(1, 1), Observation(2, 1), Observation(3, 0), Observation(4, 0)] ])
    print "Independent:", a.independent_sample_variance_estimator()
    print "Dependent:", a.correlated_variance_estimator()



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