## this is Stewart class for controlling Stewart devices.
import enum
import struct
from crccheck.crc import Crc32Mpeg2 as CRC32
import time
import serial
from Acrome_Device import *

STEWART_HEADER = 0x55

class Stewart_ControlModes(enum.IntEnum):
	InternalTrajectory = 1,
	ExternalTrajectory0 = 2,
	ExternalTrajectory1 = 3

class Stewart_ExtraCommands(enum.IntEnum):
	IDLE = 0x15,
	CALIBRATE = 0x16,
	CONTROL = 0x17,
	CONTROL_SYNC = 0x18,

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
	'Motor1_GoalPosition',
	'Motor2_GoalPosition',
	'Motor3_GoalPosition',
	'Motor4_GoalPosition',
	'Motor5_GoalPosition',
	'Motor6_GoalPosition',
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
	'Motor1_Gain',
	'Motor2_Gain',
	'Motor3_Gain',
	'Motor4_Gain',
	'Motor5_Gain',
	'Motor6_Gain',
	'Motor1_Deadband',
	'Motor2_Deadband',
	'Motor3_Deadband',
	'Motor4_Deadband',
	'Motor5_Deadband',
	'Motor6_Deadband',
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
	'IMU_Roll',
	'IMU_Pitch',
	'IMU_Yaw',
	'Motor1_CalibrationOutput',
	'Motor2_CalibrationOutput',
	'Motor3_CalibrationOutput',
	'Motor4_CalibrationOutput',
	'Motor5_CalibrationOutput',
	'Motor6_CalibrationOutput',
	'CRCValue',
], start=0)


class Stewart(Acrome_Device):
	def __init__(self, ID, port:AcromeDevicesPort, _test = False) -> bool:
		
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
			Data_(Index_Stewart.TorqueEnable, 'B'),
            Data_(Index_Stewart.TargetCoordinate_X,'f'),
            Data_(Index_Stewart.TargetCoordinate_Y,'f'),
            Data_(Index_Stewart.TargetCoordinate_Z,'f'),
            Data_(Index_Stewart.TargetRotation_Roll,'f'),
            Data_(Index_Stewart.TargetRotation_Pitch,'f'),
            Data_(Index_Stewart.TargetRotation_Yaw,'f'),
            Data_(Index_Stewart.Offset_X,'f'),
            Data_(Index_Stewart.Offset_Y,'f'),
            Data_(Index_Stewart.Offset_Z,'f'),
            Data_(Index_Stewart.InternalTrajectory_SpeedSetting,'B'),
            Data_(Index_Stewart.InternalTrajectory_time,'f'),
			Data_(Index_Stewart.Motor1_GoalPosition, 'f'),
			Data_(Index_Stewart.Motor2_GoalPosition, 'f'),
			Data_(Index_Stewart.Motor3_GoalPosition, 'f'),
			Data_(Index_Stewart.Motor4_GoalPosition, 'f'),
			Data_(Index_Stewart.Motor5_GoalPosition, 'f'),
			Data_(Index_Stewart.Motor6_GoalPosition, 'f'),
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
			Data_(Index_Stewart.Motor1_Gain,'f'),
			Data_(Index_Stewart.Motor2_Gain,'f'),
			Data_(Index_Stewart.Motor3_Gain,'f'),
			Data_(Index_Stewart.Motor4_Gain,'f'),
			Data_(Index_Stewart.Motor5_Gain,'f'),
			Data_(Index_Stewart.Motor6_Gain,'f'),
			Data_(Index_Stewart.Motor1_Deadband,'f'),
			Data_(Index_Stewart.Motor2_Deadband,'f'),
			Data_(Index_Stewart.Motor3_Deadband,'f'),
			Data_(Index_Stewart.Motor4_Deadband,'f'),
			Data_(Index_Stewart.Motor5_Deadband,'f'),
			Data_(Index_Stewart.Motor6_Deadband,'f'),
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
			Data_(Index_Stewart.IMU_Roll,'f'),
			Data_(Index_Stewart.IMU_Pitch,'f'),
			Data_(Index_Stewart.IMU_Yaw,'f'),
			Data_(Index_Stewart.Motor1_CalibrationOutput,'f'),
			Data_(Index_Stewart.Motor2_CalibrationOutput,'f'),
			Data_(Index_Stewart.Motor3_CalibrationOutput,'f'),
			Data_(Index_Stewart.Motor4_CalibrationOutput,'f'),
			Data_(Index_Stewart.Motor5_CalibrationOutput,'f'),
			Data_(Index_Stewart.Motor6_CalibrationOutput,'f'),
            Data_(Index_Stewart.CRCValue, 'I'),
        ]
		super().__init__(STEWART_HEADER, ID, Datas_Stewart, port, _test)
		self._vars[Index_Stewart.DeviceID].value(ID)

	def get_classic_packet_0(self):
		custom_package_list = [Index_Stewart.Motor1_Position, Index_Stewart.Motor2_Position, Index_Stewart.Motor3_Position, Index_Stewart.Motor4_Position, Index_Stewart.Motor5_Position, Index_Stewart.Motor6_Position]
		self.read_var(*custom_package_list)
		
	def calibrate(self):
		fmt_str = '<BBBB'
		struct_out = list(struct.pack(fmt_str, *[self._header, self._id, 8, Stewart_ExtraCommands.CALIBRATE]))
		struct_out = bytes(struct_out) + struct.pack('<I', CRC32.calc(struct_out))
		self._ack_size = 38 #  38 = 4 + 6*(4+1) + 4
		self._write_bus(struct_out)

		indexes = [Index_Stewart.Motor1_CalibrationOutput, Index_Stewart.Motor2_CalibrationOutput, Index_Stewart.Motor3_CalibrationOutput, Index_Stewart.Motor4_CalibrationOutput, Index_Stewart.Motor5_CalibrationOutput, Index_Stewart.Motor6_CalibrationOutput, ]
		if self._read_var_no_timeout():
			return [self._vars[index].value() for index in indexes]
		else:
			return False

	def control(self):
		fmt_str = '<BBBB'
		struct_out = list(struct.pack(fmt_str, *[self._header, self._id, 8, Stewart_ExtraCommands.CONTROL]))
		struct_out = bytes(struct_out) + struct.pack('<I', CRC32.calc(struct_out))
		self._ack_size = 8
		#burayi kontrol et.
		self._write_bus(struct_out)

	def idle(self):
		fmt_str = '<BBBB'
		struct_out = list(struct.pack(fmt_str, *[self._header, self._id, 8, Stewart_ExtraCommands.IDLE]))
		struct_out = bytes(struct_out) + struct.pack('<I', CRC32.calc(struct_out))
		self._ack_size = 8
		#burayi kontrol et.
		self._write_bus(struct_out)


	def control_sync(self):
		fmt_str = '<BBBB'
		struct_out = list(struct.pack(fmt_str, *[self._header, self._id, 8, Stewart_ExtraCommands.CONTROL_SYNC]))
		struct_out = bytes(struct_out) + struct.pack('<I', CRC32.calc(struct_out))
		self._ack_size = 8
		#burayi kontrol et.
		self._write_bus(struct_out)

	def idle(self):
		fmt_str = '<BBBB'
		struct_out = list(struct.pack(fmt_str, *[self._header, self._id, 8, Stewart_ExtraCommands.IDLE]))
		struct_out = bytes(struct_out) + struct.pack('<I', CRC32.calc(struct_out))
		self._ack_size = 8
		#burayi kontrol et.
		self._write_bus(struct_out)
	
	



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