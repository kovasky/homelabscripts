#!/usr/local/bin/python

import sys
import socket
import concurrent.futures

def getIP(dns_name) -> str:
    try:
        ipAddr = socket.gethostbyname(dns_name)
        return ipAddr
    except socket.gaierror:
        return None

def generateRule(dnsName, currentSID, outputFile) -> None:
    dnsName = dnsName.strip().encode('ascii', errors='ignore')
    ipAddr = getIP(dnsName)

    if ipAddr:
        outboundRule = f'pass ip any any -> {ipAddr} any (msg:"Allow outbound connection to {dnsName}"; sid:{currentSID};)\n'
        outputFile.write(outboundRule)
        print(f"Converted {dnsName} to {ipAddr} and added outbound rule with SID {currentSID}")
        currentSID += 1
        inboundRule = f'pass ip {ipAddr} any -> any any (msg:"Allow inbound connection from {ipAddr}"; sid:{currentSID};)\n'
        outputFile.write(inboundRule)
        print(f"Added inbound rule for {ipAddr} with SID {currentSID}")
        currentSID += 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./generateRules.py inputFile outputFile")
        sys.exit(1)

    inputFilePath = sys.argv[1]
    outputFilePath = sys.argv[2]

    with open(inputFilePath, "r") as inputFile, open(outputFilePath, "w") as outputFile:
        currentSID = 1
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for line in inputFile:
                future = executor.submit(generateRule, line, currentSID, outputFile)
                futures.append(future)
                currentSID += 2
            concurrent.futures.wait(futures)

    print("Rule generation complete")
