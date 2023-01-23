import sys
import time
import struct
import socket
import datetime
import zlib

from event import *


def example_send_event_v2(ip_addr, is_compressed, event_name):
	protocol_version = S2SSignatures.SPLUNK_SIGNATURE_V2
	is_compressed = True
	event_index = SPLUNK_DEFAULT_INDEX
	event_host = "CLAROTY_HOST"
	event_source = "mysource"
	event_source_type = "mysourcetype"

	# Connect
	print('[-] Connecting to {ip_addr}:{port}'.format(ip_addr=ip_addr, port=SPLUNK_DEFAULT_FORWARDER_PORT))
	print('\t- Protocol version is {protocol_version} | Comperssion mode is {is_compressed}'.format(protocol_version=protocol_version, is_compressed=is_compressed))
	s2s = S2S(host=ip_addr, port=SPLUNK_DEFAULT_FORWARDER_PORT, protocol_version=protocol_version, is_compressed=is_compressed)
	time.sleep(0.3)

	# Send capabilities
	capabilities = {
					S2SCapabilities.cap_ack: '0', # Must be 0
					S2SCapabilities.cap_compression: '1' if is_compressed else '0',
					S2SCapabilities.cap_pl: '6',
					S2SCapabilities.cap_v4: 'true',
					S2SCapabilities.cap_cli_can_rcv_hb: '1',
					S2SCapabilities.cap_supports_ack_setting_on_idx: '1',
					S2SCapabilities.cap_channel_limit: '1',
				}
	print('[-] Setting capabilities: {capabilities}'.format(capabilities=capabilities))
	s2s.send_capabilities(capabilities=capabilities)
	time.sleep(0.3)

	# Send event
	event_data = event_name + '=' + str(time.time())
	print('[-] Sending event (v2) with event:')
	print('		[-] index: {}'.format(event_index))
	print('		[-] host: {}'.format(event_host))
	print('		[-] source: {}'.format(event_source))
	print('		[-] sourcetype: {}'.format(event_source_type))		
	print('		[-] data: {}'.format(event_data))		

	dict_additionals = {
					S2SKeys.s2s_path: '/this/is/path',
					S2SKeys.s2s_eventId: '1',
					S2SKeys.s2s_pdId: '1',
					S2SKeys.s2s_rbatch_done: '1',
					S2SKeys.s2s_bucket_type: '1',
					S2SKeys.s2s_bid: '1',
					S2SKeys.s2s_aid: '1',
					S2SKeys.s2s_rslice_offset: '1',
					S2SKeys.s2s_searchable: '1',
					S2SKeys.s2s_target_mask: '1',
					S2SKeys.s2s_with_hashes: '1',
					S2SKeys.s2s_gen_key_1: '1',
					S2SKeys.s2s_gen_key_2: '1',
					S2SKeys.s2s_recover_trailing_msg: '1',
					S2SKeys.s2s_cooked: '1234',
					S2SKeys.s2s_channel: '1234',
					S2SKeys.s2s_savedPort: '1234',
					S2SKeys.s2s_savedHost: '1234',
					S2SKeys.s2s_evt_resolve_ad_obj: '1234',
					'my_special_field': 'my_special_value',
					#S2SKeys.s2s__metadata_index: 'default',
					#S2SKeys.s2s_token: '1',
					#S2SKeys.s2s_rtype: '1',
				}
	s2s.send_event(index=event_index, host=event_host, source=event_source, sourcetype=event_source_type, raw_data=event_data, timestamp=None, dict_additionals=dict_additionals)

	# Close
	s2s.close()



def main():
	if len(sys.argv) != 2:
		print("Usage: python {} IP_ADDR".format(sys.argv[0]))
		sys.exit(1)

	ip_addr = sys.argv[1]
	example_send_event_v2(ip_addr=ip_addr, is_compressed=False, event_name="event_v2")
	example_send_event_v2(ip_addr=ip_addr, is_compressed=True, event_name="event_v2_compress")


if __name__ == "__main__":
	main()