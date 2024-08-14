import numpy as np
import time
import logging
import scipy
from analytics.adc.mockreader import MockAdcReader
from analytics.gpm.client import Client, GpmOfflineError
from analytics.processing.constants import INNER_THRESHOLD, OUTER_THRESHOLD, CALIBRATION_DURATION_IN_SECONDS
from analytics.adc.visualization import plot_emg_data
from analytics.common.loggerutils import detail_trace
from analytics.gpm.constants import *

logger = logging.getLogger(__name__)

class EmgProcessor:    
    def __init__(self, adc_reader: MockAdcReader):
        self.adc_reader = adc_reader
        try:
            self.gpm_client = Client()
        except GpmOfflineError as e:
            logger.error(f"Failed to connect to GPM because of error={e}")
            self.gpm_client = None
        self.activation_state = False
        self.inner_threshold=INNER_THRESHOLD
        self.outer_threshold=OUTER_THRESHOLD
    
    def calibrate(self):
        def calibrate_threshold(duration, message):
            logger.info(message)
            end_time = time.time() + duration
            while time.time() < end_time:
                inner_signal, outer_signal = self.adc_reader.get_current_buffers()
                inner_max_signal = max(inner_max_signal, np.max(inner_signal))
                outer_max_signal = max(outer_max_signal, np.max(outer_signal))
        
        inner_max_signal = float('-inf')
        outer_max_signal = float('-inf')

        calibrate_threshold(CALIBRATION_DURATION_IN_SECONDS, f"Starting calibration... Relax arm for {CALIBRATION_DURATION_IN_SECONDS} seconds.")
        calibrate_threshold(CALIBRATION_DURATION_IN_SECONDS, "Contract inner arm muscle.")
        calibrate_threshold(CALIBRATION_DURATION_IN_SECONDS, "Contract outer arm muscle.")

        logger.info("Calibration completed.")
        logger.info(f"Inner max: {inner_max_signal}")
        logger.info(f"Outer max: {outer_max_signal}")

        return inner_max_signal, outer_max_signal
    
    def preprocess(self, signals):
        # TODO determine values for following parameters
        # sampling_freq
        # highpass (for inner and outer)
        # lowpass (for inner and outer)
        # smoothing_window = 100

        def bandpass_filter(signal, sampling_freq, highpass_freq, lowpass_freq):
            b, a = scipy.signal.butter(4, [highpass_freq, lowpass_freq],
                                       btype='bandpass', fs=sampling_freq)
            filtered_signal = scipy.signal.filtfilt(b, a, signal)
            return filtered_signal

        def normalize_and_smooth(signal, window: int, max_value: int) -> np.ndarray:
            rectified_signal = np.abs(signal)
            smoothed_signal = np.convolve(rectified_signal, np.ones(window) / window, mode='valid')
            normalized_signal = smoothed_signal / max_value
            return normalized_signal
        
        inner_signal = signals[0]
        outer_signal = signals[1]

        # TODO see note at the beginning of this method definition
        # inner_signal = bandpass_filter(inner_signal, sampling_freq = 2000,
        #                                highpass_freq = highpass_inner, lowpass_freq=lowpass_inner)
        # outer_signal = bandpass_filter(outer_signal, sampling_freq=2000,
        #                                highpass_freq=highpass_outer, lowpass_freq=highpass_outer)
        # inner_signal = normalize_and_smooth(inner_signal, smoothing_window, max_value)
        # outer_signal = normalize_and_smooth(outer_signal, smoothing_window, max_value)

        # TODO implement larger array that contains past signals
        return inner_signal, outer_signal

    def run_detect_activation_loop(self):
        while True:
            with detail_trace("Processing signals", logger, log_start=True) as trace_step:
                signal_buffer = self.adc_reader.get_current_buffers() # returns a 2d numpy array [[inner_signal], [outer_signal]]
                plot_emg_data(signal_buffer)
                trace_step("Read signal buffer")
                inner_signal, outer_signal = self.preprocess(signal_buffer)
                max_inner = np.max(inner_signal) if len(inner_signal) != 0 else 0 
                max_outer = np.max(outer_signal) if len(outer_signal) != 0 else 0
                if self.activation_state is False:
                    if max_inner > self.inner_threshold:
                        logger.info(f"Receievd inner_signal={max_inner} greater than inner_threshold={self.inner_threshold}, sending activation.")
                        self.activation_state = True
                        if self.gpm_client is not None:
                            self.gpm_client.send_message(MAESTRO_RESOURCE, MAESTRO_OPEN_FIST)
                        else:
                            logger.error("GPM connection failed earlier -- cannot send activation command to Grasp.")

                else:
                    if max_outer > self.outer_threshold:
                        logger.info(f"Receievd outer_signal={max_outer} greater than outer_threshold={self.outer_threshold}, sending de-activation.")
                        self.activation_state = False
                        if self.gpm_client is not None:
                            self.gpm_client.send_message(MAESTRO_RESOURCE, MAESTRO_CLOSE_FIST)
                        else:
                            logger.error("GPM connection failed earlier -- cannot send deactivation command to Grasp.")
            time.sleep(5)
