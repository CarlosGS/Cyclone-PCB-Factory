
import sys

import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from matplotlib import cm

import pickle # For file saving

# Misc functions:

def saveToFile(data,path):
    with open(path, 'wb') as path_file:
        ret = pickle.dump(data, path_file, protocol=2)
        path_file.close()
        return ret
    raise Exception("Could not save " + path)

def loadFromFile(path):
    with open(path, 'rb') as path_file:
        ret = pickle.load(path_file)
        path_file.close()
        return ret
    raise Exception("Could not load " + path)


def pltShowNonBlocking():
	#plt.ion() # Enable real-time plotting to avoid blocking behaviour for plt.show()
	plt.draw()
	#plt.ioff() # Disable real-time plotting

def pltNewFig():
	fig = plt.figure()
	#plt.draw()
	return fig

def pltSetFig(fig):
	plt.figure(fig.number)

def pltRefresh(fig):
	fig.canvas.draw()

def pltShow():
	#plt.ion() # IMPORTANT: Enable real-time plotting
	plt.draw()
	#plt.ioff()

