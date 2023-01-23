import sys
import time
import struct
import socket
import datetime
import zlib
from consts import *

class S2S_NG_KEY_VALUE():
	def __init__(self, key, value, key_type=S2SNG_FieldNameTypes.FIELD_NAME_INLINE_STR, value_type=S2SNG_FieldValueTypes.FIELD_VALUE_STR):
		self.key = key
		self.key_type = key_type
		self.value = value
		self.value_type = value_type

# Splunk-to-Splunk Protcol New Generation
class S2S_NG(): 
	def __init__(self, host='127.0.0.1', port=SPLUNK_DEFAULT_FORWARDER_PORT, is_compressed=False, channel_id=1):
		self.host = host
		self.port = port
		self.channel_id = channel_id
		self.is_compressed = is_compressed
		self.protocol_version = S2SSignatures.SPLUNK_SIGNATURE_V3
		self.forwareder_hostname = 'forwareder_hostname'
		self.management_port = '8089'
		self.connect()

	def connect(self):
		# Open socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(1)
		self.sock.connect((self.host, self.port))
		# Send siganture
		self.send_signature()

 
	def close(self):
		self.sock.close()

	def sr1(self, data, should_recv=False, should_print=False):
		data_recv = None
		# Compress
		if self.is_compressed:
			data_compressed = zlib.compress(data, ZLIB_COMPRESSION_DEFAULT_LEVEL)
			data = bytearray([S2SNGCommands.COMMAND_COMPRESS])
			data += data_compressed
		# Send
		self.sock.send(data)
		# Receive
		if should_recv:
			data_recv = b''
			while True:
				try:
					new_data_recv = self.sock.recv(2048)
				except Exception as e:
					break
				if new_data_recv:
					data_recv += new_data_recv
				else:
					break
			if should_print:
				print('\t - Received: {}'.format(data_recv))

		return data_recv

	def send_signature(self):
		signature = (self.protocol_version.encode() + b'\0' * 128)[:128]
		forwareder_hostname = (self.forwareder_hostname.encode() + b'\0' * 256)[:256]
		management_port = (self.management_port.encode() + b'\0' * 16)[:16]
		signature_message = signature+forwareder_hostname+management_port
		self.sock.send(signature_message)

	### Encoding ###
	def encode_type(self, key, value, key_type=S2SNG_FieldNameTypes.FIELD_NAME_INLINE_STR, value_type=S2SNG_FieldValueTypes.FIELD_VALUE_STR):
		ret = b""

		field_type_flags_val = 0

		# Field Type
		field_key_type 		= key_type & 0b11 				# 2 bits
		field_value_type 	= value_type & 0b1111 			# 4 bits
		field_type_flags 	= field_type_flags_val & 0b111 	# 3 bits
		field_type = field_key_type | (field_value_type << 2) | (field_type_flags << (2+4))
		ret += self.encode_number(field_type)

		# Field Key
		#	0, 3
		if key_type in [S2SNG_FieldNameTypes.FIELD_NAME_INLINE_STR, S2SNG_FieldNameTypes.FIELD_NAME_META_INLINE_STR]:
			ret += self.encode_str(key, null_term=False)
		#	1, 2
		elif key_type in [S2SNG_FieldNameTypes.FIELD_NAME_CODE_META_DYNAMIC, S2SNG_FieldNameTypes.FIELD_NAME_CODE_META_PREDEFINED_STR]:
			ret += self.encode_number(key)
		else:
			raise Exception("Unsupported field key type {}".format(key_type))

		# Field Value
		# 	0, 2, 10
		if value_type in [S2SNG_FieldValueTypes.FIELD_VALUE_NUMBER, S2SNG_FieldValueTypes.FIELD_VALUE_CODE_PREDEFINED_STR, S2SNG_FieldValueTypes.FIELD_VALUE_NEGATIVE_NUMBER]:
			ret += self.encode_number(value)
		# 	1 
		elif value_type == S2SNG_FieldValueTypes.FIELD_VALUE_STR:
			ret += self.encode_str(value, null_term=False)
		# 	3 .. 9
		elif S2SNG_FieldValueTypes.FIELD_VALUE_RAW_OFFSET_LEN <= value_type <= S2SNG_FieldValueTypes.FIELD_VALUE_RAW_OFFSET_LEN_URL_ESCAPING:
			ret += self.encode_base128_le(1, bits_limit=0x20) # field_value_as_offset_pos
			ret += self.encode_base128_le(2, bits_limit=0x20) # field_value_as_offset_len
		# 11, 12
		elif value_type in [S2SNG_FieldValueTypes.FIELD_VALUE_FLOAT32, S2SNG_FieldValueTypes.FIELD_VALUE_FLOAT64]:
			ret += self.encode_base128_le(0, bits_limit=0x20) # field_value_as_estorage_pos
			if field_type_flags & 1:
				ret += self.encode_base128_le(1, bits_limit=0x10)
			if field_type_flags & 2:
				ret += self.encode_base128_le(2, bits_limit=0x10)
		else:
			raise Exception("Unsupported field value type {}".format(value_type))
		return ret

	def encode_str(self, data, null_term=False):
		if type(data) != bytes:
			data = data.encode()
		if null_term:
			data += b'\x00'
		return self.encode_base128_le(len(data)) + data

	def encode_number(self, num):
		return self.encode_base128_le(num, bits_limit=0x40)

	# Encode number as Base128 Little Endian
	def encode_base128_le(self, num, bits_limit=0x40):
		result = bytearray()
		if num.bit_length() > bits_limit:
			raise Exception("Not allowed to encode a number with more than {} bits (got {} bits)".format(bits_limit, num.bit_length()))

		while num.bit_length() > 7:
			single_byte = (num & 0b01111111) | 0b10000000
			result.append(single_byte)
			num = num >> 7
		result.append(num)
		return result

	### Send ###
	def send_register_channel(self, channel_id=None):
		if not channel_id:
			channel_id = self.channel_id
		buf = bytearray([S2SNGCommands.COMMAND_REGISTER_CHANNEL])
		buf += self.encode_number(channel_id)					# Channel ID
		buf += self.encode_str("channel_something_first", null_term=True)	# Channel Name
		# Items
		items_count = 1
		buf += self.encode_number(items_count)
		for i in range(items_count):
			buf += self.encode_str("channel_something_{item_id}".format(item_id=i), null_term=True)
		self.sr1(buf)

	def send_unregister_channel(self, channel_id=None):
		if not channel_id:
			channel_id = self.channel_id
		buf = bytearray([S2SNGCommands.COMMAND_REMOVE_CHANNEL])
		buf += self.encode_number(channel_id)					# Channel ID
		self.sr1(buf)

	def send_timezone(self, timezone):
		buf = bytearray([S2SNGCommands.COMMAND_TIMEZONE])
		buf += self.encode_str(timezone, null_term=True)			# Timezone
		self.sr1(buf)

	def send_register_channel_v2(self, channel_id=None):
		if not channel_id:
			channel_id = self.channel_id
		buf = bytearray([S2SNGCommands.COMMAND_UNK_F8])
		buf += self.encode_number(1)							# Unk		
		buf += self.encode_number(self.channel_id)				# Channel ID
		buf += self.encode_str("channel_something_first", null_term=True)	# Channel Name
		# Items
		items_count = 2
		buf += self.encode_number(items_count)
		for i in range(items_count):
			item_name = "channel_something_{item_id}".format(item_id=i)
			buf += self.encode_str(item_name, null_term=True)
		self.sr1(buf)

	def send_event_ng(self, index=SPLUNK_DEFAULT_INDEX, host='', source='', sourcetype='', raw_data='', list_additionals=None):
		# NOTE: Total request size is 0x4000000 bytes
		fields_value_count = 5 # index, source, sourcetype, host, done
		if list_additionals:
			fields_value_count += len(list_additionals)

		#flags = S2SNGFlags.FLAG_RAW_DATA | S2SNGFlags.FLAG_STMID | S2SNGFlags.FLAG_FIRST_ID | S2SNGFlags.FLAG_TIME | S2SNGFlags.FLAG_ESTORAGE_BYTES
		flags = S2SNGFlags.FLAG_RAW_DATA | S2SNGFlags.FLAG_TIME | S2SNGFlags.FLAG_ESTORAGE_BYTES

		buf = bytearray([S2SNGCommands.COMMAND_SEND_EVENT])
		buf += self.encode_number(self.channel_id)	# Channle code
		buf += self.encode_number(flags) 			# Flags

		# ID starts with: AAAAAAAAAAA
		if flags & S2SNGFlags.FLAG_STMID:
			buf += self.encode_number(0)			# stmid
			buf += self.encode_number(0)			# offset
			buf += self.encode_number(0)			# suboffset

		if flags & S2SNGFlags.FLAG_FIRST_ID:
			buf += self.encode_number(0)			# first id, last id?

		if flags & S2SNGFlags.FLAG_TIME:
			buf += self.encode_number(int(time.time())) # event time

		buf += self.encode_number(fields_value_count) # fields values count
		buf += self.encode_type(key=S2SKeys.s2s_metadata_index, value=index)
		buf += self.encode_type(key=S2SKeys.s2s_metadata_host, value=S2SPrefix.s2s_host+host)
		buf += self.encode_type(key=S2SKeys.s2s_metadata_source, value=S2SPrefix.s2s_source+source)
		buf += self.encode_type(key=S2SKeys.s2s_metadata_sourcetype, value=S2SPrefix.s2s_sourcetype+sourcetype)
		buf += self.encode_type(key=S2SKeys.s2s_done, value=S2SKeys.s2s_done)
		if list_additionals:
			for key_value_type in list_additionals:
				buf += self.encode_type(key=key_value_type.key, value=key_value_type.value, key_type=key_value_type.key_type, value_type=key_value_type.value_type)

		if flags & S2SNGFlags.FLAG_ESTORAGE_BYTES:
			buf += self.encode_str("ESTORAGE_BYTES")

		if flags & S2SNGFlags.FLAG_RAW_DATA:
			buf += self.encode_str(raw_data)

		self.sr1(buf)

	def send_unk_command_fa(self):
		buf = bytearray([S2SNGCommands.COMMAND_UNK_FA])
		buf += self.encode_number(1)							# Unk
		buf += self.encode_number(1)							# Unk
		self.sr1(buf)

	def send_unk_command_fb(self):
		buf = bytearray([S2SNGCommands.COMMAND_UNK_FB])
		buf += self.encode_number(0)							# Unk
		self.sr1(buf)
 