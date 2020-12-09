

###########################################################################
import numpy as np
from matplotlib import pyplot as plt

import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import animation
import wx
import time
import random
#import wx.xrc

###########################################################################
## Class Testu_logs
###########################################################################

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
        
        self.figure = plt.Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.canvas,1,wx.EXPAND)
        self.SetSizer(self.sizer)
        
        global Blit
        Blit = True
        ##########TIMER
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.draw, self.timer)

        ###############
        

        
        
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
        x=range(1,6)
        y=50
        col=[]
        global barcollection
        self.barcollection = self.axes.bar(x,y, color=col)
        self.animator = animation.FuncAnimation(self.figure,self.animate,blit = False, interval=50)


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
            self.timer.Start(1)
            self.toggleBtn.SetLabel("Stop")
        else:
            print ("timer stopped!")
            self.timer.Stop()
            self.toggleBtn.SetLabel("Start")

    def OnVariantsA( self, event ):
        global Blit
        Blit = True
        print ("With Blit")
        

    def OnVariantsB( self, event ):
        global Blit
        print ("Without Blit")
        Blit = False
        
    #def TimeInterval(self, event):
        

    def animate(self, i):
        
        global drawing
        if drawing:
            return
        drawing = True
        if Blit == True:
            for i in range(len(self.barcollection)):
                val = random.randint(0,50)
                self.barcollection[i].set_height(val)
                #print(i)
                if val < 10:
                    #print("blue")
                    self.barcollection[i].set_color("blue")
                elif val >= 25:
                    #print("green")
                    self.barcollection[i].set_color("green")
                else:
                    #print("red")
                    self.barcollection[i].set_color("red")
        drawing = False
    
    def draw(self, event):
        #print("start drawing")

        global start_time
        global k, fps
        global Blit
        

        if Blit == True:
            pass
            
        else:
            plt.clf()
            x=range(1,6)
            for i in range(len(x)):
                y=random.randint(0,50)
                self.barcollection = self.axes.bar(i,y)
            
        #self.figure.canvas.flush_events()
        #####
        current_time = time.time()
        fps =  int( ( 9 * fps + 1.0 / ( current_time - start_time ) ) / 10 )
        #fps = str( int( fps ) )
        self.m_statusBar1.SetStatusText( 'FPS:{0:3d}'.format( fps ) )
        start_time = current_time
        
        
        
        
class MainApp(wx.App):
    def OnInit(self):
        mainFrame = Testu_logs(None)
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
