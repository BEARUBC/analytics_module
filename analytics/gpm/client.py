import socket
import logging
import analytics.protobuf.sgcp_pb2 as sgcp
from analytics import config
from analytics.gpm.constants import PREFIX_LENGTH_SIZE
from analytics.common.loggerutils import detail_trace

logger = logging.getLogger(__name__)

class GpmOfflineError(Exception):
    pass

class Client():
    """
    A simple class to manage the TCP connection to the GPM module and provide an easy-to-use
    interface to create requests from the SGCP proto definitions and decode GPM responses
    """
    def __init__(self):
        self.config = config["gpm"]
        logger.info(f"GPM client configs: {self.config}")
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.config["host"].as_str(), self.config["port"].as_number()))
        except ConnectionRefusedError:
            raise GpmOfflineError("Connection refused. Is GPM up and running?")
        self.READ_BUFFER_SIZE = self.config["read_buffer_size"].as_number()

    def send_message(self, resource: str, task_code: str):
        """
        Sends a SGCP request to GPM

        :param resource: Name of the SGCP resource
        :param task_code: Name of the task_code associated to `resource`
        """
        with detail_trace(f"Sending request to GPM for resource={resource} with task_code={task_code}", logger, log_start=True) as trace_step:
            request = sgcp.Request()
            request.resource = sgcp.Resource.Value(resource)
            request.taskCode = task_code
            # despite the name, `SerializeToString` returns the `bytes` type
            buf = request.SerializeToString()
            # prefix (64-bit) length to the protobuf frame to enable streaming
            buf_len = len(buf).to_bytes(PREFIX_LENGTH_SIZE)
            self.socket.sendall(buf_len + buf)
            trace_step("sent_message")
            data = self.recv()
            trace_step("received_response")
            return data
        
    def recv(self, num_bytes=None) -> bytes:
        """
        Reads num_bytes from underlying TCP stream. This is a blocking function and will wait until 
        some data is available to be read.

        :param num_bytes: Number of bytes to be read from socket
        """
        if num_bytes is None:
            num_bytes = self.READ_BUFFER_SIZE
        return self.socket.recv(num_bytes)
    
    def close(self):
        self.socket.close()
