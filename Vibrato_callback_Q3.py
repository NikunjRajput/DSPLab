# simple_wire_gain.py
# Play microphone input to speaker using callback function
#
# Like simple_wire.py, but additionally applies a gain 

import pyaudio
import struct
import time
from myfunctions import clip16
import math



CHANNELS = 1
RATE = 16000        # frames / second
gain = 4.0
DURATION = 10
LEN = RATE
#num_blocks = int(math.floor(LEN/N))

# Vibrato parameters
f0 = 3
W = 0.3
# W = 0 # for no effct

# Create a buffer (delay line) for past values
BUFFER_LEN =  1024                          # Buffer length
buffer = [0.0 for i in range(BUFFER_LEN)]   # Initialize to zero

kr = 0  # read index
kw = int(0.5 * BUFFER_LEN)  # write index (initialize to middle of buffer)
p = 0
# print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))
print 'The buffer is {0:d} samples long.'.format(BUFFER_LEN)
# Number of blocks in wave file


print ('* Playing...')
# Define callback function
def my_callback_fun(input_string, block_size, time_info, status):
    global kr,kw
    # Buffer (delay line) indices
    #print input_string

    N = block_size      # Number of frames
    #print N
    #for n in range(0, num_blocks):
    # Convert string to tuple of numbers
    input_block = struct.unpack('h'*N, input_string)

   
    # Create output (initialize to zero)
    output_value = [0.0 for n in range(0,N)]

    for n in range(0,N):
        #output_block[n] = clip16(gain * input_block[n])
         # Compute output value - time-varying delay, no direct path
        output_value[n] = buffer[int(kr)]  # use int() for integer
        #print input_block[n]
        # Update buffer (pure delay)
        buffer[kw] = input_block[n]

        # Increment read index
        kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n / RATE )
            # Note: kr is not integer!

        # Ensure that 0 <= kr < BUFFER_LEN
        if kr >= BUFFER_LEN:
            # End of buffer. Circle back to front.
            kr = 0

        # Increment write index    
        kw = kw + 1
        if kw == BUFFER_LEN:
            # End of buffer. Circle back to front.
            kw = 0

        # Convert output values to binary string
    output_string = struct.pack('h'*N, *output_value)
    #print output_string

    return (output_string, pyaudio.paContinue)    # Return data and status


# Create audio object
p = pyaudio.PyAudio()

# Open stream using callback
stream = p.open(format = pyaudio.paInt16,       # 16 bits/sample
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                frames_per_buffer = 1024,
                stream_callback = my_callback_fun)

stream.start_stream()
print 'The wire will be on for 6 seconds'
# Keep the stream active for 6 seconds by sleeping here

time.sleep(5)

stream.stop_stream()
stream.close()
p.terminate()

