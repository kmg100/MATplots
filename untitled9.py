import wx
import wx.lib.agw.aui as aui
import wx.lib.mixins.inspection as wit
import numpy as np
from numba import vectorize, cuda


import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar


class Plot(wx.Panel):
    def __init__(self, parent, id=-1, dpi=None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, **kwargs)
        x = np.linspace(0,50., num=100)
        X,Y = np.meshgrid(x,x)
        self.wxBitmapFromBits(X,Y)




class PlotNotebook(wx.Panel):
    def __init__(self, parent, id=-1):
        wx.Panel.__init__(self, parent, id=id)
        self.nb = aui.AuiNotebook(self)
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def add(self, name="plot"):
        page = Plot(self.nb)
        self.nb.AddPage(page, name)
        
def draw():
    x = np.linspace(0,50., num=100)
    X,Y = np.meshgrid(x,x)
    

def demo():
    # alternatively you could use
    #app = wx.App()
    # InspectableApp is a great debug tool, see:
    # http://wiki.wxpython.org/Widget%20Inspection%20Tool
    app = wit.InspectableApp()
    frame = wx.Frame(None, -1, 'Plotter')
    plotter = PlotNotebook(frame)
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    demo()