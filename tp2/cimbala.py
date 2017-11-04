import numpy as np
import scipy.stats as stats

def detectarOutliers(jumps):
    outliers = cimbala(jumps)

    print("jumps (rtt diffs): " + str(jumps))
    print("outliers by jumps: " + str(outliers))
    
    return outliers

def cimbala(rttDifs):
    outliers = []
    if len(rttDifs) > 0:
        seguirBuscando = True
        while seguirBuscando:
            seguirBuscando = False
            media = np.mean(rttDifs)
            desvioStandard = np.std(rttDifs)
            tg = thompsonGamma(rttDifs)
            outlier = None
            for rttDif in rttDifs:
                delta = np.absolute(rttDif - media)
                #print("delta: " + str(delta) + " t*S: " + str(tg * desvioStandard))
                if (delta > tg * desvioStandard):
                    outlier = rttDif
                    break
            if outlier:
                rttDifs.remove(outlier)
                outliers.append(outlier)
                seguirBuscando = True

    return outliers


def thompsonGamma(rtts):
    n = len(rtts)
    t_a_2 = stats.t.ppf(1 - 0.025, n - 2)
    sqRootN = np.sqrt(n)
    numerator = t_a_2 * (n - 1)
    denominator = sqRootN * np.sqrt(n - 2 + np.power(t_a_2, 2))
    return numerator / denominator
