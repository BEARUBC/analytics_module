import numpy as np
import logging
import matplotlib.pyplot as plt
from analytics.adc.basereader import BaseAdcReader
from matplotlib.animation import FuncAnimation

logger = logging.getLogger(__name__)

class EmgVisualizer:
    """This class spawns a (near) real-time visualization of the incoming EMG values"""
    def __init__(self, adc_reader: BaseAdcReader):
        logger.info("Initializing visualization.")
        self.adc_reader = adc_reader
        self.buffers = adc_reader.get_current_buffers()
        self.anim = FuncAnimation(plt.gcf(), self._update, interval=1000)
        self._update_emg_data_plot()
        plt.tight_layout()
        plt.show()

    def _update(self, _):
        """Used by `matplotlib.animation.FuncAnimation` to update the plot each frame"""
        plt.subplot(2,1,1)
        plt.cla()
        plt.subplot(2,1,2)
        plt.cla()
        self._update_emg_data_plot()

    def _update_emg_data_plot(self):
        """Fetches latest EMG data and updates the plot configurations with these values"""
        self.buffers = self.adc_reader.get_current_buffers()
        inner_buf, outer_buf = self.buffers

        # plot inner muscle EMG readings
        plt.subplot(2,1,1)
        time_buf = np.array([i/1000 for i in range(0, len(inner_buf), 1)]) # sampling rate 1000 Hz
        plt.plot(time_buf, inner_buf)
        plt.xlabel('Time (sec)')
        plt.ylabel('EMG (a.u.)')
        plt.title('Inner EMG readings')

        # plot outer muscle EMG readings
        plt.subplot(2,1,2)
        time_buf = np.array([i/1000 for i in range(0, len(outer_buf), 1)]) # sampling rate 1000 Hz
        plt.plot(time_buf, outer_buf)
        plt.xlabel('Time (sec)')
        plt.ylabel('EMG (a.u.)')
        plt.title("Outer EMG readings")
    