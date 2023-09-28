#!/usr/bin/python3

import sys
import requests
from requests import Response
import json
import ipaddress

def getIPList(apiEndpoint : str, headers : dict) -> json:
    response = requests.get(apiEndpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch existing IP list. Status code: {response.status_code}")
        print(response.text)
        sys.exit(1)

def addIPtoList(ipAddr : str, apiEndpoint : str, headers : dict) -> Response:
    payload = [{"ip": ipAddr}]
    response = requests.post(apiEndpoint, headers=headers, data=json.dumps(payload))
    return response

def removeIPFromList(ipId : str, apiEndpoint : str, headers : dict) -> Response:
    payload = {"items": [{"id": ipId}]}
    response = requests.delete(apiEndpoint, headers=headers, data=json.dumps(payload))
    return response

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./modifyBanList.py <ip> <add|del>")
        sys.exit(1)

    ipAddr = sys.argv[1]

    try:
        addr = ipaddress.IPv6Address(ipAddr)
        first_64_bits = str(addr.exploded).split(':')[:4]
        ipAddr = ':'.join(first_64_bits) + '::/64'
    except:
        pass

    action = sys.argv[2]
    listId = ''
    accountId = ''
    email = ''
    apiKey = ''
    apiEndpoint = f'https://api.cloudflare.com/client/v4/accounts/{accountId}/rules/lists/{listId}/items'

    headers = {
        'X-Auth-Email': f'{email}',
        'X-Auth-Key': f'{apiKey}',
        'Content-Type': 'application/json'
    }

    existingIpList = getIPList(apiEndpoint,headers)
    response = None

    if action == "del":
        ipId = None
        for item in existingIpList['result']:
            if item['ip'] == ipAddr:
                ipId = item['id']
                break
        payload = {"items": [{"id": ipId}]}

        if ipId is not None:
            response = requests.delete(apiEndpoint,headers=headers,data=json.dumps(payload))
    elif not any(item['ip'] == ipAddr for item in existingIpList['result']):
        payload = [{
            "ip": ipAddr
        }]
        response = requests.post(apiEndpoint, headers=headers, data=json.dumps(payload))

    if response is not None:
        if response.status_code == 200:
            print(f"IP address {ipAddr} {action} to the custom IP list successfully.")
    else:
        print(f"Failed to {action} IP address {ipAddr} to the custom IP list.")
