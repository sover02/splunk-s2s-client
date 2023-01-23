SPLUNK_DEFAULT_INDEX = 'main' # main/default
SPLUNK_DEFAULT_FORWARDER_PORT = 9997
ZLIB_COMPRESSION_DEFAULT_LEVEL = 6

class S2SSignatures():
	SPLUNK_SIGNATURE_V1 = '--splunk-cooked-mode--' #0
	SPLUNK_SIGNATURE_V2 = '--splunk-cooked-mode-v2--' #1
	SPLUNK_SIGNATURE_V2C = '--splunk-cooked-mode-v2--:C' #2
	SPLUNK_SIGNATURE_V3 = '--splunk-cooked-mode-v3--' #3 # Supports capabilities

class S2SKeys():
	s2s_metadata_source = 'MetaData:Source' # # Default value: 'default' or 'main'
	s2s_metadata_sourcetype = 'MetaData:Sourcetype'
	s2s_metadata_host = 'MetaData:Host'
	s2s_metadata_index = 'MetaData:Index'
	s2s_time = '_time'
	s2s_raw = '_raw'
	s2s_done = '_done'
	s2s_path = '_path'
	s2s_cooked = '_cooked' # Default value: '_cooked'
	s2s_channel = '_channel' # Default value: 'remoteport::SRC_PORT' (SRC_PORT is the request's source port, e.g. 49931)
	s2s_savedPort = '_savedPort' # Default value: '9997'
	s2s_savedHost = '_savedHost' # Default value: 'host::SRC_HOST' (SRC_HOST is the request's IP address, e.g. 10.1.1.3)
	s2s_evt_resolve_ad_obj = 'evt_resolve_ad_obj' # Default value: 0
	s2s__metadata_index = '_MetaData:Index' # Default value: 'default'
	s2s_eventId = '__s2s_eventId'
	s2s_pdId = '__s2s_pdId'
	s2s_capabilities = '__s2s_capabilities'
	s2s_control_msg = '__s2s_control_msg'
	s2s_rtype = '__s2s_rtype'
	s2s_rbatch_done = '__s2s_rbatch_done'
	s2s_bucket_type = '__s2s_bucket_type'
	s2s_bid = '__s2s_bid'
	s2s_aid = '__s2s_aid'
	s2s_rslice_offset = '__s2s_rslice_offset'
	s2s_searchable = '__s2s_searchable'
	s2s_target_mask = '__s2s_target_mask'
	s2s_with_hashes = '__s2s_with_hashes'
	s2s_gen_key_1 = '__s2s_gen_key_1'
	s2s_gen_key_2 = '__s2s_gen_key_2'
	s2s_token = '__s2s_token'
	s2s_recover_trailing_msg = '__s2s_recover_trailing_msg'

class S2SPrefix():
	s2s_source = 'source::'
	s2s_sourcetype = 'sourcetype::'
	s2s_host = 'host::'

class S2SCapabilities():
	cap_ack = 'ack'
	cap_compression = 'compression'
	cap_pl = 'pl'
	cap_v4 = 'v4'
	cap_cli_can_rcv_hb = 'cli_can_rcv_hb'
	cap_supports_ack_setting_on_idx = 'supports_ack_setting_on_idx'
	cap_channel_limit = 'channel_limit'

class S2SNG_FieldNameTypes():
	FIELD_NAME_INLINE_STR = 0
	FIELD_NAME_CODE_META_DYNAMIC = 1
	FIELD_NAME_CODE_META_PREDEFINED_STR = 2 # S2SNG_FIELD_CODE_PREDEFIENED_VALUES
	FIELD_NAME_META_INLINE_STR = 3
	
class S2SNG_FieldValueTypes():
	# 	Part of the PipeLineData values
	###################################
	FIELD_VALUE_NUMBER = 0
	FIELD_VALUE_STR = 1
	FIELD_VALUE_CODE_PREDEFINED_STR = 2 # S2SNG_FIELD_CODE_PREDEFIENED_VALUES
	# 	NOT Part of the PipeLineData values (will fail with "Field value could not be interpreted as a PipelineData value:")
	###################################
	FIELD_VALUE_RAW_OFFSET_LEN = 3
	FIELD_VALUE_RAW_OFFSET_LEN_REPEAT_DBL_QUOTE = 4
	FIELD_VALUE_RAW_OFFSET_LEN_REPEAT_SNGL_QUOTE = 5
	FIELD_VALUE_RAW_OFFSET_LEN_CE_SCAPING = 6
	FIELD_VALUE_RAW_OFFSET_LEN_XML_ESCAPING = 7
	FIELD_VALUE_RAW_OFFSET_LEN_XML_ESCAPING_W_CDATA = 8
	FIELD_VALUE_RAW_OFFSET_LEN_URL_ESCAPING = 9
	FIELD_VALUE_NEGATIVE_NUMBER = 10 # Max value < 0x8000000000000000
	FIELD_VALUE_FLOAT32 = 11
	FIELD_VALUE_FLOAT64 = 12

class S2SNGCommands():
	COMMAND_UNK_F8 = 0xf8
	COMMAND_COMPRESS = 0xf9
	COMMAND_UNK_FA = 0xfa
	COMMAND_UNK_FB = 0xfb
	COMMAND_SEND_EVENT = 0xfc
	COMMAND_REMOVE_CHANNEL = 0xfd
	COMMAND_REGISTER_CHANNEL = 0xfe
	COMMAND_TIMEZONE = 0xff

class S2SNGFlags():
	FLAG_RAW_DATA 		= 0x01
	FLAG_STMID 			= 0x02 # starts with AAAAAAAAAAA
	FLAG_FIRST_ID 		= 0x04
	FLAG_TIME 			= 0x08
	FLAG_UNK_8000 		= 0x8000
	FLAG_ESTORAGE_BYTES = 0x10000

class S2SNG_FIELD_CODE_PREDEFIENED_VALUES():
	# Max value < 0x46
	field_as_predefined_string__subsecond = 0 # _subsecond
	field_as_predefined_string_date_second = 1 # date_second
	field_as_predefined_string_date_minute = 2 # date_minute
	field_as_predefined_string_date_hour = 3 # date_hour
	field_as_predefined_string_date_year = 4 # date_year
	field_as_predefined_string_date_month = 5 # date_month
	field_as_predefined_string_date_mday = 6 # date_mday
	field_as_predefined_string_date_wday = 7 # date_wday
	field_as_predefined_string_date_zone = 8 # date_zone
	field_as_predefined_string_sunday = 9 # sunday
	field_as_predefined_string_monday = 10 # monday
	field_as_predefined_string_tuesday = 11 # tuesday
	field_as_predefined_string_wednesday = 12 # wednesday
	field_as_predefined_string_thursday = 13 # thursday
	field_as_predefined_string_friday = 14 # friday
	field_as_predefined_string_saturday = 15 # saturday
	field_as_predefined_string_january = 16 # january
	field_as_predefined_string_february = 17 # february
	field_as_predefined_string_march = 18 # march
	field_as_predefined_string_april = 19 # april
	field_as_predefined_string_may = 20 # may
	field_as_predefined_string_june = 21 # june
	field_as_predefined_string_july = 22 # july
	field_as_predefined_string_august = 23 # august
	field_as_predefined_string_september = 24 # september
	field_as_predefined_string_october = 25 # october
	field_as_predefined_string_november = 26 # november
	field_as_predefined_string_december = 27 # december
	field_as_predefined_string_local = 28 # local
	field_as_predefined_string_punct = 29 # punct
	field_as_predefined_string_timestartpos = 30 # timestartpos
	field_as_predefined_string_timeendpos = 31 # timeendpos
	field_as_predefined_string__indextime = 32 # _indextime
	field_as_predefined_string_MINUS_60 = 33 # -60
	field_as_predefined_string_MINUS_120 = 34 # -120
	field_as_predefined_string_MINUS_180 = 35 # -180
	field_as_predefined_string_MINUS_240 = 36 # -240
	field_as_predefined_string_MINUS_300 = 37 # -300
	field_as_predefined_string_MINUS_360 = 38 # -360
	field_as_predefined_string_MINUS_420 = 39 # -420
	field_as_predefined_string_MINUS_480 = 40 # -480
	field_as_predefined_string_MINUS_540 = 41 # -540
	field_as_predefined_string_MINUS_600 = 42 # -600
	field_as_predefined_string_MINUS_660 = 43 # -660
	field_as_predefined_string_meta = 44 # meta
	field_as_predefined_string_truncated = 45 # truncated
	field_as_predefined_string_timestamp = 46 # timestamp
	field_as_predefined_string_invalid = 47 # invalid
	field_as_predefined_string_none = 48 # none
	field_as_predefined_string_eet = 49 # eet
	field_as_predefined_string_elt = 50 # elt
	field_as_predefined_string_ert = 51 # ert
	field_as_predefined_string_iet = 52 # iet
	field_as_predefined_string_ilt = 53 # ilt
	field_as_predefined_string_usz = 54 # usz
	field_as_predefined_string_nev = 55 # nev
	field_as_predefined_string_nh = 56 # nh
	field_as_predefined_string_ns = 57 # ns
	field_as_predefined_string_nst = 58 # nst
	field_as_predefined_string_nstr = 59 # nstr
	field_as_predefined_string_null = 60 # null
	field_as_predefined_string_false = 61 # false
	field_as_predefined_string_true = 62 # true
	field_as_predefined_string_metric_name = 63 # metric_name
	field_as_predefined_string__value = 64 # _value
	field_as_predefined_string_time = 65 # time
	field_as_predefined_string_linecount = 66 # linecount
	field_as_predefined_string_metric_type = 67 # metric_type
	field_as_predefined_string_metric_timestamp = 68 # metric_timestamp
	field_as_predefined_string__event_status = 69 # _event_status