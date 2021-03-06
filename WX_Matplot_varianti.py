# -*- coding: utf-8 -*-

###########################################################################
#MATPLOTLIB grafiki
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
        
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.canvas,1,wx.EXPAND)
        self.SetSizer(self.sizer)
        global x
        x = np.linspace(0,50., num=100)
        X,Y = np.meshgrid(x,x)
        global line
        line, = self.axes.plot([], lw=3)
        global k
        k=0.
        global Blit
        Blit = True
        ##########TIMER
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.draw, self.timer)

        ################
        self.axes.set_xlim(x.min(), x.max())
        self.axes.set_ylim([-1.1, 1.1])
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
        #self.figure = mpl.figure.Figure(figsize=(2, 2))
        #self.canvas = FigureCanvas(self, -1, self.figure)
        #self.timer = wx.Timer(self)
        #self.Bind(wx.EVT_TIMER, self.TimeInterval, self.tim


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
        #self.timer.Start(10)

    def OnVariantsB( self, event ):
        global Blit
        print ("Without Blit")
        Blit = False
        #self.timer.Stop()
    #def TimeInterval(self, event):
        

    def draw(self, event):
        global start_time
        global k, fps
        global Blit
        global drawing
        
        if drawing:
            return
        drawing = True
        self.figure.canvas.mpl_connect('button_press_event', self.OnClick)
        #x = np.linspace(0,50., num=100)
        #X,Y = np.meshgrid(x,x)
        #self.set_data(x, np.sin(x/3.+k))
        
        #self.axes.plot([], lw=3)
        k+=0.11
        line.set_data(x, np.sin(x/3.+k))
        if Blit == True:
            self.figure.canvas.restore_region(self.axesbackground)
            self.axes.draw_artist(line)
            self.figure.canvas.blit(self.axes.bbox)
            #print(k)
        else:
            self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        #####
        current_time = time.time()
        try:
            fps =  int( ( 9 * fps + 1.0 / ( current_time - start_time ) ) / 10 )
        except ZeroDivisionError as e:
            pass
        #fps = str( int( fps ) )
        self.m_statusBar1.SetStatusText( 'FPS:{0:3d}'.format( fps ) )
        start_time = current_time
        drawing = False
        
    def OnClick(self, event):
        if event.dblclick:  
            pass
        else:
            if event.button == 3:
                try:#wx.MessageBox("This is a Message Box", "Message" ,wx.OK | wx.ICON_INFORMATION)
                    if wx.TheClipboard.Open():
                        wx.TheClipboard.SetData(wx.TextDataObject(str("%.2f" %event.ydata)))
                        print("sucess")
                        wx.TheClipboard.Close()
                    self.xdata1=str("%.2f" %event.xdata)
                    self.ydata1=str("%.2f" %event.ydata)
                    print(self.xdata1,self.ydata1)
                    a = MyDialog(self, "Dialog",self.xdata1,self.ydata1).ShowModal()
                except TypeError:
                    pass
        
class MyDialog(wx.Dialog): 
   def __init__(self, parent, title, xtext,ytext): 
      super(MyDialog, self).__init__(parent, title = "Izvēlētie Dati", size = (150,150)) 
      panel = wx.Panel(self) 
      #####Text box for data
      self.textboxSampleTime =  wx.StaticText(panel, -1,label=xtext, pos = (0,0))
      self.textboxSampleTime =  wx.StaticText(panel, -1,label=ytext, pos = (0,15))
      #####Button
      self.btn = wx.Button(panel, wx.ID_OK, label = "EXIT", size = (50,20), pos = (50,50))
      
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
