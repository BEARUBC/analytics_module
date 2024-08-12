import socket
import analytics.protobuf.sgcp_pb2 as sgcp
from analytics.gpm.constants import GPM_HOST, GPM_PORT
from analytics.common.loggerutils import detail_trace

class Client():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((GPM_HOST, GPM_PORT))
        request = sgcp.Request()
        request.resource = sgcp.Resource.Value("MAESTRO")
        request.taskCode = "OPEN_FIST"
        buf = request.SerializeToString() # despite the name, this returns the bytes type
        buf_len = len(buf).to_bytes(8, byteorder='big')
        self.socket.sendall(buf_len + buf)




