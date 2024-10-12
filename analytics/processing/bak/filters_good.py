import numpy as np
import time
import logging
import scipy
from analytics.adc.mockreader import MockAdcReader
from analytics.gpm.client import Client, GpmOfflineError
from analytics.processing.constants import (
    INNER_THRESHOLD,
    OUTER_THRESHOLD,
    CALIBRATION_DURATION_IN_SECONDS,
)
from analytics.common.loggerutils import detail_trace
from analytics.gpm.constants import *
from analytics.common.decorators import retryable
from analytics import config

logger = logging.getLogger(__name__)


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
        self.config = config["processing"]
        logger.info(f"Processing module configs: {self.config}")
        self._sleep_duration = self.config[
            "sleep_between_processing_in_seconds"
        ].as_number()
        self._buffers = None

    def calibrate(self):
        def calibrate_threshold(duration, message):
            logger.info(message)
            end_time = time.time() + duration
            while time.time() < end_time:
                inner_signal, outer_signal = self._adc_reader.get_current_buffers()
                inner_max_signal = max(inner_max_signal, np.max(inner_signal))
                outer_max_signal = max(outer_max_signal, np.max(outer_signal))

        inner_max_signal = float("-inf")
        outer_max_signal = float("-inf")

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
        # notch_filter = True # if we decide to use the notch filter

        def bandpass_filter(signal, sampling_freq, highpass_freq, lowpass_freq):
            b, a = scipy.signal.butter(
                4, [highpass_freq, lowpass_freq], btype="bandpass", fs=sampling_freq
            )
            filtered_signal = scipy.signal.filtfilt(b, a, signal)
            return filtered_signal

        def normalize_and_smooth(
            signal, smoothing_window: int, max_value: int
        ) -> np.ndarray:
            rectified_signal = np.abs(signal)
            smoothed_signal = np.convolve(
                rectified_signal,
                np.ones(smoothing_window) / smoothing_window,
                mode="valid",
            )
            normalized_signal = smoothed_signal / max_value
            return normalized_signal

        def notch_filter(signal, sampling_freq, f0, Q):
            if f0 > sampling_freq / 2:
                raise Exception(
                    "notch frequency must be less than or equal to fs/2 (f0 <= fs/2"
                )
            b, a = scipy.signal.iirnotch(f0, Q, sampling_freq)
            notched_filtered_data = scipy.signal.filtfilt(b, a, signal)
            return notched_filtered_data

        def root_mean_square(signal, buffer_size):
            # Ensure the signal is a numpy array
            emg_signal = np.array(emg_signal)

            # Initialize an empty list to store the RMS values
            rms_values = []

            # Iterate over the signal in buffer-sized chunks
            for i in range(0, len(emg_signal) - buffer_size + 1):
                buffer = emg_signal[i:i + buffer_size]  # Get the buffer window
                rms = np.sqrt(np.mean(np.square(buffer)))  # Compute RMS for the buffer
                rms_values.append(rms)

            return np.array(rms_values)

        highpass_inner = 100
        lowpass_inner = 900
        highpass_outer = 100
        lowpass_outer = 900
        max_value = 1
        # sampling_freq depends on sleep time of the reading

        filtered_signals = []
        for signal in signals:
            signal = bandpass_filter(
                signal,
                sampling_freq=2000,
                highpass_freq=highpass_inner,
                lowpass_freq=lowpass_inner,
            )
            if notch_filter:
                signal = notch_filter(signal, sampling_freq=2000, f0=850, Q=17)
            # signal = normalize_and_smooth(
            #     signal, smoothing_window=100, max_value=max_value
            # )
            signal = root_mean_square(signal, 50)

            filtered_signals.append(signal)

        inner_signal = filtered_signals[0]
        outer_signal = filtered_signals[1]

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

                determine_activation(max_inner, max_outer)

            # time.sleep(self._sleep_duration) ##### ?

    # Helper Functions
    def determine_activation(max_inner, max_outer):
        if self.activation_state is False:
            if max_inner > self.inner_threshold:
                logger.info(
                    f"Received inner_signal={max_inner} greater than inner_threshold={self.inner_threshold}, sending activation."
                )
                contracts_arm()
                time.sleep(1) # to prevent colliding signal.
        else:
            if max_outer > self.outer_threshold:
                logger.info(
                    f"Received outer_signal={max_outer} greater than outer_threshold={self.outer_threshold}, sending de-activation."
                )
                relaxes_arm()
                time.sleep(1) # to prevent colliding signal.

    def contracts_arm(self):
        self.activation_state = True
        if self.gpm_client is not None:
            self.gpm_client.send_message(
                MAESTRO_RESOURCE, MAESTRO_OPEN_FIST
            )
        else:
            logger.error(
                "GPM connection failed earlier -- cannot send activation command to Grasp."
            )

    def relaxes_arm(self):
        self.activation_state = False
        if self.gpm_client is not None:
            self.gpm_client.send_message(
                MAESTRO_RESOURCE, MAESTRO_CLOSE_FIST
            )
        else:
            logger.error(
                "GPM connection failed earlier -- cannot send deactivation command to Grasp."
            )

    @retryable(base_delay_in_seconds=0.1, logger=logger)
    def get_current_buffers(self):
        if self._buffers is None:
            raise Exception("Buffers have not yet been initialized")
        inner, outer = self._buffers
        return (inner, outer)
