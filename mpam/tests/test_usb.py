import usb.core
import serial
import serial.tools.list_ports as port_list
ports = list(port_list.comports())
for p in ports:
    print (p)
od = usb.core.find(idVendor=0x239a, idProduct=0x800b)

with open('/home/Evan/.named-dirs') as f:
    print(f.read())

# print(od)

# od.set_configuration()

#ser = serial.Serial(port = "dev/ttyS2")


a = bytearray(128)

a[56] = a[45] = 1

with open("/dev/ttyS4", "wb") as f:
    f.write(a)
    f.flush()
    f.write(a)
    
    
    







    
