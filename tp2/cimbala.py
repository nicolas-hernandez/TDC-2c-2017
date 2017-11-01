import numpy as np
def detectarOutliers(mediciones):
    rttDifs = []
    rttAnterior = 0

    for medicion in mediciones:
        rttDifs.append(float(medicion[2]) - rttAnterior)
        rttAnterior = float(medicion[2])

    outliers = cimbala(rttDifs)
    #outliersRemoviendo = cimbalaRemoviendo(rttDifs)

    return outliersStandard#, outliers_removiendo
    
def cimbala(rttDifs):
    outliers = []
    if len(rttDifs) > 0:
        media = np.mean(rttDifs)
        desvio_standard = np.std(rttDifs)
        tg = thompsonGamma(rttDifs)
    for rttDif in rttDifs:
        delta = np.absolute(rttDif - media)
        if (delta > tg * desvio_standard):
            outliers.append(rttDif)
    return outliers

def cimbalaRemoviendo(rttDifs):
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
                delta = np.absolute(rtt_dif - media)
                if (delta > tg * desvio_standard):
                    outlier = rttDif
                    break
                if outlier:
                    rttDifs.remove(outlier)
                    outliers.append(outlier)
                    seguirBuscando = True
    return outliers


def thompson_gamma(rtts):
    n = len(rtts)
    t_a_2 = stats.t.ppf(1 - 0.025, n - 2)
    sqRootN = np.sqrt(n)
    numerator = t_a_2 * (n - 1)
    denominator = sqRootN * np.sqrt(n - 2 + np.power(t_a_2, 2))
    return numerator / denominator
