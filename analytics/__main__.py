import analytics
import logging
from analytics.gpm.constants import *
from analytics.metrics.exporter import start_metrics_server
from analytics.adc.mockreader import MockAdcReader
from analytics.processing.filters import EmgProcessor
from threading import Thread

logger = logging.getLogger(__name__)

def main():
    analytics.initialize_config_and_logging()
    metrics_thread = Thread(target=start_metrics_server)
    metrics_thread.start()
    adc_reader = MockAdcReader()
    reader_thread = Thread(target=adc_reader.start_reading)
    reader_thread.start()
    emg_processor = EmgProcessor(adc_reader)
    emg_processor.run_detect_activation_loop()
    
if __name__ == "__main__":
    main()