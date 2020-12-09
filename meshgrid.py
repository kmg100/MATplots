
import wx
import time
import numpy as np 
 
class MyForm(wx.Frame):
 
    def __init__(self, parent ):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Timer Tutorial 1", 
                                   size=(500,500))
 
        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.toggleBtn = wx.Button(panel, wx.ID_ANY, "Start")
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        self.toggleBtn.Bind(wx.EVT_BUTTON, self.onToggle)
       
        
        x = np.linspace(0,50., num=100)
        X,Y = np.meshgrid(x,x)
        self.Bitmap = wx.StaticBitmap(self, bitmap=wx.wxBitmapFromBits(self))
        bSizer2.Add( self.Bitmap, 0, wx.ALL, 5 )
        panel.SetSizer( bSizer2 )
        panel.Layout()
        bSizer2.Fit( panel )
        
        
    
    def onToggle(self, event):
        btnLabel = self.toggleBtn.GetLabel()
        if btnLabel == "Start":
            print ("starting timer...")
            self.timer.Start(1000)
            self.toggleBtn.SetLabel("Stop")
        else:
            print ("timer stopped!")
            self.timer.Stop()
            self.toggleBtn.SetLabel("Start")
            
    def update(self, event):
        print ("\nupdated: ")
        print (time.ctime())

        
# Run the program
class MainApp(wx.App):
    def OnInit(self):
        mainFrame = MyForm(None)
        #mainFrame.draw()
        #mainFrame.status()
        mainFrame.Show(True)
        return True



if __name__ =='__main__':
    # start time of the loop
   app = MainApp()
   app.MainLoop()
