import numpy as np
import time
import logging
import scipy
from analytics.adc.mockreader import MockAdcReader
from analytics.gpm.client import Client, GpmOfflineError
from analytics.processing.constants import (
    INNER_THRESHOLD,
    OUTER_THRESHOLD,
    INNER_LOWER_THRESHOLD,
    OUTER_LOWER_THRESHOLD,
    CALIBRATION_DURATION_IN_SECONDS,
)
from analytics.common.loggerutils import detail_trace
from analytics.gpm.constants import *
from analytics.common.decorators import retryable
from analytics import config

logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)


class EmgProcessor:
    """
    The main signal processing class - it reads, processes, and analyzes raw EMG data
    to make a decision on the next state of the arm (i.e Open or Close).
    """

    def __init__(self, adc_reader: MockAdcReader):
        self._adc_reader = adc_reader
        try:
            self.gpm_client = Client()
        except Exception as e:
            logger.error(f"Failed to connect to GPM because of error={e}")
            self.gpm_client = None
        self.activation_state = False
        self.inner_threshold = INNER_THRESHOLD
        self.outer_threshold = OUTER_THRESHOLD
        self.inner_lower_threshold = INNER_LOWER_THRESHOLD
        self.outer_lower_threshold = OUTER_LOWER_THRESHOLD
        self.inner_max_signal = float('-inf')
        self.outer_max_signal = float('-inf')
        self.config = config["processing"]
        logger.info(f"Processing module configs: {self.config}")
        self._sleep_duration = self.config[
            "sleep_between_processing_in_seconds"
        ].as_number()
        self._buffers = None

    def calibrate(self):
        def calibrate_threshold(duration, message):
            logger.warn(message)
            end_time = time.time() + duration
            while time.time() < end_time:
                inner_signal, outer_signal = self._adc_reader.get_current_buffers()
                self.inner_max_signal = max(self.inner_max_signal, np.max(inner_signal))
                self.outer_max_signal = max(self.outer_max_signal, np.max(outer_signal))

        calibrate_threshold(
            CALIBRATION_DURATION_IN_SECONDS,
            f"Starting calibration... Relax arm for {CALIBRATION_DURATION_IN_SECONDS} seconds.",
        )
        calibrate_threshold(
            CALIBRATION_DURATION_IN_SECONDS, "Contract inner arm muscle."
        )
        calibrate_threshold(
            CALIBRATION_DURATION_IN_SECONDS, "Contract outer arm muscle."
        )

        logger.warn("Calibration completed.")
        logger.warn(f"Inner max: {self.inner_max_signal}")
        logger.warn(f"Outer max: {self.outer_max_signal}")

        return self.inner_max_signal, self.outer_max_signal

    def preprocess(self, signals):
        # TODO determine values for following parameters
        # sampling_freq
        # highpass (for inner and outer)
        # lowpass (for inner and outer)
        # smoothing_window = 100
        # notch_filter = True # if we decide to use the notch filter

        def bandpass_filter(signal, sampling_freq, highpass_freq, lowpass_freq):
            b, a = scipy.signal.butter(
                4, [highpass_freq, lowpass_freq], btype="bandpass", fs=sampling_freq
            )
            filtered_signal = scipy.signal.filtfilt(b, a, signal)
            return filtered_signal

        # rectify, normalize, smooth
        def normalize_and_smooth(
            signal, smoothing_window: int, max_value: int
        ) -> np.ndarray:
            rectified_signal = np.abs(signal)
            normalized_signal = rectified_signal / max_value
            smoothed_signal = np.convolve(
                normalized_signal,
                np.ones(smoothing_window) / smoothing_window,
                mode="valid",
            )
            return normalized_signal

        def notch_filter(signal, sampling_freq, f0, Q):
            if f0 > sampling_freq / 2:
                raise Exception(
                    "notch frequency must be less than or equal to fs/2 (f0 <= fs/2"
                )
            b, a = scipy.signal.iirnotch(f0, Q, sampling_freq)
            notched_filtered_data = scipy.signal.filtfilt(b, a, signal)
            return notched_filtered_data

        inner_signal = signals[0]
        outer_signal = signals[1]

        return inner_signal, outer_signal

    def run_detect_activation_loop(self):
        while True:
            with detail_trace(
                "Processing signals", logger, log_start=False
            ) as trace_step:
                signal_buffer = (
                    self._adc_reader.get_current_buffers()
                )  # returns a 2d numpy array [[inner_signal], [outer_signal]]
                trace_step("Read signal buffer")
                self._buffers = self.preprocess(signal_buffer)
                inner_signal, outer_signal = self._buffers
                max_inner = np.max(inner_signal) if len(inner_signal) != 0 else 0
                max_outer = np.max(outer_signal) if len(outer_signal) != 0 else 0
                
                self.gpm_client.send_message(
                                    MAESTRO_RESOURCE, MAESTRO_OPEN_FIST)
                time.sleep(3)
                                    
                self.gpm_client.send_message(
                                    MAESTRO_RESOURCE, MAESTRO_CLOSE_FIST)
                time.sleep(3)

    @retryable(base_delay_in_seconds=0.1, logger=logger)
    def get_current_buffers(self):
        if self._buffers is None:
            raise Exception("Buffers have not yet been initialized")
        inner, outer = self._buffers
        return (inner, outer)

    def get_thresholds(self):
        return self.inner_threshold, self.outer_threshold
