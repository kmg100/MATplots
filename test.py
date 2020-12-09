# -*- coding: utf-8 -*-

###########################################################################
import wx.lib.agw.aui as aui
import wx.lib.mixins.inspection as wit
import numpy as np
from matplotlib import pyplot as plt

import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import wx
import time
import random
from matplotlib import cm
#import wx.xrc


import wx.lib.mixins.inspection as WIT

fps = 0.
drawing = False
start_time = time.time()

class Testu_logs ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Testu logs", pos = wx.DefaultPosition, size = wx.Size( 700,450 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer1.Add( self.m_panel1, 1, wx.EXPAND, 5 )

        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN|wx.TAB_TRAVERSAL )
        self.m_panel2.SetMinSize( wx.Size( 150,-1 ) )
        
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.canvas,1,wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit
        global x
        x =range(1,6)
        global y
        y=1000
       
        colors = []
        global barcollection
        self.barcollection = self.axes.bar(x,y,color=colors)
        global my_cmap
        my_cmap = plt.cm.get_cmap('jet')#seit parveido krasu lai atbilstu colormap
        
        global k
        k=0.
        global Blit
        Blit = True
        ##########TIMER
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.draw, self.timer)

        ################

        self.figure.canvas.draw() 
        
        self.axesbackground = self.figure.canvas.copy_from_bbox(self.axes.bbox)
        plt.show(block=False)
        
        bSizer2 = wx.BoxSizer( wx.VERTICAL )


        bSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button1 = wx.Button( self.m_panel2, wx.ID_ANY, u"Variants A", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button1, 0, wx.ALL, 5 )

        self.m_button2 = wx.Button( self.m_panel2, wx.ID_ANY, u"Variants B", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button2, 0, wx.ALL, 5 )
        
        self.toggleBtn = wx.Button(self.m_panel2, wx.ID_ANY, "Start")
        bSizer2.Add( self.toggleBtn, 0, wx.ALL, 5 )


        bSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        self.m_panel2.SetSizer( bSizer2 )
        self.m_panel2.Layout()
        bSizer2.Fit( self.m_panel2 )
        bSizer1.Add( self.m_panel2, 0, wx.EXPAND, 5 )

        
        self.SetSizer( bSizer1 )
        self.Layout()


        self.Centre( wx.BOTH )
        self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP|wx.BORDER_RAISED, wx.ID_ANY )
        # Connect Events
        self.Bind( wx.EVT_CLOSE, self.OnClose )
        self.Bind( wx.EVT_IDLE, self.OnIdle )
        self.m_button1.Bind( wx.EVT_BUTTON, self.OnVariantsA )
        self.m_button2.Bind( wx.EVT_BUTTON, self.OnVariantsB )
        self.toggleBtn.Bind(wx.EVT_BUTTON, self.onToggle)
        ########################
        self.figure.canvas.mpl_connect('button_press_event', self.OnClick)

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def OnClose( self, event ):
        #self.Close()
        #pass
        event.Skip()

    def OnIdle( self, event ):
        event.Skip()
        
    def onToggle(self, event):
        btnLabel = self.toggleBtn.GetLabel()
        if btnLabel == "Start":
            print ("starting timer...")
            self.timer.Start(5)
            self.toggleBtn.SetLabel("Stop")
        else:
            print ("timer stopped!")
            self.timer.Stop()
            self.toggleBtn.SetLabel("Start")

    def OnVariantsA( self, event ):
        global Blit
        Blit = True
        self.barcollection = self.axes.bar(x,y)
        self.figure.canvas.draw() 
        self.axesbackground = self.figure.canvas.copy_from_bbox(self.axes.bbox)
        plt.show(block=False)
        print ("With Blit")
        #self.timer.Start(10)

    def OnVariantsB( self, event ):
        global Blit
        print ("Without Blit")
        Blit = False
        #self.timer.Stop()
    #def TimeInterval(self, event):
        
    def OnClick(self, e):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if e.dblclick else 'single', e.button,
           e.x, e.y, e.xdata, e.ydata))
        
        
    def draw(self, event):
        global start_time
        global k, fps
        global Blit
        global drawing
        global my_cmap
        
        if drawing:
            return
        drawing = True
        if Blit == True:##Seit kods lai zimetu barus atrak izmantojot set height un canvas draw
            for i in range(len(self.barcollection)):
                y = random.randint(0,1000)
                colors = my_cmap(y)
                #self.figure.canvas.restore_region(self.axesbackground)
                self.barcollection[i].set_height(y)#nomaina bara augstumu
                #self.axes.draw_artist(self.barcollection[i])
                self.barcollection[i].set_color(colors)##Seit izmantojot colormap liek krasu atksiriba no datiem
                #self.figure.canvas.blit(self.axes.bbox)
            self.figure.canvas.draw()#parzime jaunu bar tikai
            #plt.pause(0.001)
        else:
            self.axes.clear()
            y = np.random.randint(1,1001,5)
            #print(y)
            #my_cmap = plt.cm.get_cmap('jet')
            colors = my_cmap(y)
            self.barcollection = self.axes.bar(x,y, color=colors)
            self.figure.canvas.draw()
            self.axes.clear()
        #self.figure.canvas.flush_events()
        current_time = time.time()
        try:
            fps =  int( ( 9 * fps + 1.0 / ( current_time - start_time ) ) / 10 )
        except ZeroDivisionError:
            pass
        self.m_statusBar1.SetStatusText( 'FPS:{0:3d}'.format( fps ) )
        start_time = current_time
        drawing = False
        
        #wx.App
class MainApp(wx.App):
    def OnInit(self):
        mainFrame = Testu_logs(None)
        #mainFrame.draw()
        #mainFrame.status()
        mainFrame.Show(True)
        return True



if __name__ =='__main__':
    # start time of the loop
   app = MainApp()
   app.MainLoop()



#app = wx.App( False )

#frame = Testu_logs( None )
#frame.Show( True )

#start the applications
#app.MainLoop()
