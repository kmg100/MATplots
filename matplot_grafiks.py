import time
from matplotlib import pyplot as plt
import numpy as np
#from numba import vectorize, cuda


#################
def onclick(event):
    if event.dblclick:
        if event.button == 3:#ja ar labo kliski tad izprinte datus x un y 
            # pop up
            print(event.xdata,event.ydata)
            #### event.xdata,event.ydata # 

        else:
            pass # Do nothing
#######################
#@vectorize(['float32(float32, float32)'], target='cuda')
def live_update_demo(blit = False):
    x = np.linspace(0,50., num=100)
    X,Y = np.meshgrid(x,x)
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)

    img = ax1.imshow(X, vmin=-1, vmax=1, interpolation="None", cmap="RdBu")


    line, = ax2.plot([], lw=3)
    text = ax2.text(0.8,0.5, "")

    ax2.set_xlim(x.min(), x.max())
    ax2.set_ylim([-1.1, 1.1])

    fig.canvas.draw()   


    if blit:
        # cache the background
        axbackground = fig.canvas.copy_from_bbox(ax1.bbox)
        ax2background = fig.canvas.copy_from_bbox(ax2.bbox)

    plt.show(block=False)


    t_start = time.time()
    k=0.

    for i in np.arange(100000):
        img.set_data(np.sin(X/3.+k)*np.cos(Y/3.+k))
        line.set_data(x, np.sin(x/3.+k))
        tx = 'Mean Frame Rate:\n {fps:.3f}FPS'.format(fps= ((i+1) / (time.time() - t_start)) )
        text.set_text(tx)
        #print tx
        k+=0.11
        if blit:
            # restore background
            fig.canvas.restore_region(axbackground)
            fig.canvas.restore_region(ax2background)

            # redraw just the points
            ax1.draw_artist(img)
            ax2.draw_artist(line)
            ax2.draw_artist(text)

            # fill in the axes rectangle
            fig.canvas.blit(ax1.bbox)
            fig.canvas.blit(ax2.bbox)

        else:
            # redraw everything
            fig.canvas.draw()

        fig.canvas.flush_events()
        connection_id = fig.canvas.mpl_connect('button_press_event', onclick)



live_update_demo(True)   # 175 fps
#live_update_demo(False) # 28 fps
