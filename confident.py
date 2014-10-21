__author__ = 'Jose'

import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm
import collections
import itertools
import operator
import pymc as pm
import matplotlib.pylab as pl
'''
Requires pandas and statsmodels

To install:

pip isntall pandas
pip install git+https://github.com/pymc-devs/pymc
'''

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

    binary_observations = sm.families.Binomial()

    def independent_sample_variance_estimator(self):
        '''
        Calculates the variance of a learning curve assuming every point is independent
        :return: variance estimator
        '''
        return  [np.var( TimePoints.get_values(timepoint) ) for timepoint in self]

    def pooled_sample_variance_estimator(self):
        #TODO: implement
        pass

    @staticmethod
    def invlogit(x):
         import theano.tensor as t
         return t.exp(x) / (1 + t.exp(x))
    def foo(self, discrete):
        student_ids  = []
        timestep_ids = []
        y = []

        ids = collections.defaultdict(itertools.count().next)
        for t in range(0, len(self)):
            student_ids  +=  [ids[o.id] for o in self[t]]
            timestep_ids +=  [t         for o in self[t]]
            y            +=  [o.value   for o in self[t]]

        n_students  =  len(set(student_ids))
        n_timesteps = len(self)

        print student_ids, "!", n_students

        with pm.Model() as hierarchical_model:
            # Hyperpriors for group nodes
            mu_student = pm.Normal('mu_student', mu=0., sd=100**2)
            sigma_student = pm.Uniform('sigma_student', lower=0, upper=100)

            #mu_timestep = pm.Normal('mu_beta', mu=0., sd=100**2)
            #sigma_timestep = pm.Uniform('sigma_beta', lower=0, upper=100)

            student  = pm.Normal('student', mu=mu_student, sd=sigma_student, shape=n_students) #random effect
            timestep = pm.Normal('timestep', mu=0, sd=100**2, shape=n_timesteps)  #fixed effect

            # Model error
            eps = pm.Uniform('eps', lower=0, upper=100)


            theta = student[student_ids] + timestep[timestep_ids]

            # Data likelihood
            if discrete:
                ll = pm.Bernoulli('theta', p=self.invlogit(theta), observed=y)
            else:
                ll = pm.Normal('theta', mu=theta, sd=eps, observed=y)

        with hierarchical_model:
            print "Find MAP..."
            start = pm.find_MAP()
            #if discrete:
            #     step = pm.BinaryMetropolis(scaling=start)
            # else:
            print "NUTS..."
            step = pm.NUTS(scaling=start)
            print "Samples..."
            hierarchical_trace = pm.sample(2000, step, start=start, progressbar=False)
        print "done..."
        print "Plot..."

        pl.figure(figsize=(10,10))
        f = pm.traceplot(hierarchical_trace[500:])
        f.savefig("a.png")
        return hierarchical_trace



    @staticmethod
    def decorrelate(df, family = binary_observations):
        results = sm.glm('output ~ id + C(timestep) - 1', family=family, data=df).fit()

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

            ind_var = np.var(TimePoints.get_values(self[t]))
            bias = 0
            print ">", cov_matrix
            if np.size(cov_matrix) > 1:
                for i in range(0, len(values)-1):
                    bias += cov_matrix[i][len(values)-1] #TODO: multiply by two?

            var = ind_var + bias  # independent variance + bias

            variance_timesteps.append(var)
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
    a = TimePoints([ [  Observation("a", 1), Observation("b", 0), Observation("c", 0), Observation("d", 0)],
                     [  Observation("a", 1), Observation("b", 1), Observation("c", 0), Observation("d", 0)] ])
    print "Independent:", a.independent_sample_variance_estimator()
    print "Dependent:", a.foo(True)



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