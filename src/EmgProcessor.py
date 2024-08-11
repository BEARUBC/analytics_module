import numpy as np
import time
import AdcReader
import scipy

class EmgProcessor:
    INNER_THRESHOLD = 0.1
    OUTER_THRESHOLD = 0.9
    ACTIVATION_STATE = False


    
    def __init__(self, *args, **kwargs):
        self.INNER_THRESHOLD = kwargs.get('inner_threshold', 0.1)
        self.OUTER_THRESHOLD = kwargs.get('outer_threshold', 0.9)
    
    def calibrate(self):
        def calibrate_threshold(duration, message):
            print(message)
            end_time = time.time() + duration
            while time.time() < end_time:
                inner_signal, outer_signal = AdcReader.read_buffer()
                inner_max_signal = max(inner_max_signal, np.max(inner_signal))
                outer_max_signal = max(outer_max_signal, np.max(outer_signal))
        
        inner_max_signal = float('-inf')
        outer_max_signal = float('-inf')

        calibrate_threshold(3, "Starting calibration... Relax arm for 3 seconds.")
        calibrate_threshold(3, "Contract inner arm muscle.")
        calibrate_threshold(3, "Contract outer arm muscle.")
        print("Calibration completed.")
        print("Inner max: ", inner_max_signal)
        print("Outer max: ", outer_max_signal)
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
        inner_signal = bandpass_filter(inner_signal, sampling_freq = 2000,
                                       highpass_freq = highpass_inner, lowpass_freq=lowpass_inner)
        outer_signal = bandpass_filter(outer_signal, sampling_freq=2000,
                                       highpass_freq=highpass_outer, lowpass_freq=highpass_outer)
        inner_signal = normalize_and_smooth(inner_signal, smoothing_window, max_value)
        outer_signal = normalize_and_smooth(outer_signal, smoothing_window, max_value)
        # TODO implement larger array that contains past signals
        return inner_signal, outer_signal

    def detect_activation(self):
        signal_buffer = AdcReader.get_buffer() # returns a 2d numpy array [[inner_signal], [outer_signal]]
        inner_signal, outer_signal= self.preprocess(signal_buffer)
        if self.ACTIVATION_STATE is False:
            if np.max(inner_signal) > self.INNER_THRESHOLD:
                self.ACTIVATION_STATE = True
                # send state to the arm
        else:
            if np.max(outer_signal) > self.OUTER_THRESHOLD:
                self.ACTIVATION_STATE = False
                # send state to the arm
    
    def main():
        # for testing timing
        pass
