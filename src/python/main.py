from acrome_embedded_devices import *
port = "COM12"
baudrate = 3000000

Stewart_0 = Stewart(0, port, baudrate)
Stewart_1 = Stewart(1, port, baudrate)

print(Stewart_0._vars[Index_Stewart.DeviceID].value())
print(Stewart_1._vars[Index_Stewart.DeviceID].value())


#print(Stewart_0.ping())
#print(list(Stewart_0.write_var([12,42],[23,42])))
print(Stewart_0.write_var([4,233],[2,22]))
print(list(Stewart_0.write_var([4,233],[2,22])))
#Stewart_0.set_variable(Indexes_Stewart.GoalCoordinate, [x,y,z,roll,pitch,yaw])
#Stewart_1.set_variable(Indexes_Stewart.SpeedSetting, 4)

'''
sendStewarts(Indexes_Stewart.GoalCoordinate, [0,[x,y,z,roll,pitch,yaw]], [1,[x,y,z,roll,pitch,yaw]],[2,[x,y,z,roll,pitch,yaw]])

sendStewarts_Coordinates([ids],[[],[],[],])
sendStewarts_MotorPositions()
'''



