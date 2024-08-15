import analytics
import logging
from analytics.gpm.constants import *
from analytics.metrics.exporter import start_metrics_server
from analytics.adc.mockreader import MockAdcReader
from analytics.processing.filters import EmgProcessor
from analytics.adc.visualization import EmgVisualizer
from threading import Thread

logger = logging.getLogger(__name__)

def main():
    analytics.initialize_config_and_logging()
    adc_reader = MockAdcReader()
    emg_processor = EmgProcessor(adc_reader)
    Thread(target=adc_reader.start_reading).start()
    Thread(target=emg_processor.run_detect_activation_loop).start()
    Thread(target=start_metrics_server, daemon=True).start()
    EmgVisualizer(adc_reader)
    
if __name__ == "__main__":
    main()