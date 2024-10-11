import analytics
import logging
from analytics import config
from analytics.gpm.constants import *
from analytics.metrics.exporter import start_metrics_server
from analytics.processing.filters import EmgProcessor
from analytics.adc.visualization import CalibrationVisualizer, EmgVisualizer
from analytics.adc.constants import *
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

    if USE_CALIBRATION_VISUALIZER:
        # the matplotlib GUI demands to be in the main thread
        calibration_visualizer = CalibrationVisualizer(adc_reader)
        # thus calibration needs to be done in another thread
        calibration_thread = Thread(target=emg_processor.calibrate, args=(calibration_visualizer,))
        calibration_thread.start()
        calibration_visualizer.init_visualization() # calibration thread tells it when to stop
        calibration_thread.join() # waits for the calibration to finish
    else:
        emg_processor.calibrate(None)

    inner_max, outer_max = emg_processor.get_maximums()
    inner_threshold, outer_threshold = emg_processor.get_thresholds()
    
    Thread(target=emg_processor.run_detect_activation_loop).start()
    Thread(target=start_metrics_server, daemon=True).start()
    if USE_EMG_VISUALIZER: 
        EmgVisualizer(adc_reader, emg_processor).init_visualization(inner_max, outer_max, inner_threshold, outer_threshold)


if __name__ == "__main__":
    main()
