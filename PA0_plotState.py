import numpy as np
import math
import matplotlib.pyplot as plt

#create the starting point for our state trajectory
start = np.matrix([[1],[0]])
#create the state transition matrix
mult = np.matrix([[math.cos(0.05), -math.sin(0.05)],
		 [math.sin(0.05), math.cos(0.05)]])
#set the current x(i) to x(0)
cur = start
for i in range(0,100): #calculate x(i) for 100 iterations from x(0)
	plt.plot(cur[0], cur[1], 'bo') #plot x(i) as a red circle
	cur = mult*cur #calculate x(i+1)
#show the finished plot
plt.show()
