import numpy as np
import time
import AdcReader


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
    
    def preprocess(self):
        pass
    
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
