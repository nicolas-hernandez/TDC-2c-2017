from os import getuid
import traceroute as tr
import json
if __name__ == "__main__":

    if getuid() != 0:
        print('Ejecutar con permisos de administrador')
        exit(1)
    #university = "www.imperial.ac.uk"
    #university = "www.kuleuven.be"
    university = "www.uzh.ch"
    #university = "www.stanford.edu"
    #university = "www.unr.edu.ar" #NO RESPONDE EL DESTINO (BLOQUEADO POR FIREWALL?)
    #university = "www.unc.edu.ar"
    route = tr.TraceRoute(university)
    print(json.dumps(route.traced, indent=4))
