'''
Libraries include matplotlib and scipy,
which can be installed by double clicking on the
"installrequirements.bat" (Windows)
'''
import time
import numpy
import matplotlib.pyplot as plt
from scipy import stats
import tkinter as tk
import os

# Setup Variables

bgcolor='#e6e6e6'
linecount=0

# Open config file and set variables

userconfig=[0,"gordon","crowbar",[],[]]
configtxt = open("config.txt", "r+")
Lines = configtxt.readlines()

# Most optimized line reading method I could write, using an array
for line in Lines:
  string=line.split('=')
  string=string[1]
  string=string.strip()
  userconfig[linecount]=string
  linecount+=1

#Turn the two data arrays into actual arrays
userconfig[3]=[int(n) for n in userconfig[3].split(',')]
userconfig[4]=[int(n) for n in userconfig[4].split(',')]

if(userconfig[0]=='1'):
  # Totally NOT discord's dark mode color!
  bgcolor='#2C2F33'

sleepmodel = numpy.poly1d(numpy.polyfit(userconfig[3], userconfig[4], 3))

myline = numpy.linspace(0, 100, 100)

plt.scatter(userconfig[3], userconfig[4])
plt.plot(myline, sleepmodel(myline))
plt.show()



'''
# Setup Canvas

root=tk.Tk()
root.title("Sleep Helper")
canvas = tk.Canvas(root, height='800', width='800', bg=bgcolor)
canvas.pack()

# Plot the Polynomial Regression Graph

# Functions

# Main loop

root.mainloop()
'''