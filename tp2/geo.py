from os import getuid
import requests
import json, ast
from pprint import pprint

def geolocateIp(ip):
    response = {}
    if ip != None:
        if ip.startswith("192.168."):
            ip = requests.get('https://api.ipify.org').text

        try:
            response = requests.get("http://ip-api.com/json/" + str(ip)).json()
        except:
            response = {'status': 'fail'}

    return response

def ipContinent(ip):
    geolocalizationInfo = geolocateIp(ip)
    if geolocalizationInfo['status'] != 'success':
        return ""
    else:
        return iso3166CountryToContinent(geolocateIp(ip)['countryCode'])

def geolocateTraceroute(file):
    with open(file) as dataFile:    
        data = json.load(dataFile)
    
    #createJSONFile(data, file)
    getStaticImage(data, file)

def createJSONFile(data, file):
    f = open("coordinates_" + file,"w")
    
    f.write("[\n")

    for node in data:
        response = geolocateIp(node["ip_address"])
        response = ast.literal_eval(json.dumps(response))
        if "lat" in response and "lon" in response:
            lat = response["lat"]
            lon = response["lon"]
            f.write("{'lat':" + str(lat) + ",'lng':" + str(lon) + "}")
            if data.index(node) < len(data)-1:
                f.write(",")
            f.write("\n")

    f.write("]")

    f.close()

def getStaticImage(data, file):    
    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    
    url = "https://maps.googleapis.com/maps/api/staticmap?center=0,0&zoom=2&size=1024x1024&maptype=roadmap&scale=2"
    markers = ""
    path = "&path=color:0x0000ff|weight:5"
    key = "&key=AIzaSyBe1-uJ1v7Wjj_4E980XAmLCzX1vXuUD-4"

    for node in data:
        response = geolocateIp(node["ip_address"])
        response = ast.literal_eval(json.dumps(response))
        if "lat" in response and "lon" in response:
            lat = response["lat"]
            lon = response["lon"]
            markers = markers + "&markers=color:green%7Clabel:" + letters[data.index(node) % 27] + "%7C" + str(lat) + "," + str(lon)
            path = path + "|" + str(lat) + "," + str(lon)

    mapUrl = url + markers + path + key

    print(mapUrl)

def iso3166CountryToContinent(countryCode):
    #"iso 3166 country","continent code"
    with open(file) as dataFile:    
        countryToContinentDict = json.load("countryToContinent.json")
    return countryToContinentDict[countryCode]

if __name__ == "__main__":

    if getuid() != 0:
        print('Ejecutar con permisos de administrador')
        exit(1)
    #Parse command line arguments
    parser = argparse.ArgumentParser(description='Geolocalizacion de los nodos de una ruta. Genera un mapa con los nodos de la ruta ubicados en el.')
    parser.add_argument("file", help="archivo con formato json con el output de nuestro traceroute")            
    args = parser.parse_args()                                            
    geolocateTraceroute(args.file)
