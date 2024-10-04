import analytics
import logging
from analytics import config
from analytics.gpm.constants import *
from analytics.metrics.exporter import start_metrics_server
from analytics.processing.filters import EmgProcessor
from analytics.adc.visualization import EmgVisualizer
from threading import Thread

logger = logging.getLogger(__name__)
adc_config = config["adc"]

if adc_config["use_mock_adc"]:
    logger.info("Using mock ADC.")
    from analytics.adc.mockreader import MockAdcReader as Reader
else:
    from analytics.adc.reader import AdcReader as Reader


def main():
    analytics.initialize_config_and_logging()
    adc_reader = Reader()
    Thread(target=adc_reader.start_reading).start()
    emg_processor = EmgProcessor(adc_reader)
    inner_max, outer_max = emg_processor.calibrate()
    # emg_processor.calibrate()
    Thread(target=emg_processor.run_detect_activation_loop).start()
    Thread(target=start_metrics_server, daemon=True).start()
    EmgVisualizer(adc_reader, emg_processor).init_visualization(inner_max, outer_max)


if __name__ == "__main__":
    main()
