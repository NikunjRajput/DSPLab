# record2wave_stereo
"""
Record stereo input (mics) to wave file.
"""

import pyaudio
import struct
import math
import wave

filename = 'record2wave_stereo_output.wav'

# RATE = 32000        # Sampling rate (frames/second)
RATE = 48000
# RATE = 96000
# RATE = 48000  
CHANNELS = 2        # Stereo
BLOCKSIZE = 1024    # Number of frames in a block
WIDTH = 2           # Number of bytes per sample
RECORD_SECONDS = 4  # Duration of recording

# Open wave file
wf = wave.open(filename, 'w')
wf.setnchannels(CHANNELS)
wf.setsampwidth(WIDTH)
wf.setframerate(RATE)

p = pyaudio.PyAudio()

number_of_devices = p.get_device_count()
print('There are {0:d} devices'.format(number_of_devices))

property_list = ['defaultSampleRate', 'maxInputChannels', 'maxOutputChannels']
for i in range(0, number_of_devices):
    print('Device {0:d} has:'.format(i))
    for s in property_list:
        print ' ', s, '=', p.get_device_info_by_index(i)[s]

# FPB: Frames per buffer - affects latency.
# Small value for FPB (e.g. 256) gives low latency
# Large value for FPB (e.g. 2**14) gives high latency
# FPB = 256
# FPB = 512
FPB = 1024
# FPB = 2**12
# FPB = 2**14

stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                frames_per_buffer = FPB)

# Create output buffer
samples = [0 for i in range(0, CHANNELS * BLOCKSIZE)]

print('* Recording for {0:.3f} seconds'.format(RECORD_SECONDS))

# Start loop
for i in range(0, int(RATE / BLOCKSIZE * RECORD_SECONDS)):

    # Get frames from audio input stream
    input_string = stream.read(BLOCKSIZE)   # BLOCKSIZE = number of frames read

    # Convert binary string to tuple of numbers
    input_tuple = struct.unpack('h' * CHANNELS * BLOCKSIZE, input_string);    # WIDTH = 2
    # input_tuple = struct.unpack('i' * CHANNELS * BLOCKSIZE, input_string);      # WIDTH = 4
   
    # Loop through the samples
    for n in range(0, CHANNELS * BLOCKSIZE, CHANNELS):    # increment by 2 for stereo (1 for mono)
        # No processing (stereo):
        samples[n] = input_tuple[n]           # channel 0 (left)
        samples[n+1] = input_tuple[n+1]       # channel 1 (right)
        # OR
        # Amplitude modulation (stereo):
        # samples[n] = input_tuple[n] * math.cos(math.pi*n*f0/RATE);      # channel 0 (left)
        # samples[n+1] = input_tuple[n+1] * math.cos(math.pi*n*f1/RATE);  # channel 1 (right)

    # convert samples to binary string
    output_string = struct.pack('h' * CHANNELS * BLOCKSIZE, *samples)       # WIDTH = 2
    # output_string = struct.pack('i' * CHANNELS * BLOCKSIZE, *samples)       # WIDTH = 4

    # Write samples to audio output stream
    # stream.write(output_string)

    # Write to wave file
    wf.writeframes(output_string)

print("* Done")

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()

# Close wave file
wf.close()
