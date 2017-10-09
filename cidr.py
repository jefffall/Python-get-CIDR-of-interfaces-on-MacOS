
# note - this is only tested for MacOS High Sierra on a Macbook Pro.
# will not work in pure linux without modifications


import  subprocess
import re
import os
import sys

print "Finding IPV4 CIDR addresses on MacOS interfaces...\n"

deviceList = subprocess.check_output(['networksetup', '-listallhardwareports'])

devices = deviceList.splitlines()

print "Found these network devices on MacOS:\n"

deviceList = []
for device in devices:
    if "Device:" in device:
        myinterface = re.sub('Device: ', '', device)
        print myinterface
        deviceList.append(myinterface)
        
f = open(os.devnull,"w")
sys.stderr = f

#print deviceList
print "\nList of Network Devices with an associated IPV4 address in CIDR format:\n"

for device in deviceList:
    #print "device: ", device
    try:
        #print "trying"
        ipAddr = subprocess.check_output(['ipconfig', 'getifaddr', device])
        if len(ipAddr):
            netMask = subprocess.check_output(['ipconfig','getoption', device, 'subnet_mask'])
            NetMaskBits = sum([bin(int(x)).count("1") for x in netMask.split(".")])
            cleanIp = ipAddr.rstrip()
            print device+": "+ str(cleanIp) +"/"+ str(NetMaskBits)
    except:
        pass

    