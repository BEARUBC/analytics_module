import numpy as np
import logging
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def plot_emg_data(buffers):
    """Plots current EMG readings -- TODO: @krarpit make real-time"""    
    inner_buf, outer_buf = buffers
    time_buf = np.array([i/1000 for i in range(0, len(inner_buf), 1)]) # sampling rate 1000 Hz

    # for inner_buf
    fig = plt.figure()
    plt.plot(time_buf, inner_buf)
    plt.xlabel('Time (sec)')
    plt.ylabel('EMG (a.u.)')
    fig_name = 'graphs/fig_inner_emg.png'
    fig.set_size_inches(w=11,h=7)
    fig.savefig(fig_name)
    logger.info("Saved latest inner-muscle EMG visualization.")

    # for outer_buf
    fig = plt.figure()
    plt.plot(time_buf, outer_buf)
    plt.xlabel('Time (sec)')
    plt.ylabel('EMG (a.u.)')
    fig_name = 'graphs/fig_outer_emg.png'
    fig.set_size_inches(w=11,h=7)
    fig.savefig(fig_name)
    logger.info("Saved latest outer-muscle EMG visualization.")
    