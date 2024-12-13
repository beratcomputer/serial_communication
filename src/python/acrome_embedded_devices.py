from Stewart import *

#port = AcromeDevicesPort("COM11")

def scan_Stewarts(port:AcromeDevicesPort):
    id_list = []
    for i in range(255):
        print(i)
        stewart = Stewart(i, port)
        if stewart.ping()== True:
            id_list.append(i)
    return id_list


#print(scan_Stewarts(port))