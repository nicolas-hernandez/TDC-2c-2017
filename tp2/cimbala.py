import numpy as np
import scipy.stats as stats

def detectOutliers(jumps):
    outliers = cimbala(jumps)

    print("jumps (rtt diffs): " + str(jumps))
    print("outliers by jumps: " + str(outliers))
    
    return outliers

def cimbala(rttDifs):
    outliers = []
    if len(rttDifs) > 0:
        keepLooking = True
        while keepLooking:
            keepLooking = False
            mean = np.mean(rttDifs)
            standardDeviation = np.std(rttDifs)
            tg = thompsonGamma(rttDifs)
            outlier = None
            for rttDif in rttDifs:
                delta = np.absolute(rttDif - mean)
                #print("delta: " + str(delta) + " t*S: " + str(tg * standardDeviation))
                if (delta > tg * standardDeviation):
                    outlier = rttDif
                    break
            if outlier:
                rttDifs.remove(outlier)
                outliers.append(outlier)
                keepLooking = True

    return outliers


def thompsonGamma(rtts):
    n = len(rtts)
    t_a_2 = stats.t.ppf(1 - 0.025, n - 2)
    sqRootN = np.sqrt(n)
    numerator = t_a_2 * (n - 1)
    denominator = sqRootN * np.sqrt(n - 2 + np.power(t_a_2, 2))
    return numerator / denominator
