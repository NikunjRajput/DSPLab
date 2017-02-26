# plot_micinput_spectrum.py

"""

    Using Pyaudio, get audio input and plot real-time FFT of blocks.
    Modified - Nikunj Rajput, October 2016
    Modified - Ivan Selesnick, October 2015
    Based on program by Gerald Schuller
    """

import scipy
from scipy import signal
import pyaudio
import struct
from matplotlib import pyplot as plt
from scipy.signal import filter_design as fd
import numpy as np
import pylab
import math



plt.ion()           # Turn on interactive mode so plot gets updated

from myfunctions import clip16

WIDTH = 2           # Number of bytes per sample
CHANNELS = 1        # mono
RATE = 16000        # Sampling rate (frames/second)
DURATION = 10        # duration of processing (seconds)

N = DURATION*RATE   # N : Number of samples to process

print 'Running for ', DURATION, 'seconds...'

plt.figure(1)
plt.ylim(0, 10*RATE)

# plt.xlim(0, BLOCKSIZE/2.0)         # set x-axis limits
# plt.xlabel('Frequency (k)')
# f = np.linspace(0, BLOCKSIZE-1, BLOCKSIZE)

# # Time axis in units of milliseconds:
plt.xlim(0, RATE/2.0)         # set x-axis limits
plt.xlabel('Frequency (Hz)')
f = [n*float(RATE/1024) for n in range(1024)]

line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(f)                         # x-data of plot (frequency)
plt.pause(.01)
plt.show()




# Difference equation coefficients
b0 =  0.008442692929081
b2 = -0.016885385858161
b4 =  0.008442692929081

# a0 =  1.000000000000000
a1 = -3.580673542760982
a2 =  4.942669993770672
a3 = -3.114402101627517
a4 =  0.757546944478829


# Initialization
x1 = 0.0
x2 = 0.0
x3 = 0.0
x4 = 0.0
y1 = 0.0
y2 = 0.0
y3 = 0.0
y4 = 0.0


p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True)

print "******Recording******"



for n in range(0, N):
    
    # Get one frame from audio input (microphone)
    input_string = stream.read(1)
    
    # Convert binary string to tuple of numbers
    input_tuple = struct.unpack('h', input_string)
    
    
    # Convert one-element tuple to number
    input_value = input_tuple[0]
    
    X = np.fft.fft(input_tuple)
    plt.figure(1)
    line.set_ydata(abs(X))                               # Update y-data of plot
    #plt.subplot(2, 1, 1)
    plt.show()
    plt.draw()
    plt.pause(1)
    plt.close()

    
    # Set input to difference equation
    x0 = input_value
    
    # Difference equation
    y0 = b0*x0 + b2*x2 + b4*x4 - a1*y1 - a2*y2 - a3*y3 - a4*y4
    
    # Delays
    x4 = x3
    x3 = x2
    x2 = x1
    x1 = x0
    y4 = y3
    y3 = y2
    y2 = y1
    y1 = y0
    
    
    # Compute output value
    output_value_left = clip16(x0)    # Number
    output_value_right = clip16(y0)    # Number
    Y = np.fft.fft(output_value_right)
    plt.figure(2)
    line.set_ydata(abs(Y))                               # Update y-data of plot
    #plt.subplot(2, 1, 2)
    plt.show()
    plt.draw()
    plt.pause(1)
    plt.close()
    
    # Convert output value to binary string
    output_string = struct.pack('hh', output_value_left,output_value_right)
    
    # Write binary string to audio stream
    stream.write(output_string)
    
    # Get next frame
    input_string = wf.readframes(1)




print "******Done******"


stream.stop_stream()
stream.close()
p.terminate()

print '* Done'
