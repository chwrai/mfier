import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import numpy as np

# main TODO: 
# - emulate realtime audio data from testrecord.py (alternating of two chords)
#

# this file last done:
# - inspected getpolyphoneD return to pass as argument of plotto function

# Get freq and magnitude of first 3 highest harmonics
# using local minimum by differentiation



def getPolyphonD(amps,freqs,Npoly=3):

	length = len(amps)
	diffs = np.zeros(length)
	topfreq = np.zeros(Npoly)
	topamp = np.zeros(Npoly)

	# Differentiate
	for i in range(length):	# amps and freqs are obviously the same length
		if i == range(length)[-1]: # prevent out of bounds for the last diff index
			break
		diffs[i] = (amps[i+1] - amps[i])/(freqs[i+1] - freqs[i])

	# Get respective frequencies
	lastVal = 0
	flag = 0
	for idx,val in enumerate(diffs):
		if val < 0.0 and lastVal > 0.0:
			topfreq[flag] = freqs[idx]
			topamp[flag] = amps[idx]
			flag += 1
		if flag == Npoly:
			break
		lastVal = val

	return (topfreq,topamp, diffs)

def plotto(xsis,ysis,*,diffs=np.array([None])):
	
	fig,ax = plt.subplots()
	ax.plot(xsis,ysis)
	
	# this is plotting for differentiation
	if (diffs[0] != None):
		ax.plot(xsis,diffs)

	ax.grid()
	fig.suptitle("FFT products")
	plt.style.use('classic')
	plt.show()

def mainn():
	N = 2**11 # Number of sample points

	# sample spacing with sampling freq times 2 (at least)
	# to avoid aliasing of measured wave according to nyquist frequency concept
	# 2093.005 being C7, the highest limit of measuring target range
	T = 1.0 / (2*2093.005)
	x = np.linspace(0.0, N*T, N, endpoint=False)
	# x = np.linspace(0.0, 13.6, 8, endpoint=False)
	f1 = 261.626 #c4
	f2 = 330.0   #e4
	f3 = 391.995 #g4
	y = np.sin(f1 * 2.0*np.pi*x) + 0.5*np.sin(f2 *2.0*np.pi*x) + 0.3*np.sin(f3*2.0*np.pi*x)
	
	yf = fft(y)
	fftfrq = fftfreq(N, T)[:N//2] # fftfreq will return symmetrical range of -n to n, thus we split them to half to only get the positive part 
	fftamp = 2.0/N * np.abs(yf[0:N//2])

	print(x)
	print(len(x))
	# getPolyphonD(fftamp,fftfrq)
	# plotto(fftfrq,fftamp,diffs=getPolyphonD(fftamp,fftfrq)[2])

mainn()
