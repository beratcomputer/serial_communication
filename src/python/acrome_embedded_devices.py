from Stewart import *



stewart_1 = Stewart(0, 'ADASD', 1123123, True)
stewart_1.get_classic_packet_0()

print(stewart_1._vars[81].index())

def scan_Stewarts(port, baudrate = 921600):
    id_list = []
    for i in range(255):
        stewart = Stewart(i, port, baudrate, True)
        if stewart.ping()== True:
            id_list.append(i)
    return id_list

def scan_all_Devices():
    pass