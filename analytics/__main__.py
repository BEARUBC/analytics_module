import analytics
import logging
from analytics.gpm.constants import *
from analytics.gpm.client import Client
from analytics.metrics.exporter import start_metrics_server
from analytics.processing.filters_mock import MockEmgProcessor

logger = logging.getLogger(__name__)

def main():
    analytics.initialize_config_and_logging()
    start_metrics_server()
    emg_processor = MockEmgProcessor()
    emg_processor.calibrate()
    emg_processor.detect_activation()

if __name__ == "__main__":
    main()