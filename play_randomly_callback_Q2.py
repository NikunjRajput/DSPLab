

import pyaudio
import struct
from math import sin, cos, pi
import random
from myfunctions import clip16
import time
# import numpy as np

BLOCKSIZE = 1024    # Number of frames per block
WIDTH = 2           # Bytes per sample
CHANNELS = 1
RATE = 8000         # Sampling rate in Hz

# Parameters
T = 10      # Total play time (seconds)
Ta = 0.4    # Decay time (seconds)
f1 = 350    # Frequency (Hz)

# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
om1 = 2.0 * pi * float(f1)/RATE

# Filter coefficients (second-order IIR)
a1 = -2*r*cos(om1)
a2 = r**2
b0 = sin(om1)

NumBlocks = T * RATE / BLOCKSIZE

y = [0 for i in range(BLOCKSIZE)]
print 'Playing for {0:f} seconds ...'.format(T),

# Define callback function
def my_callback_fun(input_string, block_size, time_info, status):

    

    THRESHOLD = 2.5 / RATE          # For a rate of 2.5 impulses per second

    # Loop through blocks
    for i in range(0, NumBlocks):

    # Do difference equation for block
        for n in range(BLOCKSIZE):

            rand_val = random.random()
            if rand_val < THRESHOLD:
                x = 15000
            else:
                x = 0

            y[n] = b0 * x - a1 * y[n-1] - a2 * y[n-2]  
                  # What happens when n = 0?
                  # In Python negative indices cycle to end, so it works..

            y[n] = clip16(y[n])

    # If numpy is available, then clipping can be done using:
    # y = np.clip(y, -32000, 32000)

    # Convert numeric list to binary string
    data = struct.pack('h' * BLOCKSIZE, *y);


    return (data, pyaudio.paContinue)    # Return data and status


# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = False,
                output = True,
                stream_callback = my_callback_fun)

#stream.start_stream()
# Keep the stream active for 6 seconds by sleeping here
time.sleep(6.0)


    # Write binary string to audio output stream
    #stream.write(data, BLOCKSIZE)

print 'Done.'

stream.stop_stream()
stream.close()
p.terminate()
