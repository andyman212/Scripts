import requests
import json
with open('C:/Users/andym/CodeSamples/Python/Networking/IOS-XE/restconf.json') as payload:
    json_data = json.load(payload)

router = {"ip": "ios-xe-mgmt-latest.cisco.com", "port": "9443",
          "user": "developer", "password": "C1sco12345"}

headers = {"Accept": "application/yang-data+json, application/yang-data.errors+json",
           "Content-Type": "application/yang-data+json"}

url = f"https://{router['ip']}:{router['port']}/restconf/data/ietf-interfaces:interfaces"

response = requests.post(url, headers=headers, auth=(
    router['user'], router['password']), data=json_data, verify=False)

print(response.text)