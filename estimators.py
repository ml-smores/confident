__author__ = 'Jose'
class VarianceEstimator:
    @staticmethod
    def bernoulli(l):
        cnt = Counter(l)
        if len(cnt.keys()) > 2:
            raise RuntimeError("List includes observations that are not sampled from a binomial " + str(cnt))

        n = float(len(l))
        return reduce(operator.mul, [float(c) / n for c in cnt.values()])  if len(cnt.keys()) == 2 else 0




    @staticmethod
    def sample_variance(l, ddof=0):
        return np.var(l, ddof=ddof)

class CovarianceEstimator:
    @staticmethod
    def bernoulli(ls, positive = 1, bias = 0):
        cnt = Counter()
        n = float('nan')
        for l in ls:
            cnt.update(l)
            if not np.isnan(n):
                if len(l) != n:
                    raise RuntimeError("Al lists should be the same length, there is no imputation implemented: " + str(n) + " " + str(len(l)))
            n = len(l)

        if len(cnt.keys()) > 2:
            raise RuntimeError("List includes observations that are not sampled from a binomial " + str(cnt))

        covar = np.zeros((len(ls),len(ls)))
        for  i, l1 in enumerate(ls):
            for j, l2 in enumerate(ls):
                c1 = Counter(l1)
                c2 = Counter(l2)

                e_x =  float(c1[positive]) / n
                e_y =  float(c2[positive]) / n

                covar[i, j] = 0
                for obs in range(0, n):
                    x = l1[obs]
                    y = l2[obs]
                    covar[i, j] += (x - e_x) * (y - e_y)

                if len(cnt.keys()) != 2:
                    covar[i, j] = 0

        return covar / (n -1 + bias)



