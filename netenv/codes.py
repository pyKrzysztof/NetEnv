CHANNEL_FAILURE = -2
HOST_UNREACHABLE = -32
GENERAL_FAILURE = -64
TIMEOUT_ERROR = -128
AUTH_ERROR = -256
EXCEPTIONS = [CHANNEL_FAILURE, HOST_UNREACHABLE, GENERAL_FAILURE, TIMEOUT_ERROR, AUTH_ERROR]

def error_as_string(code):
    try: code = int(str(code))
    except: pass
    if code == GENERAL_FAILURE:
        return "General Failure."
    elif code == TIMEOUT_ERROR:
        return "Timeout."
    elif code == AUTH_ERROR:
        return "Authentication Error."
    else:
        return code