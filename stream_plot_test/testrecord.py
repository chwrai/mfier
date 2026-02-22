import queue
import sys

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

# in miliseconds, the minimum period of window,
# for the best performance should be at least larger
# than the period of the lowest detectable wave frequency (in this case, E2: 82hz)  
window = 50 # still not confident so just use the largest possible one (20hz)

device_info = sd.query_devices(kind='input')
samplerate = device_info['default_samplerate'] # mostly 44.1kHz
downsample = 10
plotinterval = 30
channels = 1

mapping = [0]  # Channel numbers start with 1
q = queue.Queue()
frames_legend = [0]
def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata[::downsample], mapping)
    frames_legend[0] = frames


def update_plot(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global plotdata
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])

    legend.get_texts()[0].set_text(f'Frames = {frames_legend[0]}')
    return lines

length = int(window * samplerate / (1000 * downsample))
plotdata = np.zeros((length, channels))
fig, ax = plt.subplots()
lines = ax.plot(plotdata)
ax.axis((0, len(plotdata), -1, 1))
ax.set_yticks([0])
ax.yaxis.grid(True)
ax.tick_params(bottom=False, top=False, labelbottom=False,
               right=False, left=False, labelleft=False)
fig.tight_layout(pad=0)

graph, = plt.plot([], [], color="gold",lw=5,markersize=3,label='Time: 0')
legend = plt.legend(loc=1)

stream = sd.InputStream(
     channels=channels,
    samplerate=samplerate, callback=audio_callback, blocksize=256)
ani = FuncAnimation(fig, update_plot, interval=plotinterval)
with stream:
    plt.show()
