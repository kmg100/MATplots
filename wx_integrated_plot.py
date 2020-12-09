


# -*- coding: utf-8 -*-

###########################################################################
import numpy as np
from drawing_module import PlotGraphics,PolySpline,PlotCanvas
#from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import wx
import time
from numba import jit


global xdata1

fps = 0.
drawing = False
start_time = time.time()


x=np.arange(1000)
#seit izveido objektu ko zimes plota
def _draw1Objects():
    global x
    # 100 points sin function, plotted as green dots
    data1 = 2. * np.pi * x / 200.+k
    data1.shape = (500, 2)
    data1[:, 1] = np.sin(data1[:, 0])
    line1 = PolySpline(
        data1, legend='Green Line', colour='green', width=1)

    # 50 points cos function, plotted as red dot-dash
    data1 = 2. * np.pi * x / 100.+k
    data1.shape = (500, 2)
    data1[:, 1] = np.cos(data1[:, 0])
    line2 = PolySpline(data1, legend='Red Line', colour='red', width=1)

    return PlotGraphics([ line1, line2], "Testu grafiki")




class Testu_logs ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Testu logs", pos = wx.DefaultPosition, size = wx.Size( 700,450 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )



        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN|wx.TAB_TRAVERSAL )
        self.m_panel2.SetMinSize( wx.Size( 150,-1 ) )
        





        self.client = PlotCanvas(self)
        #self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer1.Add( self.client, 1, wx.EXPAND, 5 )        
        global k
        k=0.
        global Blit
        Blit = True
        ##########TIMER
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.draw, self.timer)


 
        
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
        
        # define the function for drawing pointLabels
        #self.client.SetPointLabelFunc(self.DrawPointLabel)
        # Create mouse event for showing cursor coords in status bar
        #self.client.canvas.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        # Show closest point when enabled
        #self.client.canvas.Bind(wx.EVT_MOTION, self.OnMotion)
        self.resetDefaults()
        self.Show(True)




    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def OnClose( self, event ):
        #self.Close()
        #pass
        event.Skip()

    def OnIdle( self, event ):
        event.RequestMore(True)
        global fps, start_time,k
        current_time = time.time()
        k+=0.11
        self.client.Draw(_draw1Objects())
        #self.m_panel1.Refresh()
        try:
            fps =  int( ( 9 * fps + 1.0 / ( current_time - start_time ) ) / 10 )
            self.m_statusBar1.SetStatusText( 'FPS:{0:3d}'.format( fps ) )
        except ZeroDivisionError:
            pass
        start_time = current_time
        
    def onToggle(self, event):
        btnLabel = self.toggleBtn.GetLabel()
        if btnLabel == "Start":
            print ("starting timer...")
            self.timer.Start(0)
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
    

    def resetDefaults(self):
        """Just to reset the fonts back to the PlotCanvas defaults"""
        self.client.SetFont(
            wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.client.SetFontSizeAxis(10)
        self.client.SetFontSizeLegend(7)
        self.client.setLogScale((False, False))
        self.client.SetXSpec('auto')
        self.client.SetYSpec('auto')
        



    #@nb.jit(nopython=True)
    def draw(self, event):
        global start_time
        global k, fps
        global Blit
        global drawing
        
        if drawing:
            return
        drawing = True

        #self.axes.plot([], lw=3)
        k+=0.11

    
        if Blit == True:
            #self.resetDefaults()
            pass
            #print(k)


        #####
        current_time = time.time()
        try:
            fps =  int( ( 9 * fps + 1.0 / ( current_time - start_time ) ) / 10 )
        except ZeroDivisionError:
            pass
        #fps = str( int( fps ) )
        #self.m_statusBar1.SetStatusText( 'FPS:{0:3d}'.format( fps ) )
        start_time = current_time
        drawing = False



        
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







#    data1 = 2. * np.pi * np.arange(100) / 100.
 #   data1.shape = (50, 2)
  #  data1[:, 1] = np.cos(data1[:, 0])
   # lines = PolySpline(data1, legend='Red Line', colour='red')
    #
#PlotGraphics([markers1, lines, markers2], "Graph Title", "X Axis", "Y Axis")