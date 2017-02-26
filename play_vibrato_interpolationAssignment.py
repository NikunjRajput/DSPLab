# play_vibrato_ver2.py
# Reads a specified wave file (mono) and plays it with a vibrato effect.
# (Sinusoidal time-varying delay)
# This implementation uses a circular buffer with two buffer indices.
# Uses linear interpolation



BLOCKSIZE = 64
import pyaudio
import wave
import struct
import math
from myfunctions import clip16

# TRY BOTH WAVE FILES
#wavfile = 'author.wav'
wavfile= 'sin01_stereo.wav'
# wavfile = 'decay_cosine_mono.wav'
# wavfile = 'sin01_mono.wav'
#print 'Play the wave file: {0:s}.'.format(wavfile)

# Open wave file
wf = wave.open( wavfile, 'rb')

# Read wave file properties

CHANNELS = wf.getnchannels()        # Number of channels
RATE = wf.getframerate()            # Sampling rate (frames/second)
LEN  = wf.getnframes()              # Signal length
WIDTH = wf.getsampwidth()           # Number of bytes per sample

#WIDTH = 2           # bytes per sample
#CHANNELS = 2       # mono
#RATE = 8000
DURATION = 1     # Duration in seconds

#print('The file has %d channel(s).'         % CHANNELS)
#print('The file has %d frames/second.'      % RATE)
#print('The file has %d frames.'             % LEN)
#print('The file has %d bytes per sample.'   % WIDTH)

# Vibrato parameters
f0 = 2
W = 0.2
f0R = 400
WR = 100

# W = 0 # for no effct

# f0 = 10
# W = 0.2

# OR
# f0 = 20
# ratio = 1.06
# W = (ratio - 1.0) / (2 * math.pi * f0 )
# print W

# Create a buffer (delay line) for past values
buffer_MAX =  1024                          # Buffer length
buffer = [0.0 for i in range(buffer_MAX)]   # Initialize to zero



# print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))
print 'The buffer is {0:d} samples long.'.format(buffer_MAX)


# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = p.get_format_from_width(WIDTH),
                channels    = 2,
                rate        = RATE,
                input       = False,
                output      = True)

#output_all = ''            # output signal in all (string)

output_value_left = [0 for n in range(0, BLOCKSIZE/2)]
output_value_right = [0 for n in range(0, BLOCKSIZE/2)]

# Number of blocks in wave file
#num_blocks = int(math.floor(LEN/BLOCKSIZE))
num_blocks = int( DURATION * RATE / BLOCKSIZE )
print ('* Playing...')

# Loop through wave file 
for n in range(0, num_blocks):
	kr = 0  # read index
	kw = int(0.5 * buffer_MAX)  # write index (initialize to middle of buffer)
	kw = buffer_MAX/2

	# Buffer (delay line) indices
	krR = 0  # read index
	kwR = int(0.5 * buffer_MAX)  # write index (initialize to middle of buffer)
	kwR = buffer_MAX/2
    # Get sample from wave file
	#input_string = stream.read(BLOCKSIZE)
	input_string = wf.readframes(BLOCKSIZE)
	#print input_string
    # Convert string to number
	input_value = struct.unpack('hh' * BLOCKSIZE, input_string)
    #input_value_Left = input_value[0]                    # Number
    #input_value_right = input_value[1]

	count = 0 
	input_value_left = []
	input_value_right = []
	frames = []
	for item in input_value:
		if(count % 2 == 0):
			input_value_left.append(item)

		else:
			input_value_right.append(item)
		count = count + 1

    
      
    
	for n in range(0, (BLOCKSIZE/2)-1):
    	# Get previous and next buffer values (since kr is fractional)
		kr_prev = int(math.floor(kr))               
		kr_next = kr_prev + 1
		frac = kr - kr_prev    # 0 <= frac < 1
		if kr_next >= buffer_MAX:
			kr_next = kr_next - buffer_MAX

		kr_prevR = int(math.floor(krR))               
		kr_nextR = kr_prevR + 1
		fracR = krR - kr_prevR    # 0 <= frac < 1
		if kr_nextR >= buffer_MAX:
			kr_nextR = kr_nextR - buffer_MAX  
    # Compute output value using interpolation
		output_value_left[n] = input_value[2*n] + ((1-frac) * buffer[kr_prev] + frac * buffer[kr_next])
		output_value_right[n] = input_value[2*n+1] + ((1-fracR) * buffer[kr_prevR] + fracR * buffer[kr_nextR])  
		output_string = (struct.pack('hh' , output_value_left[n], output_value_right[n]))
		stream.write(output_string,BLOCKSIZE)
       # Update buffer (pure delay)
		buffer[kw] = input_value_left
		buffer[kwR] = input_value_right
       #stream.write(output_string)
    	#output_wf.writeframes(output_string)
    
    #print output_value_left
    

    	# Increment read index
		kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n / RATE )
		krR = krR + 1 + WR * math.sin( 2 * math.pi * f0R * n / RATE )
	    
        # Note: kr is fractional (not integer!)

	    # Ensure that 0 <= kr < buffer_MAX
		if kr >= buffer_MAX:
	        # End of buffer. Circle back to front.
			kr = 0
	    # Ensure that 0 <= kr < buffer_MAX
		if krR >= buffer_MAX:
	        # End of buffer. Circle back to front.
			krR = 0

	    # Increment write index    
		kw = kw + 1
		if kw == buffer_MAX:
	        # End of buffer. Circle back to front.
			kw = 0

	    # Increment write index    
		kwR = kwR + 1
		if kwR == buffer_MAX:
	        # End of buffer. Circle back to front.
			kwR = 0    

    # Clip and convert output value to binary string
    #output_string = struct.pack('h', clip16(output_value))

    #output_string = struct.pack('hh', clip16(output_value_left),clip16(output_value_right))


    # Write output to audio stream
    #stream.write(output_string)

    #output_all = output_all + output_string     # append new to total

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()


#output_wavefile = wavfile[:-4] + '_vibratoAss.wav'
#print 'Writing to wave file', output_wavefile
#wf = wave.open(output_wavefile, 'w')      # wave file
#wf.setnchannels(2)      # one channel (mono)
#wf.setsampwidth(2)      # two bytes per sample
#wf.setframerate(RATE)   # samples per second
#wf.writeframes(output_all)
#wf.close()
print('* Done')

