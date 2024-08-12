import socket
from gpm.constants import GPM_HOST, GPM_PORT
from common.loggerutils import detail_trace

class Client():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((GPM_HOST, GPM_PORT))




