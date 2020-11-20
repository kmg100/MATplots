import matplotlib.pyplot as plt
from matplotlib import animation
import random
import time
fig=plt.figure()
y = 50
global col
col = []
x=range(1,6)
barcollection = plt.bar(x,y, color = col)
t_start = time.time()
def animate(i):
    for i in range(len(barcollection)):
        val = random.randint(0,50)
        barcollection[i].set_height(val)
        print(val)
        if val < 10:
            print("blue")
            barcollection[i].set_color("blue")
        elif val >= 25:
            print("green")
            barcollection[i].set_color("green")
        else:
            print("red")
            barcollection[i].set_color("red")
	#fps = (( i + 1 ) / (time.time() - t_start))
	#print(fps)
    #barcollection = plt.bar(x,y,color = col)
anim=animation.FuncAnimation(fig,animate,blit=False,interval=1000)


plt.show()
