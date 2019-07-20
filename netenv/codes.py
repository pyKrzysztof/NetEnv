CHANNEL_FAILURE = -2
HOST_UNREACHABLE = -32
GENERAL_FAILURE = -64
TIMEOUT_ERROR = -128
AUTH_ERROR = -256

def error_as_string(code):
    try: code = int(str(code))
    except: pass
    if code == GENERAL_FAILURE:
        return "General Failure."
    elif code == TIMEOUT_ERROR:
        return "Timeout."
    elif code == AUTH_ERROR:
        return "Authentication Error."
    elif code == HOST_UNREACHABLE:
        return "Unreachable Host."
    elif code == CHANNEL_FAILURE:
        return "Internal Channel Failure."
    else:
        return code