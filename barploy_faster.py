import matplotlib.pyplot as plt
from matplotlib import animation
import random
import time


fig=plt.figure()

x=range(1,6)
barcollection = plt.bar(x,50)
t_start = time.time()
def animate(i):
    for i in range(len(barcollection)):
    	barcollection[i].set_height(random.randint(0,50))
	#fps = (( i + 1 ) / (time.time() - t_start))
	#print(fps)
anim=animation.FuncAnimation(fig,animate,blit=False,interval=1)


plt.show()
