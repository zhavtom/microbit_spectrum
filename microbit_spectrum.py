from microbit import *
import random
import math

N = 8
M = 8
MIC_PIN = pin1 #microphone.sound_level()

buf = [0]*N
spect = [[0j]*N for i in range(M)]

def Wt(x):
    return math.cos(x) - 1j*math.sin(x)
    

def FFT(x):
    n = len(x)
    
    if n == 1:
        return [x[0]]
    
    x_even = x[0:n:2]
    x_odd = x[1:n:2]
    
    X_even = FFT(x_even)
    X_odd = FFT(x_odd)
    
    W = []
    for t in range(n//2):
        W.append(Wt(2*math.pi*t/n))
        
    X = [0]*n
    X[0:N//2] = list(map(lambda x,y: x+y, X_even, list(map(lambda x,y: x*y, W, X_odd))))
    X[N//2:N] = list(map(lambda x,y: x-y, X_even, list(map(lambda x,y: x*y, W, X_odd))))
    
    return X
    
    
def list_mean(array):
    l = [0j]*len(array[0])
    for x in array:
        l = list(map(lambda x,y: x+y, l, x))
    return l
    

def c_abs(x):
    return math.sqrt(x.real**2 + x.imag**2)

def spect_bar(spect):
    l = []
    
    for s in spect:
        x = int(c_abs(s))
        l += [ (x>i*5)*9 for i in range(5) ]
        
    return l
    
def level_bar(x):
    return [ (x>(10-i*2))*9 for i in range(5) ]


while True:
    sleep(0.1)
    buf[0:0] = [MIC_PIN.read_analog()]
    buf.pop(-1)

    spect[0:0] = [FFT(buf)]
    spect.pop(-1)
    
    avg_lvl = min(int(sum(buf)/N), 45)
    avg_spect = list_mean(spect)

    level_meter = level_bar(avg_lvl) + spect_bar([i/3+1 for i in avg_spect][1:4*N//8+1:N//8])

    display.show(Image(5, 5, bytearray(level_meter)))