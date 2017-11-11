from os import getuid
import traceroute as tr
import json
import argparse 

if __name__ == "__main__":

    if getuid() != 0:
        print('Ejecutar con permisos de administrador')
        exit(1)
    #Parse command line arguments
    parser = argparse.ArgumentParser(description='Implementacion de utilidad traceroute.')
    parser.add_argument("address", help="url o ip que se desea routear")            
    args = parser.parse_args()                                            
    route = tr.TraceRoute(args.address)
    print(json.dumps(route.traced, indent=4))
