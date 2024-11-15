## this is master for connected devices.
import struct
from crccheck.crc import Crc32Mpeg2 as CRC32
import time
import serial
import enum

#Classical_Commands
class Device_Commands(enum.IntEnum):
	PING = 0x00,
	READ = 0x01,
	WRITE = 0x02,
	REBOOT = 0x10,
	EEPROM_WRITE = 0x20,
	BL_JUMP = 0x30,
	WRITE_SYNC = 0x40,
	ACK = 0x80,
	WRITE_ACK = 0x80 | 0x02


class Acrome_Device():
    _BATCH_ID = 254
    def __init__(self, header, id, variables, portname, baudrate=3000000):
        if baudrate > 9500000 or baudrate < 1200:
            raise ValueError("Baudrate must be in range of 1200 to 9.5M")
        else:
            try:
                self.__baudrate = baudrate
                self.__post_sleep = 0
                self.__ph = serial.Serial(port=portname, baudrate=self.__baudrate, timeout=0.1)
            except Exception as e:
                print(f"error: {e}")
        self.__header = header
        self.__id = id
        self._vars = variables
        self._ack_size = 0

    
    def __write_bus(self, data):
        self.__ph.write(data)

    def __read_bus(self, size) -> bytes:
        self.__ph.flushInput()
        return self.__ph.read(size=size)
    
    def __read_ack(self) -> bool:
        ret = self.__read_bus(self._ack_size)
        print(list(ret))
        if len(ret) == self._ack_size:
            if (CRC32.calc(ret[:-4]) == struct.unpack('<I', ret[-4:])[0]):
                if ret[2] > 8:
                    #print("parse daha yazilmadi.")
                    #print(list(ret))
                    #self.parse_received(ret)
                    return True
                else:
                    return True # ping islemi ve WRITE_ACK icin.
            else:
                return False
        else:
            return False
    

    def ping(self):
        fmt_str = '<BBBB'
        struct_out = list(struct.pack(fmt_str, *[self.__header, self.__id, 8, Device_Commands.PING]))
        struct_out = bytes(struct_out) + struct.pack('<I', CRC32.calc(struct_out))
        self._ack_size = 8
        #burayi kontrol et.
        self.__write_bus(struct_out)
        
        if self.__read_ack():
            return True
        else:
            return False
    
    def read_var(self, *indexes):
        self._ack_size = 0
        fmt_str = '<BBBB'+'B'*len(indexes)
        struct_out = list(struct.pack(fmt_str, *[self.__header, self.__id, len(indexes) + 8, Device_Commands.READ, *indexes]))
        struct_out = bytes(struct_out) + struct.pack('<' + 'I', CRC32.calc(struct_out))
        for i in indexes:
            self._ack_size += (self._vars[int(i)].size() + 1)
        self._ack_size += 8
        self.__write_bus(struct_out)

        if self.__read_ack():
            return [self._vars[index].value() for index in indexes]
        else:
            return [None]

    def write_var(self, *idx_val_pairs):
        # bu write_ack nasil calisiyor ogrenmeyi unutma.
        # buraya bir yazilabilir mi kontrolu eklenebilir.
        fmt_str = '<BBBB'
        var_count = 0
        size = 0
        for one_pair in idx_val_pairs:
            try:
                if len(one_pair) != 2:
                    raise ValueError(f"{one_pair} more than a pair! It is not a pair")
                else:
                    fmt_str += ('B' + self._vars[one_pair[0]].type())
                    var_count+=1
                    size += (1 + self._vars[one_pair[0]].size())
            except:
                raise ValueError(f"{one_pair} is not proper pair")
        
        flattened_list = [item for sublist in idx_val_pairs for item in sublist]

        struct_out = list(struct.pack(fmt_str, *[self.__header, self.__id, size + 8, Device_Commands.WRITE, *flattened_list]))
        struct_out = bytes(struct_out) + struct.pack('<' + 'I', CRC32.calc(struct_out))
        self._ack_size = 8
        self.__write_bus(struct_out)
        if self.__read_ack():
            return True
        else:
            return False
        
    def reboot(self):
        fmt_str = '<BBBB'
        struct_out = list(struct.pack(fmt_str, *[self.__header, self.__id, 8, Device_Commands.REBOOT]))
        struct_out = bytes(struct_out) + struct.pack('<' + 'I', CRC32.calc(struct_out))    
        try:     
            self.__write_bus(struct_out)
        except:
            print("port error.....")
	
    def eeprom_save(self):
        fmt_str = '<BBBB'
        struct_out = list(struct.pack(fmt_str, *[self.__header, self.__id, 8, Device_Commands.EEPROM_WRITE]))
        struct_out = bytes(struct_out) + struct.pack('<' + 'I', CRC32.calc(struct_out))
        print(struct_out)
        print(CRC32.calc(struct_out))
        #burayi kontrol et.
        self.__write_bus(struct_out)
        try:     
            self.__write_bus(struct_out)
            if self.__read_ack(id):
                return True
        except:
            print("port error.....")

    def _bootloader_jump():
        pass


class Data_():
	def __init__(self, index, var_type, rw=True, value = 0):
		self.__index = index
		self.__type = var_type
		self.__size  = struct.calcsize(self.__type)
		self.__value = value
		self.__rw = rw

	def value(self, value=None):
		if value is None:
			return self.__value
		elif self.__rw:
			self.__value = struct.unpack('<' + self.__type, struct.pack('<' + self.__type, value))[0]

	def index(self) ->enum.IntEnum:
		return self.__index

	def size(self) -> int:
		return self.__size
	
	def type(self) -> str:
		return self.__type