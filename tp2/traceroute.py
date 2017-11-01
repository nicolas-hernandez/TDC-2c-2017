import random
#import sys
import time
import scapy.all as sp
import numpy as np
import requests as req
#from scipy import stats
#Nuestros modulos
import geo
import cimbala as cb

class TraceRoute():#MethodObject jajaja
    def __init__(self, dst):
        #TODO configurar bien
        self.tamRafaga = 3
        self.cantReintentos = 3
        self.timeout = 0.5#segs?
        self.maxTtl = 20
º
        self.destino = sp.Net(dst)
        self.echoRequests = sp.IP(dst=self.destino, ttl=(1,self.maxTtl)) / sp.ICMP()
        self.traced = []
        self.trace()

    def trace(self):
        hopCount = 1
        #continenteAnterior = 'SA'
        for request in self.echoRequests:
            request[sp.ICMP].id = random.randint(0, 65535)
            respuestas = []
            destinoAlcanzado = False
            for medicion in range(self.tamRafaga):
                for reintento in range(self.cantReintentos):
                    tiempoInicio = time.time()
                    respuesta = sp.sr1(request,timeout=self.timeout)
                    tiempoFin = time.time()
                    rtt = (tiempoFin - tiempoInicio)*1000 # time() es en segundos.
                    if respuesta is not None:
                        respuestas.append((respuesta.src, rtt))
                        destinoAlcanzado = self.destino == respuesta.src 
                        break

            hop, rttToHop = self.analizarRespuestas(respuestas)
            #continenteActual = geo.continenteDeIP(hop)
            #if continenteAnterior != continenteActual:
            #    saltoInternacional = True
            #else:
            #    saltoInternacional = False
            #continenteAnterior = continenteActual
            self.traced.append({"rtt":rttToHop, "ip_address":hop, "salto_internacional":None, "hop_num":hopCount})
            hopCount = hopCount + 1 
            if destinoAlcanzado:
                break
        self.calcularSaltosInternacionales()

    def calcularSaltosInternacionales():
        #detectar outliers se deberia pelear con los nodos null
        outliers = cb.detectarOutliers([node["rtt"] for node in self.traced])
        for node in self.route.traced:
            if node["rtt"] is not None:
                node["salto_internacional"] = node["rtt"] in outliers


    def analizarRespuestas(self, respuestas):
        #TODO rtt deberia bancarla aun si no nos responden?
        #respuesta: NO, ver ejemplo de enunciado
        ipDict = {}
        for respuesta in respuestas:
            if respuesta.src in ipDict:
                rttAcumulado, cantidadAcumulada = ipDict[respuesta.src]
                ipDict[respuesta.src] = (rttAcumulado + respuesta[1], cantidadAcumulada + 1)
            else:
                ipDict[respuesta.src] = (respuesta[1], 1)#respuesta.dst?

        cantidadMaxima = 0
        ipElegida = None
        rttPromedio = 0
        for ip in ipDict.keys():
            rttAcum, cant = ipDict[ip]
            if cant > cantidadMaxima:
                cantidadMaxima = cant
                ipElegida = ip
                rttPromedio = rttAcum / cant
        return ipElegida, rttPromedio

if __name__ == "__main__":
    if getuid() != 0:
        print('Ejecutar con permisos de administrador')
        exit(1)
    route = TraceRoute("www.google.com")
    print(json.dumps(route.traced, indent=4))
