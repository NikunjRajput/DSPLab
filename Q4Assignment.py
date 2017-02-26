# play_randomly_plots.py
"""
PyAudio Example: Generate random pulses and input them to an IIR filter of 2nd order.
It sounds like pings from a Sonar.
"""

import pyaudio
import struct
import random
from math import sin, pi
from matplotlib import pyplot as plt
from myfunctions import clip16
import numpy as np


N = 1
WIDTH = 2           # Bytes per sample
CHANNELS = 1
RATE = 8000         # Sampling rate in Hz\
f3 = 200

T = 1000

y = [0 for i in range(T/N)]
#plt.close('all')
#plt.ion()           # Turn on interactive mode so plot gets updated
fig = plt.figure()
f1 = fig.add_subplot(2,1,1)
xtime = [t for t in range(T/N)]
f1.set_ylim(-2, 2)
f1.set_xlim(0, T/N)
f1.set_xlabel('Time (n)')
line1, = f1.plot(xtime,y)
line1.set_xdata(xtime)

f2 = fig.add_subplot(2,1,2)
xfrequency = [n*float(RATE)*N/T for n in range(T/N)]
f2.set_xlim(0, RATE/2.0)
f2.set_ylim(0,100)
f2.set_xlabel('Frequency(Hz)')
line2, = f2.plot([], [], color = 'blue')
line2.set_xdata(xfrequency)

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = False,
                output = True)

print 'Playing for {0:f} seconds ...'.format(T/RATE)

Num_blocks = int(T*RATE/.5)
for t in range(0, Num_blocks):

	om1 = 2 * pi * float(f3)*t*t/RATE+400*pi*t
	#phi = 2*pi*float(f3)/RATE + pi*t*t*400
	#phi1 = phi + 2*pi*300*t*t/RATE
	y[t] = sin(om1)
	output_string = struct.pack('h'*1000,*y)
	line1.set_ydata(y)
	Y = np.fft.fft(y)
	line2.set_ydata(abs(Y))
	f1.set_title('time = {0:d}'.format(t))
	plt.pause(0.01)
	stream.write(output_string)	
	#y[t] = sin(phi)


plt.show()
print 'Done.'
stream.stop_stream()
stream.close()
p.terminate()
