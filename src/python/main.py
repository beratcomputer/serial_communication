from acrome_embedded_devices import *
port = "COM11"
baudrate = 115200

Stewart_0 = Stewart(0, port, baudrate)
#Stewart_1 = Stewart(1, port, baudrate)

print(Stewart_0.read_var(Index_Stewart.MotorSizes, Index_Stewart.Status))



#print(Stewart_0.ping())
#print(list(Stewart_0.write_var([12,42],[23,42])))
#print(Stewart_0.write_var([4,233],[2,22]))
#print(list(Stewart_0.write_var([4,233],[2,22])))
#Stewart_0.set_variable(Indexes_Stewart.GoalCoordinate, [x,y,z,roll,pitch,yaw])
#Stewart_1.set_variable(Indexes_Stewart.SpeedSetting, 4)

#print(Stewart_0.eeprom_save())
#print(list(Stewart_0.eeprom_save()))



'''
sendStewarts(Indexes_Stewart.GoalCoordinate, [0,[x,y,z,roll,pitch,yaw]], [1,[x,y,z,roll,pitch,yaw]],[2,[x,y,z,roll,pitch,yaw]])

sendStewarts_Coordinates([ids],[[],[],[],])
sendStewarts_MotorPositions()
'''



