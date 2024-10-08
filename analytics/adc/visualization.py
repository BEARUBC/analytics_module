import numpy as np
import logging
import matplotlib.pyplot as plt
from analytics.adc.basereader import BaseAdcReader
from analytics.processing.filters import EmgProcessor
from analytics.processing.constants import (
    INNER_THRESHOLD,
    OUTER_THRESHOLD,
)
from analytics.adc.constants import *
from matplotlib.animation import FuncAnimation

logger = logging.getLogger(__name__)


class EmgVisualizer:
    """This class spawns a (near) real-time visualization of the incoming EMG values"""

    def __init__(self, adc_reader: BaseAdcReader, emg_processor: EmgProcessor):
        self._adc_reader = adc_reader
        self._emg_processor = emg_processor

    def init_visualization(self, inner_max, outer_max, inner_threshold, outer_threshold):
        logger.info("Initializing visualization.")
        self.inner_max = inner_max
        self.outer_max = outer_max
        self.inner_threshold = inner_threshold
        self.outer_threshold = outer_threshold
        self._num_graphs = 4
        self.anim = FuncAnimation(
            plt.gcf(), self._update, interval=1000, cache_frame_data=False
        )
        self._update_raw_data_plot()
        self._update_processed_data_plot()
        plt.tight_layout()
        plt.show()

    def _update(self, _):
        """Used by `matplotlib.animation.FuncAnimation` to update the plot each frame"""
        self._clear()
        self._update_raw_data_plot()
        self._update_processed_data_plot()

    def _clear(self):
        for i in range(self._num_graphs):
            plt.subplot(GRAPH_DIMENSION_NROWS, GRAPH_DIMENSION_NCOLS, i + 1)
            plt.cla()

    def _make_plot(self, buffer, index, title):
        plt.subplot(GRAPH_DIMENSION_NROWS, GRAPH_DIMENSION_NCOLS, index)
        time_buf = np.array([i / 1000 for i in range(0, len(buffer), 1)])
        plt.plot(time_buf, buffer)
        plt.xlabel("Time (sec)")
        plt.ylabel("EMG (a.u.)")
        plt.title(title)

    def _update_raw_data_plot(self):
        """Fetches latest EMG data and updates the plot configurations with these values"""
        inner_buf, outer_buf = self._adc_reader.get_current_buffers()
        # plot inner muscle EMG readings
        self._make_plot(inner_buf, 1, "Raw Inner EMG Data")
        plt.axhline(y = self.inner_max, color = 'r', linestyle = 'dashed', label = "Max")
        # plot outer muscle EMG readings
        self._make_plot(outer_buf, 2, "Raw Outer EMG Data")
        plt.axhline(y = self.outer_max, color = 'r', linestyle = 'dashed', label = "Max")

    def _update_processed_data_plot(self):
        """Fetches latest processed EMG data and updates the plot configurations with these values"""
        inner_buf_clean, outer_buf_clean = self._emg_processor.get_current_buffers()
        # plot inner muscle EMG readings
        self._make_plot(inner_buf_clean, 3, "Processed Inner EMG Data")
        plt.axhline(y = max(inner_buf_clean), color = 'r', linestyle = 'dashed', label = "Max")
        plt.axhline(y = self.inner_threshold, color = 'g', linestyle = 'dashed', label = "Threshold")
        # plot outer muscle EMG readings
        self._make_plot(outer_buf_clean, 4, "Processed Outer EMG Data")
        plt.axhline(y = max(outer_buf_clean), color = 'r', linestyle = 'dashed', label = "Max")
        plt.axhline(y = self.outer_threshold, color = 'g', linestyle = 'dashed', label = "Threshold")
