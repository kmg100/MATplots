###########################################################################
import numpy as np
from PIL import Image, ImageDraw
#from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import wx
import time
global xdata1
import numpy as np
global fps
fps = 0.
drawing = False
global start_time
start_time = time.time()


class Testu_logs ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Testu logs", pos = wx.DefaultPosition, size = wx.Size( 700,450 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        lisst=[]
        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
        ####Izveidoti jauni atteli ar RGBA kanaliem
        for i in range(1,101):
            globals()["img_" + str(i)] = Image.new('RGBA', (600,600), color=(255,255,25,50))
            lisst.append(globals()["img_" + str(i)])
        #uzzime virsu viniem
        self.imgG = Image.new('RGBA', (600,600), color=(255,255,255,0))
        self.imgR = Image.new('RGBA', (600,600), color=(255,255,255,0))
        self.imgB = Image.new('RGBA', (600,600), color=(255,255,255,0))
        draw = ImageDraw.Draw(self.imgG)
        draw.line((100,200, 150,300), fill='green',width=10)
        draw2 = ImageDraw.Draw(self.imgB)
        draw2.line((200,200, 150,400), fill='blue',width=20)
        draw3 = ImageDraw.Draw(self.imgR)
        draw3.line((200,200, 50,500), fill='red',width=20)
        

        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN|wx.TAB_TRAVERSAL )
        self.m_panel2.SetMinSize( wx.Size( 150,-1 ) )
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel1.SetDoubleBuffered(True)
        
        bSizer1.Add( self.m_panel1, 1, wx.EXPAND, 5 )        
        #izveido jaunus wx attelus ko var parveidot uz bitmap ar tadu pasu izmeru ka pil atteli

        
        #self.wx_image1.SetAlpha(150)
        #no atteliem parveido uz bitmap
        self.bitt=[]
        for item in lisst:
            globals()["bmp_" + str(i)] = self.transp(item)
            self.bitt.append(globals()["bmp_" + str(i)])
        self.bmp = self.transp(self.imgR)
        self.bmp2 = self.transp(self.imgG)
        self.bmp3 = self.transp(self.imgB)

        
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
        #self.timer = wx.Timer(self)
        #self.Bind(wx.EVT_TIMER, self.draw, self.timer)

        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        bSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button1 = wx.Button( self.m_panel2, wx.ID_ANY, u"Variants A", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button1, 0, wx.ALL, 5 )

        self.m_button2 = wx.Button( self.m_panel2, wx.ID_ANY, u"Variants B", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button2, 0, wx.ALL, 5 )
        
        self.toggleBtn = wx.Button(self.m_panel2, wx.ID_ANY, "Start")
        bSizer2.Add( self.toggleBtn, 0, wx.ALL, 5 )
        self.sldR = wx.Slider(self.m_panel2, value = 10, minValue = 0,pos=(0,0), maxValue = 255,style = wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.sldG = wx.Slider(self.m_panel2, value = 10, minValue = 0,pos=(0,50), maxValue = 255,style = wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.sldB = wx.Slider(self.m_panel2, value = 10, minValue = 0,pos=(0,100), maxValue = 255,style = wx.SL_HORIZONTAL|wx.SL_LABELS)

        #self.txt = wx.StaticText(self.m_panel2, label = 'Hello',style = wx.ALIGN_CENTER)


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
        self.sldR.Bind(wx.EVT_SLIDER, self.OnSliderScrollR)
        self.sldG.Bind(wx.EVT_SLIDER, self.OnSliderScrollG)
        self.sldB.Bind(wx.EVT_SLIDER, self.OnSliderScrollB)
        ########################
    def __del__( self ):
        pass
    # Virtual event handlers, overide them in your derived class
    def OnClose( self, event ):
        #self.Close()
        #pass
        event.Skip()

    def OnIdle( self, event ):
        event.RequestMore(True)
        global fps, start_time
        current_time = time.time()
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
            #self.timer.Start(1)
            #self.toggleBtn.SetLabel("Stop")
        else:
            print ("timer stopped!")
            #self.timer.Stop()
            #self.toggleBtn.SetLabel("Start")

    def OnVariantsA( self, event ):
        global Blit
        Blit = True
        self.imgR.putalpha(128)
        self.imgB.putalpha(0)
        self.imgG.putalpha(30)
        #self.Combine()
        print ("With Blit")
        #self.timer.Start(10)

    def OnVariantsB( self, event ):
        global Blit
        for i in range(1,255):
            self.imgR.putalpha(i)
        self.imgG.putalpha(200)
        self.imgB.putalpha(128)
        Blit = False
    

#####paint funkcija kur atkariba no vertiba bitmapi tiek zimeti viens uz otra
    def OnPaint(self,event):
        dc = wx.PaintDC(self.m_panel1)
        dc.SetBackground(wx.Brush("WHITE"))

        # ... drawing here all other images in order of overlapping

        for itemz in self.bitt:
            dc.DrawBitmap(itemz, 0, 0, True)
        dc.DrawBitmap(self.bmp , 0, 0, True)
        dc.DrawBitmap(self.bmp2, 0, 0, True)
        dc.DrawBitmap(self.bmp3, 0, 0, True)

        
    def OnSliderScrollR(self, event): 
        obj = event.GetEventObject()
        val = obj.GetValue()
        self.imgR.putalpha(val)
        self.bmp = self.transp(self.imgR)
        self.m_panel1.Refresh()#komanda lai parzimetu attēlu
                
    def OnSliderScrollG(self, event): 
        obj = event.GetEventObject()
        val = obj.GetValue()
        self.imgG.putalpha(val)
        self.bmp2  = self.transp(self.imgG)
        self.m_panel1.Refresh()#komanda lai parzimetu attēlu
        
        
    def OnSliderScrollB(self, event): 
        obj = event.GetEventObject()
        val = obj.GetValue()
        imgnp = np.array(self.imgB.convert().copy() )
        white = np.sum(imgnp[:,:,:3], axis=2)
        white_mask = np.where(white != 255*3, 1, 0)
        alpha = np.where(white_mask, val, imgnp[:,:,-1])
        imgnp[:,:,-1] = alpha 
        self.bmp3 =  wx.Bitmap.FromBufferRGBA(600,600,imgnp)
        self.m_panel1.Refresh()#komanda lai parzimetu attēlu
        

    def draw(self, event):
        pass

        ##funkcija kas partaisa balto fonu uz caurspidigu
    def transp(self,img):
        imgnp = np.array(img.convert('RGBA')).copy() 
        white = np.sum(imgnp[:,:,:3], axis=2)
        white_mask = np.where(white == 255*3, 1, 0)
        alpha = np.where(white_mask, 0, imgnp[:,:,-1])
        imgnp[:,:,-1] = alpha 
        ##si funkcija parveido jauno attelu par bitmapu
        #no atteliem parveido uz bitmap
        return wx.Bitmap.FromBufferRGBA(600,600,imgnp)

        
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

    

    #fps = str( int( fps ) )
    #Testu_logs.m_statusBar1.SetStatusText( 'FPS:{0:3d}'.format( fps ) )
    



#app = wx.App( False )

#frame = Testu_logs( None )
#frame.Show( True )

#start the applications
#app.MainLoop()
