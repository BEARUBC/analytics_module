import analytics
import logging
from analytics.gpm.constants import *
from analytics.gpm.client import Client
from analytics.metrics.exporter import start_metrics_server

logger = logging.getLogger(__name__)

def main():
    # analytics.initialize_config_and_logging() broken -- TODO: @krarpit fix    
    start_metrics_server()
    client = Client()
    recv = client.send_message(MAESTRO_RESOURCE, MAESTRO_OPEN_FIST)
    print(recv)

if __name__ == "__main__":
    main()