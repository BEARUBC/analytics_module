import time
import logging
from analytics.adc.reader import AdcReader
from .constants import INNER_THRESHOLD, OUTER_THRESHOLD, CALIBRATION_DURATION_IN_SECONDS
from analytics.gpm.client import Client
from analytics.gpm.constants import *


logger = logging.getLogger(__name__)

class EmgProcessor:
    def __init__(self, *args, **kwargs):
        self.activation_state = False
        self.adc_reader = AdcReader()
        self.gpm_client = Client()
        logger.info("Initialized EMG proccessor")
    
    def calibrate(self):
        inner_max_signal = float('-inf')
        outer_max_signal = float('-inf')
        
        def calibrate_threshold(duration, message):
            logger.info(message)
            end_time = time.time() + duration

            for reading in self.adc_reader.read():
                if time.time() > end_time:
                    break
                inner_signal, outer_signal = reading
                inner_max_signal = max(inner_max_signal, inner_signal)
                outer_max_signal = max(outer_max_signal, outer_signal)

        calibrate_threshold(CALIBRATION_DURATION_IN_SECONDS, "Starting calibration... Relax arm for 3 seconds")
        calibrate_threshold(CALIBRATION_DURATION_IN_SECONDS, "Contract inner arm muscle")
        calibrate_threshold(CALIBRATION_DURATION_IN_SECONDS, "Contract outer arm muscle")

        logger.info("Calibration completed")
        logger.info(f"Inner max: {inner_max_signal}")
        logger.info(f"Outer max: {outer_max_signal}")

        return inner_max_signal, outer_max_signal
    
    def preprocess(self, signal):
        # def bandpass_filter(signal, sampling_freq, highpass_freq, lowpass_freq):
        #     b, a = scipy.signal.butter(4, [highpass_freq, lowpass_freq],
        #                                btype='bandpass', fs=sampling_freq)
        #     filtered_signal = scipy.signal.filtfilt(b, a, signal)
        #     return filtered_signal

        # def normalize_and_smooth(signal, window: int, max_value: int) -> np.ndarray:
        #     rectified_signal = np.abs(signal)
        #     smoothed_signal = np.convolve(rectified_signal, np.ones(window) / window, mode='valid')
        #     normalized_signal = smoothed_signal / max_value
        #     return normalized_signal
        
        # inner_signal = signals[0]
        # outer_signal = signals[1]
        # inner_signal = bandpass_filter(inner_signal, sampling_freq = 2000,
        #                                highpass_freq = highpass_inner, lowpass_freq=lowpass_inner)
        # outer_signal = bandpass_filter(outer_signal, sampling_freq=2000,
        #                                highpass_freq=highpass_outer, lowpass_freq=highpass_outer)
        # inner_signal = normalize_and_smooth(inner_signal, smoothing_window, max_value)
        # outer_signal = normalize_and_smooth(outer_signal, smoothing_window, max_value)
        return signal[0], signal[1]

    def detect_activation(self):
        for reading in self.adc_reader.read():
            inner_signal, outer_signal= self.preprocess(reading)
            if self.activation_state is False:
                if inner_signal > INNER_THRESHOLD:
                    self.activation_state = True
                    recv = self.gpm_client.send_message(MAESTRO_RESOURCE, MAESTRO_OPEN_FIST)
                    logger.info(f"Received response from GPM; Response={recv}")
            else:
                if outer_signal > OUTER_THRESHOLD:
                    self.activation_state = False
                    recv = self.gpm_client.send_message(MAESTRO_RESOURCE, MAESTRO_CLOSE_FIST)
                    logger.info(f"Received response from GPM; Response={recv}")
