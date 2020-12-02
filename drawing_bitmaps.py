
###########################################################################
import numpy as np
from PIL import Image, ImageDraw
#from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import wx
import time
from random import randint
from turtle import *
global xdata1

fps = 0.
drawing = False
start_time = time.time()







"""
ht(); speed(0)
color('green'); width(1)

for i in range(4): # axes
    fd(80); bk(80); rt(90)

color('red'); width(2)
pu(); goto(-50, -70); pd()

for x in range(-50, 30):
    y = 2*x + 30
    goto(x, y)

"""
class Testu_logs ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Testu logs", pos = wx.DefaultPosition, size = wx.Size( 700,450 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
        ####Izveidoti jauni atteli ar RGBA kanaliem
        self.imgG = Image.new('RGBA', (600,600), color=(255,255,255,80))
        self.imgB = Image.new('RGBA', (600,600), color=(255,255,255,80))
        self.imgR = Image.new('RGBA', (600,600), color=(255,255,255,80))
        #uzzime virsu viniem
        draw = ImageDraw.Draw(self.imgG)
        draw.line((100,200, 150,300), fill='green',width=10)
        draw2 = ImageDraw.Draw(self.imgB)
        draw2.line((200,200, 150,400), fill='blue',width=20)
        draw3 = ImageDraw.Draw(self.imgR)
        draw3.line((200,200, 50,500), fill='red',width=20)
        
        #self.imgG.putdata((0,0,0,0))
        
        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN|wx.TAB_TRAVERSAL )
        self.m_panel2.SetMinSize( wx.Size( 150,-1 ) )
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel1.SetDoubleBuffered(True)
        
        bSizer1.Add( self.m_panel1, 1, wx.EXPAND, 5 )        
        #izveido jaunus wx attelus ko var parveidot uz bitmap ar tadu pasu izmeru ka pil atteli
        self.wx_image1 = wx.Image(600, 600)
        self.wx_image2 = wx.Image(600, 600)
        self.wx_image3 = wx.Image(600, 600)
        #print('here')
        #### seit pil attela datus iedod wx attelam gan rga vertibas gan alpha vertibas
        self.wx_image1.SetData(self.imgR.convert("RGB").tobytes())
        self.wx_image1.SetAlpha(self.imgR.convert("RGBA").tobytes()[3::4])
        self.wx_image2.SetData(self.imgG.convert("RGB").tobytes())
        self.wx_image2.SetAlpha(self.imgG.convert("RGBA").tobytes()[3::4])
        self.wx_image3.SetData(self.imgB.convert("RGB").tobytes())
        self.wx_image3.SetAlpha(self.imgB.convert("RGBA").tobytes()[3::4])
        
        #self.wx_image1.SetAlpha(150)
        #no atteliem parveido uz bitmap
        self.bmp = wx.Bitmap(self.wx_image1)
        self.bmp2 = wx.Bitmap(self.wx_image2)
        self.bmp3 = wx.Bitmap(self.wx_image3)
        
        #self.bmp=wx.Bitmap.FromBuffer(600,600,self.imgR.tobytes())
        #self.bmp2=wx.Bitmap.FromBuffer(600,600,self.imgG.tobytes())
        #self.bmp3=wx.Bitmap.FromBuffer(600,600,self.imgB.tobytes())
        
        #self.bmp = wx.Bitmap.FromRGBA()
        #self.bmp2 = wx.Bitmap.FromRGBA(600, 600, red=0, green=0, blue=255, alpha=80)
        #self.bmp3 = wx.Bitmap.FromRGBA(600, 600, red=255, green=0, blue=0, alpha=80)
        
        
        global k
        k=0.
        global Blit
        Blit = True
        ##########TIMER
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.draw, self.timer)

        ################


 
        
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
        #lai zimetu vislaik uz panela 1
        self.m_panel1.Bind(wx.EVT_PAINT, self.OnPaint)
        ########################




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
            self.timer.Start(0)
            self.toggleBtn.SetLabel("Stop")
        else:
            print ("timer stopped!")
            self.timer.Stop()
            self.toggleBtn.SetLabel("Start")

    def OnVariantsA( self, event ):
        global Blit
        Blit = True
        self.imgG.putdata((0,0,0,0))
        #self.Combine()
        print ("With Blit")
        #self.timer.Start(10)

    def OnVariantsB( self, event ):
        global Blit
        datas = self.imgG.getdata()
        for item in datas:
            self.imgG.putdata((0,0,0,0))
        #self.imgR.putdata((255,255,255,150))
        #self.imgB.putdata((255,255,255,150))
       
        Blit = False
    

#####paint funkcija kur atkariba no vertiba bitmapi tiek zimeti viens uz otra
    def OnPaint(self,event):
        dc = wx.PaintDC(self.m_panel1)
        dc.SetBackground(wx.Brush("WHITE"))

        # ... drawing here all other images in order of overlapping
        if Blit == True:
            dc.DrawBitmap(self.bmp , 0, 0, True)
            dc.DrawBitmap(self.bmp2, 0, 0, True)
        elif Blit == False:
            dc.DrawBitmap(self.bmp3, 0, 0, True)
        


    def draw(self, event):
        global start_time
        global k, fps
        global Blit
        global drawing
        
        
        if drawing:
            return
        drawing = True

        
        self.m_panel1.Refresh()#komanda lai parzimetu attēlu
        
        #self.img.show()
        #####
        current_time = time.time()
        try:
            fps =  int( ( 9 * fps + 1.0 / ( current_time - start_time ) ) / 10 )
        except ZeroDivisionError:
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
                    if wx.TheClipboard.Open():#pievieno y data clipboardam
                        wx.TheClipboard.SetData(wx.TextDataObject(str("%.2f" %event.ydata)))
                        print("Sucess")
                        wx.TheClipboard.Close()
                    self.xdata1=str("X Dati: %.2f" %event.artist.get_xdata())
                    self.ydata1=str("Y Dati: %.2f" %event.artist.get_ydata())
                    print(self.xdata1,self.ydata1)
                    MyDialog(self, "Dialog",self.xdata1,self.ydata1).ShowModal()
                except TypeError:
                    pass
            #### event.xdata,event.ydata # here you click on the plot

class MyDialog(wx.Dialog): 
   def __init__(self, parent, title, xtext,ytext): 
      super(MyDialog, self).__init__(parent, title = "Izvēlētie Dati", size = (150,150)) 
      panel = wx.Panel(self) 
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
