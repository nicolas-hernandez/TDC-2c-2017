import numpy as np
import scipy.stats as stats

def detectarOutliers(mediciones):
    rttDifs = []
    rttAnterior = 0

    for medicion in mediciones:
        rttDifs.append(float(medicion) - rttAnterior)
        rttAnterior = float(medicion)

    outliers = cimbala(rttDifs)

    print("rrt difs by jumps: " + str(rttDifs))
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
