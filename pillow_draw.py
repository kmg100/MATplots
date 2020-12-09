

###########################################################################
import numpy as np
from PIL import Image, ImageDraw
from matplotlib.figure import Figure
#from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import wx
import time
from random import randint
global xdata1

fps = 0.
drawing = False
start_time = time.time()

class Testu_logs ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Testu logs", pos = wx.DefaultPosition, size = wx.Size( 700,450 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
        self.image= Image.new('RGBA', (600,600), color=(255,255,255,255))
        self.imgG = Image.new('RGBA', (600,600), color=(255,255,255,30))
        self.imgB = Image.new('RGBA', (600,600), color=(255,255,255,85))
        self.imgR = Image.new('RGBA', (600,600), color=(255,255,255,255))
        
        draw = ImageDraw.Draw(self.imgG)
        draw.line((100,200, 150,300), fill='green',width=10)
        draw2 = ImageDraw.Draw(self.imgB)
        draw2.line((200,200, 150,400), fill='blue',width=20)
        draw3 = ImageDraw.Draw(self.imgR)
        draw3.line((200,200, 50,500), fill='red',width=20)
        self.datas = self.image.getdata()
        self.datas1 = self.imgG.getdata()
        self.datas2 = self.imgR.getdata()
        self.datas3 = self.imgB.getdata()
        self.newData=[]
        self.newData1=[]
        self.newData2=[]
        self.newData3=[]
        for item in self.datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                self.newData.append((255, 255, 255, 0))
            else:
                self.newData.append(item)
        self.image.putdata(self.newData)
        for item1 in self.datas1:
            if item1[0] == 255 and item1[1] == 255 and item1[2] == 255:
                self.newData1.append((255, 255, 255, 0))
            else:
                self.newData1.append(item1)
        self.imgG.putdata(self.newData1)
        for item2 in self.datas2:
            if item2[0] == 255 and item2[1] == 255 and item2[2] == 255:
                self.newData2.append((255, 255, 255, 0))
            else:
                self.newData2.append(item2)
        self.imgR.putdata(self.newData2)
        for item3 in self.datas3:
            if item3[0] == 255 and item3[1] == 255 and item3[2] == 255:
                self.newData3.append((255, 255, 255, 0))
            else:
                self.newData3.append(item3)
        self.imgB.putdata(self.newData3)
        #self.imgG.show()

        #self.wxImg = wx.EmptyImage( *self.img.size )
        #self.imgR.putdata((255,0,0,0))
        self.image.paste(self.imgR,(0,0),mask=self.imgR.split()[3])
        self.image.paste(self.imgG,(0,0),mask=self.imgG.split()[3])
        self.image.paste(self.imgB,(0,0),mask=self.imgB.split()[3])
        
        self.image.show()
        #self.image.paste(self.imgG)
        #self.image.paste(self.imgB)
        #self.imgRGB = Image.paste(self.imgB)
        #self.image =Image.alpha_composite(self.image,self.imgR)
        #self.image =Image.alpha_composite(self.image,self.imgG)
        #self.image =Image.alpha_composite(self.image,self.imgB)
        #self.imgB = Image.alpha_composite(self.imgRG, self.imgB) 
        
        #self.imgRGB = self.imgRGB.paste(self.imgB)
        
        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN|wx.TAB_TRAVERSAL )
        self.m_panel2.SetMinSize( wx.Size( 150,-1 ) )
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        #self.SetDoubleBuffered(True)
        bSizer1.Add( self.m_panel1, 1, wx.EXPAND, 5 )        
        
        self.wx_image = wx.Image(600, 600)
        self.wx_image.SetData(self.image.convert("RGB").tobytes())
        self.wx_image.SetAlpha(self.image.convert("RGBA").tobytes()[3::4])
        self.bitmap = wx.Bitmap(self.wx_image)
        
        #self.bitR=wx.Bitmap.FromBufferRGBA(600,600,self.imgR.tobytes())
        #self.bitG=wx.Bitmap.FromBufferRGBA(600,600,self.imgG.tobytes())
        #self.bitB=wx.Bitmap.FromBufferRGBA(600,600,self.imgB.tobytes())
   
        
        
        
        
        #self.mapBitmap1 = wx.Bitmap.FromBuffer( 600, 600,self.imgRGB.tobytes() )
        #self.mapBitmap2 = wx.Bitmap.FromBuffer( 600, 600,self.imgB.tobytes() )
        #self.mapBitmap3 = wx.Bitmap.FromBuffer( 600, 600,self.imgR.tobytes() )
        self.mapStatBit =  wx.StaticBitmap( self.m_panel1,wx.ID_ANY, self.bitmap) 


        
        
        
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
        #self.Bind(wx.EVT_PAINT, self.OnPaint)
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
            self.timer.Start(1)
            self.toggleBtn.SetLabel("Stop")
        else:
            print ("timer stopped!")
            self.timer.Stop()
            self.toggleBtn.SetLabel("Start")

    def OnVariantsA( self, event ):
        global Blit
        Blit = True
        self.imgG.putalpha(125)
        self.imgR.putalpha(30)
        self.imgB.putalpha(255)
        self.Combine()
        print ("With Blit")
        #self.timer.Start(10)

    def OnVariantsB( self, event ):
        global Blit
        self.imgG.putalpha(255)
        self.imgR.putalpha(30)
        self.imgB.putalpha(200)
        #for item in datas1:
            #self.imgG.putdata((0,0,0,85))
            #self.imgR.putdata((0,0,0,0))
            #self.imgB.putdata((0,0,0,0))
        self.Combine()
       
        Blit = False
    
    def Combine(self):

        self.imgR.save("imgR.bmp")
        self.imgG.save("imgR.bmp")
        self.imgB.save("imgR.bmp")
    # Open image and ensure it has an alpha channel
        im1 = Image.open("imgR.bmp").convert('RGBA')
        im2 = Image.open("imgG.bmp").convert('RGBA')
        im3 = Image.open("imgB.bmp").convert('RGBA')
# Make into Numpy array, shape [h,w,4]
        ni1 = np.array(im1)
        ni2 = np.array(im2)
        ni3 = np.array(im3)
        print(ni1)
# Set the alpha channel of each pixel to "255 - red"
        np.where(ni1==[255,255,255,255],[255,255,255,0],ni1)
        np.where(ni2==(255,255,255,255),(255,255,255,0),ni2)
        np.where(ni3==(255,255,255,255),(255,255,255,0),ni3)
        print(ni1)

# Make back into PIL Image and save
        self.imgR = Image.fromarray(ni1)
        self.imgG = Image.fromarray(ni2)
        self.imgB = Image.fromarray(ni3)
        """
        self.datas = self.image.getdata()
        self.datas1 = self.imgG.getdata()
        self.datas2 = self.imgR.getdata()
        self.datas3 = self.imgB.getdata()
        self.newData=[]
        self.newData1=[]
        self.newData2=[]
        self.newData3=[]
        for item in self.datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                self.newData.append((255, 255, 255, 0))
            else:
                self.newData.append(item)
        self.image.putdata(self.newData)
        for item1 in self.datas1:
            if item1[0] == 255 and item1[1] == 255 and item1[2] == 255:
                self.newData1.append((255, 255, 255, 0))
            else:
                self.newData1.append(item1)
        self.imgG.putdata(self.newData1)
        for item2 in self.datas2:
            if item2[0] == 255 and item2[1] == 255 and item2[2] == 255:
                self.newData2.append((255, 255, 255, 0))
            else:
                self.newData2.append(item2)
        self.imgR.putdata(self.newData2)
        for item3 in self.datas3:
            if item3[0] == 255 and item3[1] == 255 and item3[2] == 255:
                self.newData3.append((255, 255, 255, 0))
            else:
                self.newData3.append(item3)
        self.imgB.putdata(self.newData3)
        """
        self.image.paste(self.imgR,(0,0),mask=self.imgR.split()[3])
        self.image.paste(self.imgG,(0,0),mask=self.imgG.split()[3])
        self.image.paste(self.imgB,(0,0),mask=self.imgB.split()[3])
        #self.image =Image.alpha_composite(self.image,self.imgR)
        #self.image =Image.alpha_composite(self.image,self.imgG)
        #self.image =Image.alpha_composite(self.image,self.imgB)
        #self.image =  Image.alpha_composite(self.imgR.convert('RGBA'), self.imgB.convert('RGBA'))
        self.wx_image = wx.Image(600, 600)
        self.wx_image.SetData(self.image.convert("RGB").tobytes())
        self.wx_image.SetAlpha(self.image.convert("RGBA").tobytes()[3::4])
        self.bitmap = wx.Bitmap(self.wx_image)
        self.mapStatBit =  wx.StaticBitmap( self.m_panel1,wx.ID_ANY, self.bitmap)
                
        """
    def OnPaint(self,event):
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush("WHITE"))

        # ... drawing here all other images in order of overlapping
        if Blit == True:
            dc.DrawBitmap(self.bitR, 0, 0, True)
        else:
            dc.DrawBitmap(self.bitG, 0, 0, True)
            dc.DrawBitmap(self.bitB, 0, 0, True)
"""

    def draw(self, event):
        global start_time
        global k, fps
        global Blit
        global drawing
        
        
        if drawing:
            return
        drawing = True
        
        #x = np.linspace(0,1000., num=100)
        #draw = ImageDraw.Draw(self.imgG)
        #self.y+=0.5
        #self.line_points.append((self.x,randint(0, 300)) )#for i in np.arange(3),
        #self.x+=1
        #self.y=100*np.sin(self.x/4+k)
        #print(self.line_points)
        #line_points = [(100, 100), (150, 200), (300, 100), (500, 300)]
        #draw.line(self.line_points, width=1, fill=1, joint='curve')
        self.mapStatBit.Refresh()
        #self.Refresh()
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
