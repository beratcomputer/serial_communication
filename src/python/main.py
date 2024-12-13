from acrome_embedded_devices import *
port_name = "COM11"
baudrate = 921600 
port = AcromeDevicesPort(port_name)
Stewart_0 = Stewart(0, port)
#Stewart_1 = Stewart(1, port, baudrate)


print(Stewart_0.calibrate())

Stewart_0.control()
Stewart_0.write_var([Index_Stewart.OperationMode, Stewart_ControlModes.InternalTrajectory])
#Stewart_0.write_var([Index_Stewart.Motor1_P, float(10)], [Index_Stewart.Motor2_P, float(10)], [Index_Stewart.Motor1_3, float(10)], [Index_Stewart.Motor4_P, float(10)], [Index_Stewart.Motor5_P, float(10)], [Index_Stewart.Motor6_P, float(10)])
Stewart_0.write_var([Index_Stewart.Motor1_P, 6.0],[Index_Stewart.Motor2_P, 6.0],[Index_Stewart.Motor3_P, 6.0])
Stewart_0.write_var([Index_Stewart.Motor4_P, 6.0],[Index_Stewart.Motor5_P, 6.0],[Index_Stewart.Motor6_P, 6.0])

Stewart_0.write_var([Index_Stewart.Motor1_D, 1.0],[Index_Stewart.Motor2_D, 1.0],[Index_Stewart.Motor3_D, 1.0])
Stewart_0.write_var([Index_Stewart.Motor4_D, 1.0],[Index_Stewart.Motor5_D, 1.0],[Index_Stewart.Motor6_D, 1.0])

while True:
    xyz = [0,0,0]
    xyz[0] = input(f"x = ")
    xyz[1] = input(f"y = ")
    xyz[2] = input(f"z = ")
    roll = input(f"roll = ")
    pitch = input(f"pitch = ")
    
    Stewart_0.write_var([Index_Stewart.TargetCoordinate_X, float(xyz[0])], [Index_Stewart.TargetCoordinate_Y, float(xyz[1])], [Index_Stewart.TargetCoordinate_Z, float(xyz[2])], [Index_Stewart.TargetRotation_Roll, float(roll)], [Index_Stewart.TargetRotation_Pitch, float(pitch)])
    Stewart_0.write_var([Index_Stewart.TorqueEnable , 1])

while True:
    motors = [0,0,0,0,0,0]
    for i in range(len(motors)):
        motors[i] = input(f"{i}. Motor = ")

    Stewart_0.write_var([Index_Stewart.Motor1_GoalPosition, float(motors[0])], [Index_Stewart.Motor2_GoalPosition, float(motors[1])], [Index_Stewart.Motor3_GoalPosition, float(motors[2])], [Index_Stewart.Motor4_GoalPosition, float(motors[3])], [Index_Stewart.Motor5_GoalPosition, float(motors[4])], [Index_Stewart.Motor6_GoalPosition, float(motors[5])])
    Stewart_0.write_var([Index_Stewart.TorqueEnable , 1])

#Stewart_0.control_sync()








#Stewart_0.write_var([Index_Stewart.MotorSizes, 2], [Index_Stewart.Offset_X, float(1000)])
#print(Stewart_0.ping())


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



