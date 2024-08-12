import socket
import logging
import analytics.protobuf.sgcp_pb2 as sgcp
from analytics.gpm.constants import GPM_HOST, GPM_PORT, READ_BUF_SIZE
from analytics.common.loggerutils import detail_trace

logger = logging.getLogger(__name__)

class Client():
    """
    A simple class to manage the TCP connection to the GPM module and provide an easy-to-use
    interface to create requests from the SGCP proto definitions and decode GPM responses
    """
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((GPM_HOST, GPM_PORT))

    def send_message(self, resource: str, task_code: str):
        with detail_trace(f"Sending request to GPM for resource={resource} with task_code={task_code}", logger, log_start=True) as trace_step:
            request = sgcp.Request()
            request.resource = sgcp.Resource.Value(resource)
            request.taskCode = task_code
            # despite the name, `SerializeToString` returns the `bytes` type
            buf = request.SerializeToString()
            # prefix (64-bit) length to the protobuf frame to enable streaming
            buf_len = len(buf).to_bytes(8, byteorder='big')
            self.socket.sendall(buf_len + buf)
            trace_step("Sent message")
            data = self.recv()
            trace_step("Received response")
            return data
        
    def recv(self) -> bytes:
        return self.socket.recv(READ_BUF_SIZE)
