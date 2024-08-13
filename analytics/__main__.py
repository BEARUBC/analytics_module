import analytics
import logging
from analytics.gpm.constants import *
from analytics.gpm.client import Client
from analytics.metrics.exporter import start_metrics_server
from analytics.adc.mock_reader import MockAdcReader
from threading import Thread
import time

logger = logging.getLogger(__name__)

def main():
    analytics.initialize_config_and_logging()
    start_metrics_server()
    adc_reader = MockAdcReader()
    reader_thread = Thread(target = adc_reader.start_reading)
    reader_thread.start()
    while True:
        logger.info(f"Current value of buffer = {adc_reader.get_current_buffers()}")
        time.sleep(10)

if __name__ == "__main__":
    main()