# playAM_blocking.py
# Play a wave file with amplitude modulation. 
# Assumes wave file is mono.
# This implementation reads and plays a block at a time (blocking).
# Assignment: modify file so it works for both mono and stereo wave files
#  (where does this file have an error when wave file is stereo and why? )
"""
Read a signal from a wave file, do amplitude modulation, play to output
Original: pyrecplay_modulation.py by Gerald Schuller, Octtober 2013
Modified to read a wave file - Ivan Selesnick, September 2015
Modified to work for mono and stereo file using STFT - Nikunj Rajput, December 2016
"""

import pyaudio
import struct
import wave
import math
import numpy as np
import cmath
from myfunctions import clip16

# f0 = 0      # Normal audio
#f0 = 400    # 'Duck' audio

BLOCKSIZE = 512      # Number of frames per block
Nfft = 1024


# Open wave file (mono)
input_wavefile = 'author.wav'
# input_wavefile = 'sin01_mono.wav'
# input_wavefile = 'sin01_stereo.wav'
wf = wave.open( input_wavefile, 'rb')
RATE = wf.getframerate()
WIDTH = wf.getsampwidth()
LEN = wf.getnframes() 
CHANNELS = wf.getnchannels() 
print LEN

print 'The sampling rate is {0:d} samples per second'.format(RATE)
print 'Each sample is {0:d} bytes'.format(WIDTH)
print 'The signal is {0:d} samples long'.format(LEN)
print 'The signal has {0:d} channel(s)'.format(CHANNELS)

# Open audio stream
p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = 1,
                rate = RATE,
                input = False,
                output = True)


Nx = BLOCKSIZE + LEN + BLOCKSIZE
num_blocks = int(2*Nx/BLOCKSIZE)+1-1
L = BLOCKSIZE/2 * (num_blocks + 1)
t = 0 


# Create block (initialize to zero)
output_block = [0 for n in range(0, BLOCKSIZE)]

# Number of blocks in wave file
# num_blocks = int(math.floor(LEN/BLOCKSIZE))

print('* Playing...')

# Go through wave file 
input_string = wf.readframes(LEN)     # BLOCKSIZE = number of frames read

    # Convert binary string to tuple of numbers    
input_tuple = struct.unpack('h' * LEN, input_string)
for i in range(0, num_blocks):

    # Get block of samples from wave file
    #input_string = wf.readframes(LEN)     # BLOCKSIZE = number of frames read

    # Go through block
    for n in range(0, BLOCKSIZE):
        p = n - 0.5

        # Amplitude modulation  (f0 Hz cosine)
        #print math.cos(math.pi*p/BLOCKSIZE-math.pi/2)
        
        output_block[n] = input_tuple[n+t] * math.cos(math.pi*p/BLOCKSIZE-math.pi/2)
        #print output_block[n]
        
        # output_block[n] = input_tuple[n] * 1.0  # for no processing
      
    #X =  np.arange(output_block)
    t =  t + BLOCKSIZE/2
    X = np.fft.fft(output_block)
    
    
    X = abs(X)
   
    for n in range(0, BLOCKSIZE):
        X[n] = clip16(X[n])
    #print X

    # Convert values to binary string
    #X = np.fft.fft(output_block)
    output_string = struct.pack('h' * BLOCKSIZE, *X)
    
    #X= real(X)
    t = t + BLOCKSIZE/2

    # Write binary string to audio output stream
    stream.write(output_string)

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()
