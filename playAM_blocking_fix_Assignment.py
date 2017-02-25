# playAM_blocking_fix.py
# Play a mono wave file with amplitude modulation. 
# This implementation reads and plays a block at a time (blocking)
# and corrects for block-to-block angle mismatch.
# Assignment: modify this file so it works for both mono and stereo wave files
#  (where does this file have an error when wave file is stereo and why? )

# f0 = 0      # Normal audio
f0 = 400    # 'Duck' audio
f1 = 9000
BLOCKSIZE = 64      # Number of frames per block

import pyaudio
import struct
import wave
import math
FORMAT = pyaudio.paInt16
# Open wave file (mono)
#wave_file_name = 'author.wav'
wave_file_name = 'sin01_stereo.wav'
# wave_file_name = 'sin01_mono.wav'
# wave_file_name = 'sin01_stereo.wav'
wf = wave.open(wave_file_name, 'rb')
RATE = wf.getframerate()
WIDTH = wf.getsampwidth()
LEN = wf.getnframes() 
CHANNELS = wf.getnchannels() 

print 'The sampling rate is {0:d} samples per second'.format(RATE)
print 'Each sample is {0:d} bytes'.format(WIDTH)
print 'The signal is {0:d} samples long'.format(LEN)
print 'The signal has {0:d} channel(s)'.format(CHANNELS)

output_wavefile = wave_file_name[:-4] + '_AM_fix.wav'
output_wf = wave.open(output_wavefile, 'w')      # wave file
output_wf.setframerate(RATE)
output_wf.setsampwidth(WIDTH)
output_wf.setnchannels(CHANNELS)

# Open audio stream
p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = 2,
                rate = RATE,
                input = False,
                output = True)

# Create block (initialize to zero)
output_block_left = [0 for n in range(0, BLOCKSIZE)]
output_block_right = [0 for n in range(0, BLOCKSIZE)]

# Number of blocks in wave file
num_blocks = int(math.floor(LEN/BLOCKSIZE))

# Initialize angle
theta = 0.0
theta1 = 0.0

# Block-to-block angle increment
theta_del = (float(BLOCKSIZE*f0)/RATE - math.floor(BLOCKSIZE*f0/RATE)) * 2.0 * math.pi
theta_del1 = (float(BLOCKSIZE*f0)/RATE - math.floor(BLOCKSIZE*f1/RATE)) * 2.0 * math.pi

print('* Playing...')

# Go through wave file 
for i in range(0, num_blocks):

    # Get block of samples from wave file
    input_string = wf.readframes(BLOCKSIZE)     # BLOCKSIZE = number of frames read

    # Convert binary string to tuple of numbers    
    input_tuple = struct.unpack('hh' * BLOCKSIZE, input_string)
    # print input_tuple
    count = 0 
    input_tuple_left = []
    input_tuple_right = []
    frames = []
    for item in input_tuple:
        if(count % 2 == 0):
            input_tuple_left.append(item)
        else:
            input_tuple_right.append(item)
        count = count + 1

    # print input_tuple_left  
                  # Number
    
    # print input_tuple_right
            # (h: two bytes per sample (WIDTH = 2))

    # Go through block
    for n in range(0, BLOCKSIZE/2):
        # Amplitude modulation  (f0 Hz cosine)
        output_block_left[n] = input_tuple_left[n] * math.cos(2*math.pi*n*f0/RATE + theta)
        output_block_right[n] = input_tuple_right[n] * math.cos(2*math.pi*n*f1/RATE + theta1)
        output_string = (struct.pack('hh' , output_block_left[n], output_block_right[n]))
        #frames.append(output_string)
        stream.write(output_string)
        output_wf.writeframes(output_string)
        # output_block[n] = input_tuple[n] * 1.0  # for no processing
    # print output_block_left
    # Set angle for next block
        theta = theta + theta_del
        theta1 = theta1 + theta_del1

    

    

    # output_string = struct.pack('hh', output_block_right,output_string_left)

    # Write binary string to audio output stream
    # 
        

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()


# Original file by Gerald Schuller, October 2013
