import pylab
import pyaudio
import struct
import sys
import numpy as np
import wave
import pygame


def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return int(x)

def clip16_warning( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
        print 'positive clipping'
    elif x < -32768:
        x = -32768
        print 'negative clipping'
    else:
        x = x        
    return int(x)

def time_scale(tscale,output_wavefile):
    N = 2048
    H = N/4
    print ('c')
    wavfile = 'demo.wav'
    wf = wave.open( wavfile, 'rb')
    RATE = wf.getframerate()
    WIDTH = wf.getsampwidth()
    #wavfile = sys.argv[1]
    # read input and get the timescale factor
    signalin  = wf.getnframes()
    #(sr,signalin) = wavfile.readframes(sys.argv[2])

    L = signalin
    print L
    #tscale = 3
    # signal blocks for processing and output
    phi  = pylab.zeros(N)
    out = pylab.zeros(N, dtype=complex)
    out1 = pylab.zeros(N, dtype=complex)
    sigout = pylab.zeros(L/tscale+N, dtype = complex)
    sigout1 = pylab.zeros(L/tscale+N, dtype = complex)
    sigout2 = pylab.zeros(L/tscale+N, dtype = complex)
    input_string = wf.readframes(L)
    input_value1 = struct.unpack('h' * L, input_string)
    # max input amp, window
    amp = max(input_value1)
    win = pylab.hanning(N)
    p = 0
    pp = 0
    

    p1 = pyaudio.PyAudio()
    stream = p1.open(format = p1.get_format_from_width(WIDTH),
                    channels = 1,
                    rate = RATE,
                    input = False,
                    output = True)
    output_all = ''            # output signal in all (string)

    while p < L-(N+H):
        #print N
        # take the spectra of two consecutive windows
        p1 = int(p)

        
        #win = list(win)
        #print input_value[p1:p1+N]
        input_value = np.asarray(input_value1)
        
        #print input_value
        
        spec1 =  np.fft.fft(win*input_value[p1:p1+N])
        spec2 =  np.fft.fft(win*input_value[p1+H:p1+N+H])
        spec3 = abs(spec2)


        
        # take their phase difference and integrate

        #phi += (angle(spec2) - angle(spec1))
        phi = (phi + np.angle(spec2/spec1)) % 2 * (np.pi)
        out = np.fft.ifft(spec3*np.exp(1j*phi))
        for i in range(0,N):
            out.real[i] = clip16(out.real[i])
        
        
        print('* e')  
        sigout[pp:pp+N] += win*out
        #print out
        #print sigout
        #sigout = sigout/sigout.max()
        #print sigout
        B = len(sigout)
        #sigout1 = ((sigout/amp))
        #sigout2 =  abs(sigout1)
        #sigout = tuple(sigout.real)
        #sigout  = sigout.real
        #sigout = list(sigout)
        output_string = struct.pack('h' * N, *(out.real))

        pp += H
        p += H*tscale

        print('* D')  

        # Write output value to audio stream
        #stream.write(output_string)
        output_all = output_all + output_string
    print('* Done')

    stream.stop_stream()
    stream.close()
    #p1.terminate()
    output_wavefile = wavfile[:-4] + str(time_scale) + '_vibrato.wav'
   
    print 'Writing to wave file', output_wavefile

    wf = wave.open(output_wavefile, 'w')      # wave file
    print('* hip')
    wf.setnchannels(1)      # one channel (mono)
    wf.setsampwidth(2)      # two bytes per sample
    wf.setframerate(RATE)   # samples per second
    print('* hop')
    wf.writeframes(output_all)

    wf.close()
    pygame.mixer.music.load(output_wavefile)

    pygame.mixer.music.play(-1)
    print('* Done')      




#def pitch(tscale,output_wavefile, filecount):
#    n = 4
#    pitchfactor = 2**(1.0*n/12.0)
#    pitchf = time_scale(1.0/pitchfactor, output_wavefile, filecount)
