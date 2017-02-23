# play_wav_mono.py

import pyaudio
import wave
import struct
import math
import sys

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return int(x)
def clip32( x ):    
    # Clipping for 16 bits
    if x > 2147483647:
        x = 2147483647
    elif x < -2147483648:
        x = -2147483648
    else:
        x = x        
    return int(x)
def clip8( x ):    
    # Clipping for 16 bits
    if x > 255:
        x = 255
    elif x < 0:
        x = 0
    else:
        x = x        
    return int(x)    



# gain = 1000
gain = 1


wavfile = 'author.wav'
#wavfile = 'sin01_stereo.wav'
#wavfile = 'sin01_mono.wav'

#print 'Argument 0 is ', sys.argv[0]
#if len ( sys.argv ) > 1:
 #   print 'Argument 1 is ', sys.argv[1]
#wavfile = sys.argv[1]
#print("Play the wave file %s." % wavfile)

# Open wave file (should be mono channel)   
wf = wave.open( wavfile, 'rb' )

# Read the wave file properties
num_channels = wf.getnchannels()       	# Number of channels
RATE = wf.getframerate()                # Sampling rate (frames/second)
signal_length  = wf.getnframes()       	# Signal length
width = wf.getsampwidth()       		# Number of bytes per sample

print("The file has %d channel(s)."            % num_channels)
print("The frame rate is %d frames/second."    % RATE)
print("The file has %d frames."                % signal_length)
print("There are %d bytes per sample."         % width)

p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format      = pyaudio.get_format_from_width(wf.getsampwidth()),
                channels    = num_channels,
                rate        = RATE,
                input       = False,
                output      = True )

# Get first frame
input_string = wf.readframes(1)

if num_channels == 1 :
    if width == 2 :
        while input_string != '':

            # Convert string to number
            input_tuple = struct.unpack('h', input_string)  # One-element tuple
            input_value = input_tuple[0]                    # Number

            # Compute output value
            output_value = clip16(gain * input_value)    # Number

            # Convert output value to binary string
            output_string = struct.pack('h', output_value)  

            # Write binary string to audio stream
            stream.write(output_string)                     

            # Get next frame
            input_string = wf.readframes(1)

        print("**** One channel 16 bit Monofile Done ****")

    if width == 1 :
            while input_string != '':

                # Convert string to number
                input_tuple = struct.unpack('B', input_string)  # One-element tuple
                input_value = input_tuple[0]                    # Number

                # Compute output value
                output_value = clip8(gain * input_value)    # Number

                # Convert output value to binary string
                output_string = struct.pack('B', output_value)  

                # Write binary string to audio stream
                stream.write(output_string)                     

                # Get next frame
                input_string = wf.readframes(1)

            print("**** One channel 8 bit Monofile Done ****")

    if width == 4 :
            while input_string != '':

                # Convert string to number
                input_tuple = struct.unpack('l', input_string)  # One-element tuple
                input_value = input_tuple[0]                    # Number

                # Compute output value
                output_value = clip32(gain * input_value)    # Number

                # Convert output value to binary string
                output_string = struct.pack('l', output_value)  

                # Write binary string to audio stream
                stream.write(output_string)                     

                # Get next frame
                input_string = wf.readframes(1)

            print("**** One channel 4 bit Monofile Done ****")        

elif num_channels == 2 :
    while input_string != '':

        # Convert string to numbers
        input_tuple = struct.unpack('hh', input_string)  # produces a two-element tuple

        # Compute output values
        output_value0 = clip16(gain * input_tuple[0])
        output_value1 = clip16(gain * input_tuple[1])

        # Convert output value to binary string
        output_string = struct.pack('hh', output_value0, output_value1)

        # Write output value to audio stream
        stream.write(output_string)

        # Get next frame
        input_string = wf.readframes(1)

    print("**** Two channel Stereofile Done ****")

stream.stop_stream()
stream.close()
p.terminate()
