import analytics
import logging
from analytics.gpm.constants import *
from analytics.gpm.client import Client
from analytics.metrics.exporter import start_metrics_server

logger = logging.getLogger(__name__)

def main():
    analytics.initialize_config_and_logging()
    start_metrics_server()
    client = Client()
    recv = client.send_message(MAESTRO_RESOURCE, MAESTRO_OPEN_FIST)
    logger.info(f"Received response from GPM; Response={recv}")

if __name__ == "__main__":
    main()