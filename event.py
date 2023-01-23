import sys
import time
import struct
import socket
import datetime
import zlib

from consts import *

# Splunk-to-Splunk Protcol
class S2S(): 
	def __init__(self, host='127.0.0.1', port=SPLUNK_DEFAULT_FORWARDER_PORT, protocol_version=S2SSignatures.SPLUNK_SIGNATURE_V3, is_compressed=False):
		self.host = host
		self.port = port
		self.is_compressed = is_compressed
		self.endianness = '<' if is_compressed else '>' # When the data is compressed, the Splunk uses little endianness
		self.protocol_version = protocol_version
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
 
	def sr1(self, data, should_recv=False, should_print=False):
		data_recv = None
		if self.is_compressed:
			data_without_size_header = data[4:] # in compressed mode the inner header is without size
			data_compressed = zlib.compress(data_without_size_header, ZLIB_COMPRESSION_DEFAULT_LEVEL)
			data_compressed_encoded = struct.pack('>I', len(data_compressed)+1) + data_compressed + b'\0'
			data = struct.pack('>I', len(data_compressed_encoded)) + data_compressed_encoded
		self.sock.send(data)
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

	def encode_data(self, data=''):
		data_bytes = data
		# size , string , null-terminator
		if type(data) != bytes:
			# Assuming string
			data_bytes = data.encode()
		data_len = len(data_bytes) + 1
		return struct.pack(self.endianness+'I', data_len) + data_bytes + b'\0'
 
	def encode_pair(self, key='', value='', prefix_value=''):
		return self.encode_data(key) + self.encode_data(prefix_value + value)
 
	def send_capabilities(self, capabilities):
		# Build pairs
		s2s_capabilities_key = S2SKeys.s2s_capabilities
		s2s_capabilities_value = ''
		for key in capabilities:
			s2s_capabilities_value += '{key}={value};'.format(key=key, value=capabilities[key])
		s2s_capabilities_value = s2s_capabilities_value[:-1]
		# Add key-value pairs
		payload = self.encode_pair(key=s2s_capabilities_key, value=s2s_capabilities_value)
		# Suffix
		payload += struct.pack(self.endianness+'I', 0) + self.encode_data(S2SKeys.s2s_raw) # Suffix
		# Prepare sizes
		msg_size = struct.pack(self.endianness+'I', len(payload) + 4) # 4 bytes for pairs count dword
		pairs_size = struct.pack(self.endianness+'I', 1)
		# Build final payload
		payload_final =  msg_size + pairs_size + payload
		# Send
		self.sr1(payload_final, should_recv=True, should_print=False)

	def send_event(self, index=SPLUNK_DEFAULT_INDEX, host='', source='', sourcetype='', raw_data='', timestamp=None, dict_additionals=None):
		pairs_count = 7 + (len(dict_additionals) if dict_additionals else 0)
		if not timestamp:
			timestamp = str(int(time.time()))
		payload = b''
		# Add key-value pairs
		payload += self.encode_pair(key=S2SKeys.s2s_metadata_source, value=source, prefix_value=S2SPrefix.s2s_source)
		payload += self.encode_pair(key=S2SKeys.s2s_metadata_sourcetype, value=sourcetype, prefix_value=S2SPrefix.s2s_sourcetype)
		payload += self.encode_pair(key=S2SKeys.s2s_metadata_host, value=host, prefix_value=S2SPrefix.s2s_host)
		payload += self.encode_pair(key=S2SKeys.s2s_metadata_index, value=index)
		payload += self.encode_pair(key=S2SKeys.s2s_time, value=timestamp)
		if dict_additionals:
			for key in dict_additionals:
				payload += self.encode_pair(key=key, value=dict_additionals[key])
		payload += self.encode_pair(key=S2SKeys.s2s_done, value=S2SKeys.s2s_done)
		payload += self.encode_pair(key=S2SKeys.s2s_raw, value=raw_data)
		# Suffix
		payload += struct.pack(self.endianness+'I', 0) + self.encode_data(S2SKeys.s2s_raw) # Suffix
		# Sizes
		msg_size = struct.pack(self.endianness+'I', len(payload) + 4) # 4 bytes for pairs count dword
		pairs_size = struct.pack(self.endianness+'I', pairs_count)
		# Final payload
		payload_final = msg_size + pairs_size + payload
		# Send
		self.sr1(payload_final)
 
	def close(self):
		self.sock.close()
 