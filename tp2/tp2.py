from os import getuid
import traceroute as tr
import json
if __name__ == "__main__":

    if getuid() != 0:
        print('Ejecutar con permisos de administrador')
        exit(1)
    route = tr.TraceRoute("www.imperial.ac.uk")
    print(json.dumps(route.traced, indent=4))
