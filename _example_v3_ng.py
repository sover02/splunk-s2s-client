import sys
import time
import struct
import socket
import datetime
import zlib
from consts import *
from event_ng import *


def example_send_event_ng_v3(ip_addr, is_compressed, event_name):
	protocol_version = S2SSignatures.SPLUNK_SIGNATURE_V3
	is_compressed = is_compressed
	channel_id = 123
	event_index = SPLUNK_DEFAULT_INDEX
	event_host = "CLAROTY_HOST"
	event_source = "mysource"
	event_source_type = "mysourcetype"

	print('[-] Connecting to {ip_addr}:{port}'.format(ip_addr=ip_addr, port=SPLUNK_DEFAULT_FORWARDER_PORT))
	print('\t- Protocol version is {protocol_version}'.format(protocol_version=protocol_version))
	print('\t- Comperssion mode is {is_compressed}'.format(is_compressed=is_compressed))
	print('\t- Channel id {channel_id}'.format(channel_id=channel_id))

	# Connect
	s2s = S2S_NG(host=ip_addr, port=SPLUNK_DEFAULT_FORWARDER_PORT, is_compressed=is_compressed, channel_id=channel_id)

	# Register channel
	print('[-] Registering channel {channel_id}'.format(channel_id=channel_id))
	s2s.send_register_channel()

	# Send event
	event_data = event_name + '=' + str(time.time())
	print('[-] Sending event NG (v3) with event:')
	print('		[-] index: {}'.format(event_index))
	print('		[-] host: {}'.format(event_host))
	print('		[-] source: {}'.format(event_source))
	print('		[-] sourcetype: {}'.format(event_source_type))		
	print('		[-] data: {}'.format(event_data))		

	list_additionals = [
					S2S_NG_KEY_VALUE(S2SKeys.s2s_path, '/this/is/path'),
					S2S_NG_KEY_VALUE(S2SKeys.s2s_eventId, '1'),
					S2S_NG_KEY_VALUE(S2SKeys.s2s_pdId, '1'),
					S2S_NG_KEY_VALUE(S2SKeys.s2s_rbatch_done, '1'),
					S2S_NG_KEY_VALUE(S2SKeys.s2s_bucket_type, '1'),
					S2S_NG_KEY_VALUE(S2SKeys.s2s_bid, '1'),
					S2S_NG_KEY_VALUE(S2SKeys.s2s_aid, '1'),
					S2S_NG_KEY_VALUE(S2SKeys.s2s_rslice_offset, '1'),
					S2S_NG_KEY_VALUE(S2SKeys.s2s_searchable, '1'),
					S2S_NG_KEY_VALUE(S2SKeys.s2s_target_mask, '1'),
					S2S_NG_KEY_VALUE(S2SKeys.s2s_with_hashes, '1'),
					S2S_NG_KEY_VALUE(S2SKeys.s2s_gen_key_1, '1'),
					S2S_NG_KEY_VALUE(S2SKeys.s2s_gen_key_2, '1'),
					S2S_NG_KEY_VALUE(S2SKeys.s2s_recover_trailing_msg, '1')
				]
	s2s.send_event_ng(index=event_index, host=event_host, source=event_source, sourcetype=event_source_type, raw_data=event_data, list_additionals=list_additionals)

	# Unregister
	print('[-] Unregistering channel {channel_id}'.format(channel_id=channel_id))
	s2s.send_unregister_channel()
	s2s.close()



def main():
	if len(sys.argv) != 2:
		print("Usage: python {} IP_ADDR".format(sys.argv[0]))
		sys.exit(1)

	# Settings
	ip_addr = sys.argv[1]
	example_send_event_ng_v3(ip_addr=ip_addr, is_compressed=False, event_name="event_v3")



if __name__ == "__main__":
	main()