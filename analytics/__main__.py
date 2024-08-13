import analytics
import logging
from analytics.gpm.constants import *
from analytics.gpm.client import Client
from analytics.metrics.exporter import start_metrics_server
from analytics.adc.mock_reader import MockAdcReader
from analytics.common.circularlist import CircularList
from analytics.adc.constants import READ_BUFFER_SIZE
from analytics.common.loggerutils import detail_trace
from analytics.processing.filters import EmgProcessor
from threading import Thread
import numpy as np
import time

logger = logging.getLogger(__name__)

def main():
    analytics.initialize_config_and_logging()
    start_metrics_server()
    adc_reader = MockAdcReader()
    reader_thread = Thread(target = adc_reader.start_reading)
    reader_thread.start()
    emg_processor = EmgProcessor(adc_reader)
    emg_processor.detect_activation()
    

if __name__ == "__main__":
    main()