import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

import numpy as np
from numpy import random

from numpy import genfromtxt

import matplotlib.cm as cm

error = 0.003

matchArray = genfromtxt('0_threeBestNoiseless.csv', skip_header = 1, encoding = None, delimiter = ',', dtype = None)
fig, ax1 = plt.subplots()
ogData = genfromtxt('0_noise removed.csv', skip_header = 8, encoding = None, delimiter = ',', dtype = float)
a = ogData[:,0]
b = ogData[:,1]

bars = ax1.bar(a, b, 0.001, picker=True)
ax2 = ax1.twinx()
ax2.set_navigate(False)
ax1.set_xlabel('Intensity')
ax1.set_ylabel('Mass')

# set default color
for bar in bars:
    bar.set_color('b')

# returns the base formula from the matched one
def baseFormula(wholeFormula):
    i = wholeFormula.find("+")
    if i > -1:
        return wholeFormula[:i]
    else:
        return wholeFormula

def findError(wholeFormula):
    i = wholeFormula.find(":")
    if i > -1:
        return (error - abs(float(wholeFormula[i+1:])))* 5000
    else:
        return 0

baseFormulas = []
colors = []
colorIntensity = []
ymin, ymax = ax2.get_ylim()
xA = []
xB = []
xC = []
clrsA = []
clrsB = []
clrsC = []
sizeA = []
sizeB = []
sizeC = []
for form in matchArray:
    c = 0
    if not (baseFormula(str(form[1])) in baseFormulas):
        baseFormulas.append(baseFormula(str(form[1])))
        colors.append(np.random.rand(3,))
        colorIntensity.append(form[0])
        c = len(colors) - 1
    else:
        c = baseFormulas.index(baseFormula(str(form[1])))
        colorIntensity[c] += form[0]
    xA.append(form[0])
    clrsA.append(c)
    sizeA.append(findError(form[1]))

    if not form[2] == 0:
        if not (baseFormula(str(form[2])) in baseFormulas):
            baseFormulas.append(baseFormula(str(form[2])))
            colors.append(np.random.rand(3,))
            colorIntensity.append(form[0])
            c = len(colors) - 1
        else:
            c = baseFormulas.index(baseFormula(str(form[2])))
            colorIntensity[c] += form[0]
        xB.append(form[0])
        clrsB.append(c)
        sizeB.append(findError(form[2]))
    if not form[3] == 0:
        if not (baseFormula(str(form[3])) in baseFormulas):
            baseFormulas.append(baseFormula(str(form[3])))
            colors.append(np.random.rand(3,))
            colorIntensity.append(form[0])
            c = len(colors) - 1
        else:
            c = baseFormulas.index(baseFormula(str(form[3])))
            colorIntensity[c] += form[0]
        xC.append(form[0])
        clrsC.append(c)
        sizeC.append(findError(form[3]))
    
yA = np.empty(len(xA))
yA.fill(1)
yB = np.empty(len(xB))
yB.fill(2)
yC = np.empty(len(xC))
yC.fill(3)

largest = np.amax(colorIntensity)

for i in range(len(colors)):
    colors[i] = cm.hot(1.0 - (float(colorIntensity[i])/float(largest)))

colorsA = []
colorsB = []
colorsC = []

for i in clrsA:
    colorsA.append(colors[i])
for i in clrsB:
    colorsB.append(colors[i])
for i in clrsC:
    colorsC.append(colors[i])

print yA
mew = 1
ec = 'k'

ax2.scatter(xA, yA, c = colorsA, s = sizeA, edgecolors = ec, linewidth = mew)
ax2.scatter(xB, yB, c = colorsB, s = sizeB, edgecolors = ec, linewidth = mew)
ax2.scatter(xB, yC, c = colorsC, s = sizeC, edgecolors = ec, linewidth = mew)
ax2.set_ylim(bottom = 0, top = 4)
ax2.set_autoscale_on(False)
ax2.set_ylabel('Three Best',weight='bold')

# draws the canvas
plt.show()
