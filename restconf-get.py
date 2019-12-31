import requests
import json

router = {"ip": "ios-xe-mgmt.cisco.com", "port": "9443",
          "user": "root", "password": "D_Vay!_10&"}

headers = {"Accept": "application/yang-data+json",
           "Content-Type": "application/yang-data+json"}

url = f"https://{router['ip']}:{router['port']cmdrestconf/data/ietf-interfaces:interfaces"

response = requests.get(url, headers=headers, auth=(
    router['user'], router['password']), verify=False)

api_data = response.json()

print(api_data)