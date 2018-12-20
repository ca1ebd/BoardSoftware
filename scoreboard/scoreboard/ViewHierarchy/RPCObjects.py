import json

"""
This file contains definitions for the API request
and response objects as defined by JSON RPC 2.0 protocol
    https://www.jsonrpc.org/specification
    
Things in this file:
    JSONRPC_Request
    JSONRPC_Response
    JSONRPC_Exceptions
    JSONRPC_Errors
"""

'''
A JsonRPC Request must contain 3 elements: method, params, id
    method  - String    - The method the API should execute
    params  - JSON      - Data/Arguments to pass to the method
    id      - Any       - A generic id specified by the requester
    
{
    "method":"info.test",
    "params":{},
    "id":"dummy_test"
}

Note: The official definition includes a "jsonrpc" element which
must always have the value 2.0. Since we don't have any legacy
applications that might be using an older version, we'll leave
this out.
'''
class JsonRpcRequest(dict):

    def __init__(self, raw):
        # super.__init__(self)

        # Validation Stuff
        if raw is None or len(str(raw)) == 0:   raise JsonRpcParseError("No data received!")
        try:
            j = json.loads(raw)
        except:
            raise JsonRpcParseError("Could not decode request!")
        if j is None:           raise JsonRpcParseError
        if 'method' not in j:   raise JsonRpcInvalidRequest("Did not receive 'method'")
        if 'id' not in j:       raise JsonRpcInvalidRequest("Did not receive 'id'")
        if 'params' not in j:   raise JsonRpcInvalidRequest("Did not receive 'params'")
        if type(j['params']) is not dict: raise JsonRpcInvalidRequest("Invalid 'params' type")

        # Grab the values
        self.method = j['method']
        self.id = j['id']
        self.params = j['params']

'''
A JsonRPC Response has a generic structure for success and failure
    pass    - Boolean   - Indicates if the function was successful
    result  - JSON      - The result from the API call
    error   - JSON      - Description of an error if one occurred
    id      - Any       - The id sent by the requester

{
    "pass":true,
    "result":{},
    "error":{},
    "id":"dummy_test"
}

An error object will have the following format
    code    - Int       - A defined error code
    message - String    - A desc of the error code
    data    - JSON      - Any data the application may want to pass back
{
    "code": -32700,
    "message": "Parse Error",
    "data": {}
}
'''
class JsonRpcResponse(dict):

    def __init__(self):
        self['pass'] = True
        self['result'] = {}
        self['error'] = {}
        self['id'] =  None

    def load_success(self, result):
        if type(result) is not dict:
            result = {'raw': result}
        self['result'] = result
        self['pass'] = True
        pass

    def load_error(self, error):
        # print type(error)
        # print (type(error) is JsonRpcException)
        # print (type(error) is JsonRpcInvalidRequest)
        # print isinstance(error, JsonRpcException)
        # print error
        self['pass'] = False
        self['error'] = JsonRpcError(error)


class JsonRpcError(dict):

    def __init__(self, error):
        if isinstance(error, JsonRpcException):
            self['code'] = error.code
            self['message'] = error.msg
        elif isinstance(error, Exception):
            self['code'] = JsonRpcErrors.INTERNAL_ERROR
            self['message'] = 'Unknown System Error; ' + error.message


class JsonRpcErrors():
    PARSE_ERROR         = -32700
    INVALID_REQUEST     = -32600
    METHOD_NOT_FOUND    = -32601
    INVALID_PARAMS      = -32602
    INTERNAL_ERROR      = -32603


# Base Class For Other Exceptions
class JsonRpcException(Exception):
    def __init__(self, value):
        self.msg = value
        self.code = JsonRpcErrors.INTERNAL_ERROR


class JsonRpcParseError(JsonRpcException):
    def __init__(self, value):
        self.msg = value
        self.code = JsonRpcErrors.PARSE_ERROR


class JsonRpcInvalidRequest(JsonRpcException):
    def __init__(self, value):
        self.msg = value
        self.code = JsonRpcErrors.INVALID_REQUEST


class JsonRpcMethodNotFound(JsonRpcException):
    def __init__(self, value):
        self.msg = value
        self.code = JsonRpcErrors.METHOD_NOT_FOUND


class JsonRpcInvalidParams(JsonRpcException):
    def __init__(self, value):
        self.msg = value
        self.code = JsonRpcErrors.INVALID_PARAMS


class JsonRpcInternalError(JsonRpcException):
    def __init__(self, value):
        self.msg = value
        self.code = JsonRpcErrors.INTERNAL_ERROR
