from math import cos, pi 
import pyaudio
import struct

# 16 bit/sample

# Fs : Sampling frequency (samples/second)
Fs = 8000
# Fs = 16000
# Fs = 32000
# Try Fs = 16000 and 32000 
# Fs = 32000

T = 1       # T : Duration of audio to play (seconds)
N = T*Fs    # N : Number of samples to play

# Difference equation coefficients
a1 = -1.8999
a2 = 0.9977
b1 = -1.8999
b2 = 0.9977

# Initialization
y1 = 0.0
y2 = 0.0
c1 = 0.0
c2 = 0.0
# gain = 1000.0
gain = 10000.0

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,  
                channels = 1, 
                rate = Fs,
                input = False, 
                output = True)

for n in range(0, N):

    # Use impulse as input signal
    if n == 0:
        x0 = 1.0
    else:
        x0 = 0.0

    # Difference equation
    y0 = x0 - a1 * y1 - a2 * y2

    # Delays
    y2 = y1
    y1 = y0

    b0 = y0 - b1 * c1 - b2 * c2

    b2 = b1
    b1 = b0 
    # Output
    out = gain * b0
    str_out = struct.pack('h', out)     # 'h' for 16 bits
    stream.write(str_out)

print("* done *")

stream.stop_stream()
stream.close()
p.terminate()
