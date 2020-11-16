import time
from matplotlib import pyplot as plt
import numpy as np


def live_update(blit = False):
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
    fig.canvas.draw()   #uztaisa tuksu grafiku
    if blit:
        # cache the background
        axbackground = fig.canvas.copy_from_bbox(ax1.bbox)
        ax2background = fig.canvas.copy_from_bbox(ax2.bbox)
    plt.show(block=False)
    t_start = time.time()
    k=0.
    for i in np.arange(1000):
        img.set_data(np.sin(X/3.+k)*np.cos(Y/3.+k))#atjauno datus
        line.set_data(x, np.sin(x/3.+k))#atjauno datus
        tx = 'Mean Frame Rate:\n {fps:.3f}FPS'.format(fps= ((i+1) / (time.time() - t_start)) )
        text.set_text(tx)
        #print tx
        k+=0.11
        if blit:
            # atjauno fonu
            fig.canvas.restore_region(axbackground)
            fig.canvas.restore_region(ax2background)

            # uzzime atkartoti tikai punktus
            ax1.draw_artist(img)
            ax2.draw_artist(line)
            ax2.draw_artist(text)
            # fill in the axes rectangle
            fig.canvas.blit(ax1.bbox)
            fig.canvas.blit(ax2.bbox)
            #blit var radit atminas problemas tapec var ari bez blit
        else:
            # parstais draw
            fig.canvas.draw()
        fig.canvas.flush_events()
live_update(True)   # 130 fps
#live_update(False) # 28 fps
