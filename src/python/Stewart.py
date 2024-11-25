## this is Stewart class for controlling Stewart devices.
import enum
import struct
from crccheck.crc import Crc32Mpeg2 as CRC32
import time
import serial
from Acrome_Device import *

STEWART_HEADER = 0x55

class Stewart_ExtraCommands(enum.IntEnum):
	CALIBRATE = 0x15

Index_Stewart = enum.IntEnum('Index', [
	'Header',
	'DeviceID',
	'PackageSize',
	'Command',
	'HardwareVersion',
	'SoftwareVersion',
	'Baudrate', #'WritableStart' = iBaudrate
	'Status',
	'MotorSizes',
	'MotorMaxSpeeds',
	'MotorCPRs',
	'DeviceLoopFrequency',
	'OperationMode',# RUNTIME
	'TorqueEnable',	
	'TargetCoordinate_X',
	'TargetCoordinate_Y',
	'TargetCoordinate_Z',
	'TargetRotation_Roll',
	'TargetRotation_Pitch',
	'TargetRotation_Yaw',
	'Offset_X',
	'Offset_Y',
	'Offset_Z',
	'InternalTrajectory_SpeedSetting',
	'InternalTrajectory_time',
	'MotorsPID_Gain',
	'MotorsPID_Deadbend',
	'Motor1_P',
	'Motor2_P',
	'Motor3_P',
	'Motor4_P',
	'Motor5_P',
	'Motor6_P',
	'Motor1_I',
	'Motor2_I',
	'Motor3_I',
	'Motor4_I',
	'Motor5_I',
	'Motor6_I',
	'Motor1_D',
	'Motor2_D',
	'Motor3_D',
	'Motor4_D',
	'Motor5_D',
	'Motor6_D',
	'PresentPosition_X', #'ReadOnlyStart' = 'PresentPosition_X'
	'PresentPosition_Y',
	'PresentPosition_Z',
	'PresentPosition_Roll',
	'PresentPosition_Pitch',
	'PresentPosition_Yaw',
	'PresentVelocity_X',
	'PresentVelocity_Y',
	'PresentVelocity_Z',
	'PresentVelocity_Roll',
	'PresentVelocity_Pitch',
	'PresentVelocity_Yaw',
	'Motor1_Speed',
	'Motor2_Speed',
	'Motor3_Speed',
	'Motor4_Speed',
	'Motor5_Speed',
	'Motor6_Speed',
	'Motor1_Position',
	'Motor2_Position',
	'Motor3_Position',
	'Motor4_Position',
	'Motor5_Position',
	'Motor6_Position',
	'CRCValue',
], start=0)


class Stewart(Acrome_Device):
	def __init__(self, ID, port, baudrate) -> bool:
		
		self.__ack_size = 0
		if ID > 255 or ID < 0:
			raise ValueError("Device ID can not be higher than 253 or lower than 0!")
		Datas_Stewart = [
            Data_(Index_Stewart.Header, 'B', False, 0x55),
            Data_(Index_Stewart.DeviceID, 'B'),
            Data_(Index_Stewart.PackageSize, 'B'),
            Data_(Index_Stewart.Command, 'B'),
            Data_(Index_Stewart.HardwareVersion, 'I'),
            Data_(Index_Stewart.SoftwareVersion, 'I'),
            Data_(Index_Stewart.Baudrate, 'I'),
			Data_(Index_Stewart.Status, 'B'),
			Data_(Index_Stewart.MotorSizes, 'B'),
			Data_(Index_Stewart.MotorMaxSpeeds,'f'),
			Data_(Index_Stewart.MotorCPRs,'f'),
            Data_(Index_Stewart.DeviceLoopFrequency,'f'),
            Data_(Index_Stewart.OperationMode, 'I'),
			Data_(Index_Stewart.TorqueEnable, 'I'),
            Data_(Index_Stewart.TargetCoordinate_X,'f'),
            Data_(Index_Stewart.TargetCoordinate_Y,'f'),
            Data_(Index_Stewart.TargetCoordinate_Z,'f'),
            Data_(Index_Stewart.TargetRotation_Roll,'f'),
            Data_(Index_Stewart.TargetRotation_Pitch,'f'),
            Data_(Index_Stewart.TargetRotation_Yaw,'f'),
            Data_(Index_Stewart.Offset_X,'f'),
            Data_(Index_Stewart.Offset_Y,'f'),
            Data_(Index_Stewart.Offset_Z,'f'),
            Data_(Index_Stewart.InternalTrajectory_SpeedSetting,'f'),
            Data_(Index_Stewart.InternalTrajectory_time,'f'),
            Data_(Index_Stewart.MotorsPID_Gain,'f'),
            Data_(Index_Stewart.MotorsPID_Deadbend,'f'),
            Data_(Index_Stewart.Motor1_P,'f'),
            Data_(Index_Stewart.Motor2_P,'f'),
            Data_(Index_Stewart.Motor3_P,'f'),
            Data_(Index_Stewart.Motor4_P,'f'),
            Data_(Index_Stewart.Motor5_P,'f'),
            Data_(Index_Stewart.Motor6_P,'f'),
            Data_(Index_Stewart.Motor1_I,'f'),
            Data_(Index_Stewart.Motor2_I,'f'),
            Data_(Index_Stewart.Motor3_I,'f'),
            Data_(Index_Stewart.Motor4_I,'f'),
            Data_(Index_Stewart.Motor5_I,'f'),
            Data_(Index_Stewart.Motor6_I,'f'),
            Data_(Index_Stewart.Motor1_D,'f'),
            Data_(Index_Stewart.Motor2_D,'f'),
            Data_(Index_Stewart.Motor3_D,'f'),
            Data_(Index_Stewart.Motor4_D,'f'),
            Data_(Index_Stewart.Motor5_D,'f'),
            Data_(Index_Stewart.Motor6_D,'f'),
            Data_(Index_Stewart.Motor6_D,'f'), 
            Data_(Index_Stewart.PresentPosition_X,'f'),
            Data_(Index_Stewart.PresentPosition_Y,'f'),
            Data_(Index_Stewart.PresentPosition_Z,'f'),
            Data_(Index_Stewart.PresentPosition_Roll,'f'),
            Data_(Index_Stewart.PresentPosition_Pitch,'f'),
            Data_(Index_Stewart.PresentPosition_Yaw,'f'),
            Data_(Index_Stewart.PresentVelocity_X,'f'),
            Data_(Index_Stewart.PresentVelocity_Y,'f'),
            Data_(Index_Stewart.PresentVelocity_Z,'f'),
            Data_(Index_Stewart.PresentVelocity_Roll,'f'),
            Data_(Index_Stewart.PresentVelocity_Pitch,'f'),
            Data_(Index_Stewart.PresentVelocity_Yaw,'f'),
            Data_(Index_Stewart.Motor1_Speed,'f'),
            Data_(Index_Stewart.Motor2_Speed,'f'),
            Data_(Index_Stewart.Motor3_Speed,'f'),
            Data_(Index_Stewart.Motor4_Speed,'f'),
            Data_(Index_Stewart.Motor5_Speed,'f'),
            Data_(Index_Stewart.Motor6_Speed,'f'),
            Data_(Index_Stewart.Motor1_Position,'f'),
            Data_(Index_Stewart.Motor2_Position,'f'),
            Data_(Index_Stewart.Motor3_Position,'f'),
            Data_(Index_Stewart.Motor4_Position,'f'),
            Data_(Index_Stewart.Motor5_Position,'f'),
            Data_(Index_Stewart.Motor6_Position,'f'),
            Data_(Index_Stewart.CRCValue, 'I'),
        ]
		super().__init__(STEWART_HEADER, ID, Datas_Stewart, port, baudrate)
		self._vars[Index_Stewart.DeviceID].value(ID)

	def calibrate(self):
		fmt_str = '<BBBB'
		struct_out = list(struct.pack(fmt_str, *[self._header, self._id, 8, Stewart_ExtraCommands.CALIBRATE]))
		struct_out = bytes(struct_out) + struct.pack('<I', CRC32.calc(struct_out))
		self._ack_size = 8
		#burayi kontrol et.
		self._write_bus(struct_out)
		print(list(struct_out))
	
	



"""
def stewarts_sync_set_variable(ids, indexes, vars):
	#burada ic ice variablesa yazilacak. eger set edilmesini istenmedigi bir durum var ise arrayin icine none yazilmali.
	#ornek kullanim
	# stewarts_sync_set_variable([0,1,3], [Index_Stewart.goalCoordinate_x, Index_Stewart.goalCoordinate_y, Index_Stewart.goalCoordinate_z], [[1,2,3],[2,3,0],[2,None,3]])
	
    #checks
	
    pass

def stewarts_sync_drive_coordinates(ids, vars):  
	# vars = [[x, y, z, roll, pitch, yaw], [x, y, z, roll, pitch, yaw], [x, y, z, roll, pitch, yaw]]]
	# ids kadar uzunlugu olmali ve eslesme o kadar gitmeli.
	
    if len(ids) != len(vars):
	    raise ValueError("ID length and variable list length is not equal!")
		
    stewarts_sync_set_variable([0,1,3], [Index_Stewart.goalCoordinate_x, Index_Stewart.goalCoordinate_y, Index_Stewart.goalCoordinate_z], [[1,2,3],[2,3,0],[2,None,3]])
    pass

def stewarts_sync_drive_coordinates():
	pass
"""