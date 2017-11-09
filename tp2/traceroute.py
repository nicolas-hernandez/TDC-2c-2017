import random
import time
import scapy.all as sp
import numpy as np
import requests as req
import cimbala as cb
from copy import deepcopy

class TraceRoute():#MethodObject jajaja
    def __init__(self, dst):
        self.burstSize = 30
        self.retryNumber = 3
        self.timeout = 0.5#segs?
        self.maxTtl = 30
        self.destination = sp.Net(dst)
        self.echoRequests = sp.IP(dst=self.destination, ttl=(1,self.maxTtl)) / sp.ICMP()
        self.traced = []
        self.trace()

    def trace(self):
        hopCount = 1
        #continenteAnterior = 'SA'
        for request in self.echoRequests:
            request[sp.ICMP].id = random.randint(0, 65535)
            responses = []
            destinationReached = False
            for medicion in range(self.burstSize):
                for reintento in range(self.retryNumber):
                    initTime = time.time()
                    response = sp.sr1(request,timeout=self.timeout)
                    endTime = time.time()
                    rtt = (endTime - initTime)*1000 # time() es en segundos.
                    if response is not None:
                        responses.append((response.src, rtt))
                        destinationReached = self.destination == response.src 
                        break

            hop, rttToHop = self.analyzeResponses(responses)

            self.traced.append({"rtt":rttToHop, "ip_address":hop, "salto_internacional":None, "hop_num":hopCount})
            hopCount = hopCount + 1 
            if destinationReached:
                break

        hopsWithoutRTT = []

        count = len(self.traced)

        total = 0

        for hop in self.traced:
            if hop["rtt"] == None:
                hopsWithoutRTT.append(self.traced.index(hop))
            else:
                total += hop["rtt"]
        
        prom = total/count

        self.cimbalaTraced = deepcopy(self.traced) 
        for index in hopsWithoutRTT:
            hop = self.cimbalaTraced[index]
            hop["rtt"] = prom
                
        self.calculateInternationalJumps()

    def calculateInternationalJumps(self):
        jumpRTTByHop = {}
        jumps = []
        lastNode = None
        for node in self.cimbalaTraced:
            if self.cimbalaTraced.index(node) == 0:
                jumpRTTByHop[node["ip_address"]] = 0
                jumps.append(0)
            else:
                jump = abs(float(node["rtt"]) - float(lastNode["rtt"]))
                jumpRTTByHop[node["ip_address"]] = jump #TODO: Para safar de saltos negativos...
                jumps.append(jump)

            lastNode = node
        
        outliers = cb.detectOutliers(jumps)
        for node in self.traced:
            if node["rtt"] is not None:
                isInternational = jumpRTTByHop[node["ip_address"]] in outliers
                node["salto_internacional"] = isInternational 


    def analyzeResponses(self, responses):
        ipDict = {}
        if len(responses) == 0:
            return (None, None)
        for response in responses:
            if response[0] in ipDict:
                rttAcumulated, quantityAcumulated = ipDict[response[0]]
                ipDict[response[0]] = (rttAcumulated + response[1], quantityAcumulated + 1)
            else:
                ipDict[response[0]] = (response[1], 1)

        quantityMax = 0
        ipChosen = None
        rttMean = 0
        for ip in ipDict.keys():
            rttAcum, cant = ipDict[ip]
            if cant > quantityMax:
                quantityMax = cant
                ipChosen = ip
                rttMean = rttAcum / cant
        return ipChosen, rttMean

if __name__ == "__main__":
    if getuid() != 0:
        print('Ejecutar con permisos de administrador')
        exit(1)
    route = TraceRoute("www.google.com")
    print(json.dumps(route.traced, indent=4))
