# play_wav_mono.py

import pyaudio
import wave
import struct
import math
import cmath

from myfunctions import clip16

wavfile = 'author.wav'
# wavfile = 'sin01_mono.wav'
#wavfile = 'sin01_stereo.wav'

print("Play the wave file %s." % wavfile)

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

t = signal_length/RATE
I = cmath.sqrt(1);
s0 = cmath.exp( I * 0.5 * math.pi * 0 );
s1 = cmath.exp( I * 0.5 * math.pi * 1 );
s2 = cmath.exp( I * 0.5 * math.pi * 2 );
s3 = cmath.exp( I * 0.5 * math.pi * 3 );
s4 = cmath.exp( I * 0.5 * math.pi * 4 ); 

# Difference equation coefficients
b0 =  0.008442692929081 * s0
b2 = -0.016885385858161 * s2
b4 =  0.008442692929081 * s4

# a0 =  1.000000000000000
a1 = -3.580673542760982 * s1
a2 =  4.942669993770672 * s2
a3 = -3.114402101627517 * s3
a4 =  0.757546944478829 * s4


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
stream = p.open(format      = pyaudio.paInt16,
                channels    = num_channels,
                rate        = RATE,
                input       = False,
                output      = True )


# Get first frame
input_string = wf.readframes(1)

while input_string != '':

    # Convert string to number
    input_tuple = struct.unpack('h', input_string)[0] # One-element tuple
    #input_value_left = input_tuple[0]                    # Number
    #input_value_right = input_tuple[1]

    # Set input to difference equation
    x0 = input_tuple
    #r = filter[a1,b0,x0]

    # Difference equation
    y0 = b0*x0 + b2*x2 + b4*x4 - a1*y1 - a2*y2 - a3*y3 - a4*y4 
    #yy0 = bb0*xx0 + bb2*xx2 + bb4*xx4 - aa1*yy1 - aa2*yy2 - aa3*yy3 - aa4*yy4

    f1 = 400;           #% Modulation frequency

    g = y0 * (cmath.exp( I * 2 * math.pi * f1 * t ));

    y = real(g);

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
    #output_value_left = clip16(xx0)    # Number
    output_value = clip16(y0)    # Number


    # Convert output value to binary string
    output_string = struct.pack('h', output_value)  

    # Write binary string to audio stream
    stream.write(output_string)                     

    # Get next frame
    input_string = wf.readframes(1)

print("**** Done ****")

stream.stop_stream()
stream.close()
p.terminate()
