
import sys
import wx
from numba import jit
from wx import glcanvas
# Needs NumPy
try:
    import numpy as np
except:
    msg = """
    This module requires the NumPy module, which could not be
    imported.  It probably is not installed (it's not part of the
    standard Python distribution). See the Numeric Python site
    (http://numpy.scipy.org) for information on downloading source or
    binaries."""
    raise ImportError("NumPy not found.\n" + msg)


#
# Plotting classes...
#
class PolyPoints:

    """Base Class for lines and markers
        - All methods are private.
    """

    def __init__(self, points, attr):
        self._points = np.array(points).astype(np.float64)
        self._logscale = (False, False)
        self._pointSize = (1.0, 1.0)
        self.currentScale = (1, 1)
        self.currentShift = (0, 0)
        self.scaled = self.points
        self.attributes = {}
        self.attributes.update(self._attributes)
        for name, value in attr.items():
            if name not in self._attributes.keys():
                raise KeyError(
                    "Style attribute incorrect. Should be one of %s" % self._attributes.keys())
            self.attributes[name] = value

    def setLogScale(self, logscale):
        self._logscale = logscale

    def __getattr__(self, name):
        if name == 'points':
            if len(self._points) > 0:
                data = np.array(self._points, copy=True)
                if self._logscale[0]:
                    data = self.log10(data, 0)
                if self._logscale[1]:
                    data = self.log10(data, 1)
                return data
            else:
                return self._points
        else:
            raise AttributeError(name)

    def log10(self, data, ind):
        data = np.compress(data[:, ind] > 0, data, 0)
        data[:, ind] = np.log10(data[:, ind])
        return data

    def boundingBox(self):
        if len(self.points) == 0:
            # no curves to draw
            # defaults to (-1,-1) and (1,1) but axis can be set in Draw
            minXY = np.array([-1.0, -1.0])
            maxXY = np.array([1.0, 1.0])
        else:
            minXY = np.minimum.reduce(self.points)
            maxXY = np.maximum.reduce(self.points)
        return minXY, maxXY

    def scaleAndShift(self, scale=(1, 1), shift=(0, 0)):
        if len(self.points) == 0:
            # no curves to draw
            return
        if (scale is not self.currentScale) or (shift is not self.currentShift):
            # update point scaling
            self.scaled = scale * self.points + shift
            self.currentScale = scale
            self.currentShift = shift
        # else unchanged use the current scaling

    def getLegend(self):
        return self.attributes['legend']

    def getClosestPoint(self, pntXY, pointScaled=True):
        """Returns the index of closest point on the curve, pointXY, scaledXY, distance
            x, y in user coords
            if pointScaled == True based on screen coords
            if pointScaled == False based on user coords
        """
        if pointScaled == True:
            # Using screen coords
            p = self.scaled
            pxy = self.currentScale * np.array(pntXY) + self.currentShift
        else:
            # Using user coords
            p = self.points
            pxy = np.array(pntXY)
        # determine distance for each point
        d = np.sqrt(np.add.reduce((p - pxy) ** 2, 1))  # sqrt(dx^2+dy^2)
        pntIndex = np.argmin(d)
        dist = d[pntIndex]
        return [pntIndex, self.points[pntIndex], self.scaled[pntIndex] / self._pointSize, dist]


class PolyLine(PolyPoints):

    """Class to define line type and style
        - All methods except __init__ are private.
    """

    _attributes = {'colour': 'black',
                   'width': 1,
                   'style': wx.PENSTYLE_SOLID,
                   'legend': ''}

    def __init__(self, points, **attr):
        """
        Creates PolyLine object

        :param `points`: sequence (array, tuple or list) of (x,y) points making up line
        :keyword `attr`: keyword attributes, default to:

         ==========================  ================================
         'colour'= 'black'           wx.Pen Colour any wx.NamedColour
         'width'= 1                  Pen width
         'style'= wx.PENSTYLE_SOLID  wx.Pen style
         'legend'= ''                Line Legend to display
         ==========================  ================================

        """
        PolyPoints.__init__(self, points, attr)

    @jit(nopython=True)
    def draw(self, dc, printerScale, coord=None):
        colour = self.attributes['colour']
        width = self.attributes['width'] * printerScale * self._pointSize[0]
        style = self.attributes['style']
        if not isinstance(colour, wx.Colour):
            colour = wx.NamedColour(colour)
        pen = wx.Pen(colour, width, style)
        pen.SetCap(wx.CAP_BUTT)
        dc.SetPen(pen)
        if coord == None:
            if len(self.scaled):  # bugfix for Mac OS X
                dc.DrawLines(self.scaled)
        else:
            dc.DrawLines(coord)  # draw legend line
    
    @jit(nopython=True)
    def getSymExtent(self, printerScale):
        """Width and Height of Marker"""
        h = self.attributes['width'] * printerScale * self._pointSize[0]
        w = 5 * h
        return (w, h)


class PolySpline(PolyLine):

    """Class to define line type and style
        - All methods except __init__ are private.
    """

    _attributes = {'colour': 'black',
                   'width': 1,
                   'style': wx.PENSTYLE_SOLID,
                   'legend': ''}

    def __init__(self, points, **attr):
        """
        Creates PolyLine object

        :param `points`: sequence (array, tuple or list) of (x,y) points making up spline
        :keyword `attr`: keyword attributes, default to:

         ==========================  ================================
         'colour'= 'black'           wx.Pen Colour any wx.NamedColour
         'width'= 1                  Pen width
         'style'= wx.PENSTYLE_SOLID  wx.Pen style
         'legend'= ''                Line Legend to display
         ==========================  ================================

        """
        PolyLine.__init__(self, points, **attr)

    def draw(self, dc, printerScale, coord=None):
        colour = self.attributes['colour']
        width = self.attributes['width'] * printerScale * self._pointSize[0]
        style = self.attributes['style']
        if not isinstance(colour, wx.Colour):
            colour = wx.Colour(colour)
        pen = wx.Pen(colour, width, style)
        pen.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen)
        if coord == None:
            if len(self.scaled):  # bugfix for Mac OS X
                dc.DrawSpline(self.scaled)
        else:
            dc.DrawLines(coord)  # draw legend line


class PolyMarker(PolyPoints):

    """Class to define marker type and style
        - All methods except __init__ are private.
    """

    _attributes = {'colour': 'black',
                   'width': 1,
                   'size': 2,
                   'fillcolour': None,
                   'fillstyle': wx.BRUSHSTYLE_SOLID,
                   'marker': 'circle',
                   'legend': ''}

    def __init__(self, points, **attr):
        """
        Creates PolyMarker object

        :param `points`: sequence (array, tuple or list) of (x,y) points
        :keyword `attr`: keyword attributes, default to:

         ================================ ================================
         'colour'= 'black'                wx.Pen Colour any wx.NamedColour
         'width'= 1                       Pen width
         'size'= 2                        Marker size
         'fillcolour'= same as colour     wx.Brush Colour any wx.NamedColour
         'fillstyle'= wx.BRUSHSTYLE_SOLID wx.Brush fill style (use wx.BRUSHSTYLE_TRANSPARENT for no fill)
         'style'= wx.FONTFAMILY_SOLID     wx.Pen style
         'marker'= 'circle'               Marker shape
         'legend'= ''                     Line Legend to display
         ================================ ================================

         Marker Shapes:
         - 'circle'
         - 'dot'
         - 'square'
         - 'triangle'
         - 'triangle_down'
         - 'cross'
         - 'plus'
        """

        PolyPoints.__init__(self, points, attr)

    def draw(self, dc, printerScale, coord=None):
        colour = self.attributes['colour']
        width = self.attributes['width'] * printerScale * self._pointSize[0]
        size = self.attributes['size'] * printerScale * self._pointSize[0]
        fillcolour = self.attributes['fillcolour']
        fillstyle = self.attributes['fillstyle']
        marker = self.attributes['marker']

        if colour and not isinstance(colour, wx.Colour):
            colour = wx.NamedColour(colour)
        if fillcolour and not isinstance(fillcolour, wx.Colour):
            fillcolour = wx.NamedColour(fillcolour)
            
        dc.SetPen(wx.Pen(colour, width))
        if fillcolour:
            dc.SetBrush(wx.Brush(fillcolour, fillstyle))
        else:
            dc.SetBrush(wx.Brush(colour, fillstyle))
        if coord == None:
            if len(self.scaled):  # bugfix for Mac OS X
                self._drawmarkers(dc, self.scaled, marker, size)
        else:
            self._drawmarkers(dc, coord, marker, size)  # draw legend marker
    
    @jit(nopython=True)
    def getSymExtent(self, printerScale):
        """Width and Height of Marker"""
        s = 5 * self.attributes['size'] * printerScale * self._pointSize[0]
        return (s, s)

    def _drawmarkers(self, dc, coords, marker, size=1):
        f = eval('self._' + marker)
        f(dc, coords, size)



class PlotGraphics:

    """Container to hold PolyXXX objects and graph labels
        - All methods except __init__ are private.
    """

    def __init__(self, objects, title='', xLabel='', yLabel=''):
        """Creates PlotGraphics object
        objects - list of PolyXXX objects to make graph
        title - title shown at top of graph
        xLabel - label shown on x-axis
        yLabel - label shown on y-axis
        """
        if type(objects) not in [list, tuple]:
            raise TypeError("objects argument should be list or tuple")
        self.objects = objects
        self.title = title
        self.xLabel = xLabel
        self.yLabel = yLabel
        self._pointSize = (1.0, 1.0)

    def setLogScale(self, logscale):
        if type(logscale) != tuple:
            raise TypeError(
                'logscale must be a tuple of bools, e.g. (False, False)')
        if len(self.objects) == 0:
            return
        for o in self.objects:
            o.setLogScale(logscale)

    
    def boundingBox(self):
        p1, p2 = self.objects[0].boundingBox()
        for o in self.objects[1:]:
            p1o, p2o = o.boundingBox()
            p1 = np.minimum(p1, p1o)
            p2 = np.maximum(p2, p2o)
        return p1, p2

    def scaleAndShift(self, scale=(1, 1), shift=(0, 0)):
        for o in self.objects:
            o.scaleAndShift(scale, shift)

    def setPrinterScale(self, scale):
        """Thickens up lines and markers only for printing"""
        self.printerScale = scale

    def setXLabel(self, xLabel=''):
        """Set the X axis label on the graph"""
        self.xLabel = xLabel

    def setYLabel(self, yLabel=''):
        """Set the Y axis label on the graph"""
        self.yLabel = yLabel

    def setTitle(self, title=''):
        """Set the title at the top of graph"""
        self.title = title

    def getXLabel(self):
        """Get x axis label string"""
        return self.xLabel

    def getYLabel(self):
        """Get y axis label string"""
        return self.yLabel

    def getTitle(self, title=''):
        """Get the title at the top of graph"""
        return self.title

    def draw(self, dc):
        for o in self.objects:
            # t=_time.clock()          # profile info
            o._pointSize = self._pointSize
            o.draw(dc, self.printerScale)
            #dt= _time.clock()-t
            #print(o, "time=", dt)

    def getSymExtent(self, printerScale):
        """Get max width and height of lines and markers symbols for legend"""
        self.objects[0]._pointSize = self._pointSize
        symExt = self.objects[0].getSymExtent(printerScale)
        for o in self.objects[1:]:
            o._pointSize = self._pointSize
            oSymExt = o.getSymExtent(printerScale)
            symExt = np.maximum(symExt, oSymExt)
        return symExt

    def getLegendNames(self):
        """Returns list of legend names"""
        lst = [None] * len(self)
        for i in range(len(self)):
            lst[i] = self.objects[i].getLegend()
        return lst

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, item):
        return self.objects[item]

class OpenGLCanvas(glcanvas.GLCanvas):
    def __init__(self,parent):
        glcanvas.GLCanvas.__init__(self,parent,-1)
        self.context = glcanvas.GLContext(self)
#-------------------------------------------------------------------------
# Main window that you will want to import into your application.

class PlotCanvas(wx.Panel):

    """
    Subclass of a wx.Panel which holds two scrollbars and the actual
    plotting canvas (self.canvas). It allows for simple general plotting
    of data with zoom, labels, and automatic axis scaling."""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name="plotCanvas"):
        """Constructs a panel, which can be a child of a frame or
        any other non-control window"""

        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        sizer = wx.FlexGridSizer(2, 2, 0, 0)
        self.canvas = OpenGLCanvas(self)
        self.sb_vert = wx.ScrollBar(self, -1, style=wx.SB_VERTICAL)
        self.sb_vert.SetScrollbar(0, 1000, 1000, 1000)
        self.sb_hor = wx.ScrollBar(self, -1, style=wx.SB_HORIZONTAL)
        self.sb_hor.SetScrollbar(0, 1000, 1000, 1000)

        sizer.Add(self.canvas, 1, wx.EXPAND)
        sizer.Add(self.sb_vert, 0, wx.EXPAND)
        sizer.Add(self.sb_hor, 0, wx.EXPAND)
        sizer.Add((0, 0))

        sizer.AddGrowableRow(0, 1)
        sizer.AddGrowableCol(0, 1)

        self.sb_vert.Show(False)
        self.sb_hor.Show(False)

        self.SetSizer(sizer)
        self.Fit()

        self.border = (1, 1)

        self.SetBackgroundColour("white")





        # set curser as cross-hairs
        self.canvas.SetCursor(wx.CROSS_CURSOR)
        self.HandCursor = wx.Cursor(Hand.GetImage())
        self.GrabHandCursor = wx.Cursor(GrabHand.GetImage())
        self.MagCursor = wx.Cursor(MagPlus.GetImage())

        # Things for printing
        self._print_data = None
        self._pageSetupData = None
        self.printerScale = 1
        self.parent = parent

        # scrollbar variables
        self._sb_ignore = False
        self._adjustingSB = False
        self._sb_xfullrange = 0
        self._sb_yfullrange = 0
        self._sb_xunit = 0
        self._sb_yunit = 0

        self._dragEnabled = False
        self._screenCoordinates = np.array([0.0, 0.0])

        self._logscale = (False, False)

        # Zooming variables
        self._zoomInFactor = 0.5
        self._zoomOutFactor = 2
        self._zoomCorner1 = np.array([0.0, 0.0])  # left mouse down corner
        self._zoomCorner2 = np.array([0.0, 0.0])   # left mouse up corner
        self._zoomEnabled = False
        self._hasDragged = False

        # Drawing Variables
        self.last_draw = None
        self._pointScale = 1
        self._pointShift = 0
        self._xSpec = 'auto'
        self._ySpec = 'auto'
        self._gridEnabled = False
        self._legendEnabled = False
        self._titleEnabled = True
        self._centerLinesEnabled = False
        self._diagonalsEnabled = False

        # Fonts
        self._fontCache = {}
        self._fontSizeAxis = 10
        self._fontSizeTitle = 15
        self._fontSizeLegend = 7

        # pointLabels
        self._pointLabelEnabled = False
        self.last_PointLabel = None
        self._pointLabelFunc = None
        self.canvas.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        if sys.platform != "darwin":
            self._logicalFunction = wx.EQUIV  # (NOT src) XOR dst
        else:
            # wx.EQUIV not supported on Mac OS X
            self._logicalFunction = wx.COPY

        self._useScientificNotation = False

        self._antiAliasingEnabled = False
        self._hiResEnabled = False
        self._pointSize = (1.0, 1.0)
        self._fontScale = 1.0

        self.canvas.Bind(wx.EVT_PAINT, self.OnPaint)
        self.canvas.Bind(wx.EVT_SIZE, self.OnSize)
        # OnSize called to make sure the buffer is initialized.
        # This might result in OnSize getting called twice on some
        # platforms at initialization, but little harm done.
        self.OnSize(None)  # sets the initial size based on client size

        self._gridColour = wx.BLACK

    def SetCursor(self, cursor):
        self.canvas.SetCursor(cursor)

    def GetGridColour(self):
        return self._gridColour

    def SetGridColour(self, colour):
        if isinstance(colour, wx.Colour):
            self._gridColour = colour
        else:
            self._gridColour = wx.NamedColour(colour)


    @property
    def print_data(self):
        if not self._print_data:
            self._print_data = wx.PrintData()
            self._print_data.SetPaperId(wx.PAPER_LETTER)
            self._print_data.SetOrientation(wx.LANDSCAPE)
        return self._print_data

    @property
    def pageSetupData(self):
        if not self._pageSetupData:
            self._pageSetupData = wx.PageSetupDialogData()
            self._pageSetupData.SetMarginBottomRight((25, 25))
            self._pageSetupData.SetMarginTopLeft((25, 25))
            self._pageSetupData.SetPrintData(self.print_data)
        return self._pageSetupData

    def PageSetup(self):
        """Brings up the page setup dialog"""
        data = self.pageSetupData
        data.SetPrintData(self.print_data)
        dlg = wx.PageSetupDialog(self.parent, data)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                data = dlg.GetPageSetupData()  # returns wx.PageSetupDialogData
                # updates page parameters from dialog
                self.pageSetupData.SetMarginBottomRight(
                    data.GetMarginBottomRight())
                self.pageSetupData.SetMarginTopLeft(data.GetMarginTopLeft())
                self.pageSetupData.SetPrintData(data.GetPrintData())
                self._print_data = wx.PrintData(
                    data.GetPrintData())  # updates print_data
        finally:
            dlg.Destroy()



    def setLogScale(self, logscale):
        if type(logscale) != tuple:
            raise TypeError(
                'logscale must be a tuple of bools, e.g. (False, False)')
        if self.last_draw is not None:
            graphics, xAxis, yAxis = self.last_draw
            graphics.setLogScale(logscale)
            self.last_draw = (graphics, None, None)
        self.SetXSpec('min')
        self.SetYSpec('min')
        self._logscale = logscale

    def getLogScale(self):
        return self._logscale

    def SetFontSizeAxis(self, point=10):
        """Set the tick and axis label font size (default is 10 point)"""
        self._fontSizeAxis = point

    def GetFontSizeAxis(self):
        """Get current tick and axis label font size in points"""
        return self._fontSizeAxis

    def SetFontSizeTitle(self, point=15):
        """Set Title font size (default is 15 point)"""
        self._fontSizeTitle = point

    def GetFontSizeTitle(self):
        """Get current Title font size in points"""
        return self._fontSizeTitle

    def SetFontSizeLegend(self, point=7):
        """Set Legend font size (default is 7 point)"""
        self._fontSizeLegend = point

    def GetFontSizeLegend(self):
        """Get current Legend font size in points"""
        return self._fontSizeLegend

    def SetShowScrollbars(self, value):
        """Set True to show scrollbars"""
        if value not in [True, False]:
            raise TypeError("Value should be True or False")
        if value == self.GetShowScrollbars():
            return
        self.sb_vert.Show(value)
        self.sb_hor.Show(value)
        wx.CallAfter(self.Layout)

    def GetShowScrollbars(self):
        """Set True to show scrollbars"""
        return self.sb_vert.IsShown()

    def SetUseScientificNotation(self, useScientificNotation):
        self._useScientificNotation = useScientificNotation

    def GetUseScientificNotation(self):
        return self._useScientificNotation

    def SetEnableAntiAliasing(self, enableAntiAliasing):
        """Set True to enable anti-aliasing."""
        self._antiAliasingEnabled = enableAntiAliasing
        self.Redraw()

    def GetEnableAntiAliasing(self):
        return self._antiAliasingEnabled

    def SetEnableHiRes(self, enableHiRes):
        """Set True to enable high-resolution mode when using anti-aliasing."""
        self._hiResEnabled = enableHiRes
        self.Redraw()

    def GetEnableHiRes(self):
        return self._hiResEnabled

    def SetEnableDrag(self, value):
        """Set True to enable drag."""
        if value not in [True, False]:
            raise TypeError("Value should be True or False")
        if value:
            if self.GetEnableZoom():
                self.SetEnableZoom(False)
            self.SetCursor(self.HandCursor)
        else:
            self.SetCursor(wx.CROSS_CURSOR)
        self._dragEnabled = value

    def GetEnableDrag(self):
        return self._dragEnabled

    def SetEnableZoom(self, value):
        """Set True to enable zooming."""
        if value not in [True, False]:
            raise TypeError("Value should be True or False")
        if value:
            if self.GetEnableDrag():
                self.SetEnableDrag(False)
            self.SetCursor(self.MagCursor)
        else:
            self.SetCursor(wx.CROSS_CURSOR)
        self._zoomEnabled = value

    def GetEnableZoom(self):
        """True if zooming enabled."""
        return self._zoomEnabled

    def SetEnableGrid(self, value):
        """Set True, 'Horizontal' or 'Vertical' to enable grid."""
        if value not in [True, False, 'Horizontal', 'Vertical']:
            raise TypeError(
                "Value should be True, False, Horizontal or Vertical")
        self._gridEnabled = value
        self.Redraw()

    def GetEnableGrid(self):
        """True if grid enabled."""
        return self._gridEnabled

    def SetEnableCenterLines(self, value):
        """Set True, 'Horizontal' or 'Vertical' to enable center line(s)."""
        if value not in [True, False, 'Horizontal', 'Vertical']:
            raise TypeError(
                "Value should be True, False, Horizontal or Vertical")
        self._centerLinesEnabled = value
        self.Redraw()

    def GetEnableCenterLines(self):
        """True if grid enabled."""
        return self._centerLinesEnabled

    def SetEnableDiagonals(self, value):
        """Set True, 'Bottomleft-Topright' or 'Bottomright-Topleft' to enable
        center line(s)."""
        if value not in [True, False, 'Bottomleft-Topright', 'Bottomright-Topleft']:
            raise TypeError(
                "Value should be True, False, Bottomleft-Topright or Bottomright-Topleft")
        self._diagonalsEnabled = value
        self.Redraw()

    def GetEnableDiagonals(self):
        """True if grid enabled."""
        return self._diagonalsEnabled

    def SetEnableLegend(self, value):
        """Set True to enable legend."""
        if value not in [True, False]:
            raise TypeError("Value should be True or False")
        self._legendEnabled = value
        self.Redraw()

    def GetEnableLegend(self):
        """True if Legend enabled."""
        return self._legendEnabled

    def SetEnableTitle(self, value):
        """Set True to enable title."""
        if value not in [True, False]:
            raise TypeError("Value should be True or False")
        self._titleEnabled = value
        self.Redraw()

    def GetEnableTitle(self):
        """True if title enabled."""
        return self._titleEnabled

    def SetEnablePointLabel(self, value):
        """Set True to enable pointLabel."""
        if value not in [True, False]:
            raise TypeError("Value should be True or False")
        self._pointLabelEnabled = value
        self.Redraw()  # will erase existing pointLabel if present
        self.last_PointLabel = None

    def GetEnablePointLabel(self):
        """True if pointLabel enabled."""
        return self._pointLabelEnabled

    def SetPointLabelFunc(self, func):
        """Sets the function with custom code for pointLabel drawing
            ******** more info needed ***************
        """
        self._pointLabelFunc = func

    def GetPointLabelFunc(self):
        """Returns pointLabel Drawing Function"""
        return self._pointLabelFunc

    def Reset(self):
        """Unzoom the plot."""
        self.last_PointLabel = None  # reset pointLabel
        if self.last_draw is not None:
            self._Draw(self.last_draw[0])

    def ScrollRight(self, units):
        """Move view right number of axis units."""
        self.last_PointLabel = None  # reset pointLabel
        if self.last_draw is not None:
            graphics, xAxis, yAxis = self.last_draw
            xAxis = (xAxis[0] + units, xAxis[1] + units)
            self._Draw(graphics, xAxis, yAxis)

    def ScrollUp(self, units):
        """Move view up number of axis units."""
        self.last_PointLabel = None  # reset pointLabel
        if self.last_draw is not None:
            graphics, xAxis, yAxis = self.last_draw
            yAxis = (yAxis[0] + units, yAxis[1] + units)
            self._Draw(graphics, xAxis, yAxis)

    def GetXY(self, event):
        """Wrapper around _getXY, which handles log scales"""
        x, y = self._getXY(event)
        if self.getLogScale()[0]:
            x = np.power(10, x)
        if self.getLogScale()[1]:
            y = np.power(10, y)
        return x, y

    def _getXY(self, event):
        """Takes a mouse event and returns the XY user axis values."""
        x, y = self.PositionScreenToUser(event.GetPosition())
        return x, y

    def PositionUserToScreen(self, pntXY):
        """Converts User position to Screen Coordinates"""
        userPos = np.array(pntXY)
        x, y = userPos * self._pointScale + self._pointShift
        return x, y

    def PositionScreenToUser(self, pntXY):
        """Converts Screen position to User Coordinates"""
        screenPos = np.array(pntXY)
        x, y = (screenPos - self._pointShift) / self._pointScale
        return x, y

    def SetXSpec(self, type='auto'):
        """xSpec- defines x axis type. Can be 'none', 'min' or 'auto'
        where:

        * 'none' - shows no axis or tick mark values
        * 'min' - shows min bounding box values
        * 'auto' - rounds axis range to sensible values
        * <number> - like 'min', but with <number> tick marks
        """
        self._xSpec = type

    def SetYSpec(self, type='auto'):
        """ySpec- defines x axis type. Can be 'none', 'min' or 'auto'
        where:

        * 'none' - shows no axis or tick mark values
        * 'min' - shows min bounding box values
        * 'auto' - rounds axis range to sensible values
        * <number> - like 'min', but with <number> tick marks
        """
        self._ySpec = type

    def GetXSpec(self):
        """Returns current XSpec for axis"""
        return self._xSpec

    def GetYSpec(self):
        """Returns current YSpec for axis"""
        return self._ySpec

    def GetXMaxRange(self):
        xAxis = self._getXMaxRange()
        if self.getLogScale()[0]:
            xAxis = np.power(10, xAxis)
        return xAxis

    def _getXMaxRange(self):
        """Returns (minX, maxX) x-axis range for displayed graph"""
        graphics = self.last_draw[0]
        p1, p2 = graphics.boundingBox()     # min, max points of graphics
        xAxis = self._axisInterval(self._xSpec, p1[0], p2[0])  # in user units
        return xAxis

    def GetYMaxRange(self):
        yAxis = self._getYMaxRange()
        if self.getLogScale()[1]:
            yAxis = np.power(10, yAxis)
        return yAxis

    def _getYMaxRange(self):
        """Returns (minY, maxY) y-axis range for displayed graph"""
        graphics = self.last_draw[0]
        p1, p2 = graphics.boundingBox()     # min, max points of graphics
        yAxis = self._axisInterval(self._ySpec, p1[1], p2[1])
        return yAxis

    def GetXCurrentRange(self):
        xAxis = self._getXCurrentRange()
        if self.getLogScale()[0]:
            xAxis = np.power(10, xAxis)
        return xAxis

    def _getXCurrentRange(self):
        """Returns (minX, maxX) x-axis for currently displayed portion of graph"""
        return self.last_draw[1]

    def GetYCurrentRange(self):
        yAxis = self._getYCurrentRange()
        if self.getLogScale()[1]:
            yAxis = np.power(10, yAxis)
        return yAxis

    def _getYCurrentRange(self):
        """Returns (minY, maxY) y-axis for currently displayed portion of graph"""
        return self.last_draw[2]

    def Draw(self, graphics, xAxis=None, yAxis=None, dc=None):
        """Wrapper around _Draw, which handles log axes"""

        graphics.setLogScale(self.getLogScale())

        # check Axis is either tuple or none
        if type(xAxis) not in [type(None), tuple]:
            raise TypeError(
                "xAxis should be None or (minX,maxX)" + str(type(xAxis)))
        if type(yAxis) not in [type(None), tuple]:
            raise TypeError(
                "yAxis should be None or (minY,maxY)" + str(type(xAxis)))

        # check case for axis = (a,b) where a==b caused by improper zooms
        if xAxis != None:
            if xAxis[0] == xAxis[1]:
                return
            if self.getLogScale()[0]:
                xAxis = np.log10(xAxis)
        if yAxis != None:
            if yAxis[0] == yAxis[1]:
                return
            if self.getLogScale()[1]:
                yAxis = np.log10(yAxis)
        self._Draw(graphics, xAxis, yAxis, dc)

    def _Draw(self, graphics, xAxis=None, yAxis=None, dc=None):
        """\
        Draw objects in graphics with specified x and y axis.
        graphics- instance of PlotGraphics with list of PolyXXX objects
        xAxis - tuple with (min, max) axis range to view
        yAxis - same as xAxis
        dc - drawing context - doesn't have to be specified.
        If it's not, the offscreen buffer is used
        """

        if dc == None:
            # sets new dc and clears it
            dc = wx.BufferedDC(wx.ClientDC(self.canvas), self._Buffer)
            bbr = wx.Brush(self.GetBackgroundColour(), wx.BRUSHSTYLE_SOLID)
            dc.SetBackground(bbr)
            dc.SetBackgroundMode(wx.SOLID)
            dc.Clear()
        if self._antiAliasingEnabled:
            if not isinstance(dc, wx.GCDC):
                try:
                    dc = wx.GCDC(dc)
                except Exception:
                    pass
                else:
                    if self._hiResEnabled:
                        # high precision - each logical unit is 1/20 of a point
                        dc.SetMapMode(wx.MM_TWIPS)
                    self._pointSize = tuple(
                        1.0 / lscale for lscale in dc.GetLogicalScale())
                    self._setSize()
        elif self._pointSize != (1.0, 1.0):
            self._pointSize = (1.0, 1.0)
            self._setSize()
        if (sys.platform in ("darwin", "win32") or not isinstance(dc, wx.GCDC) or wx.VERSION >= (2, 9)):
            self._fontScale = sum(self._pointSize) / 2.0
        else:
            # on Linux, we need to correct the font size by a certain factor if wx.GCDC is used,
            # to make text the same size as if wx.GCDC weren't used
            screenppi = map(float, wx.ScreenDC().GetPPI())
            ppi = dc.GetPPI()
            self._fontScale = (screenppi[
                               0] / ppi[0] * self._pointSize[0] + screenppi[1] / ppi[1] * self._pointSize[1]) / 2.0
        graphics._pointSize = self._pointSize

        dc.SetTextForeground(self.GetForegroundColour())
        dc.SetTextBackground(self.GetBackgroundColour())

        # dc.Clear()

        # set font size for every thing but title and legend
        dc.SetFont(self._getFont(self._fontSizeAxis))

        # sizes axis to axis type, create lower left and upper right corners of
        # plot
        if xAxis == None or yAxis == None:
            # One or both axis not specified in Draw
            p1, p2 = graphics.boundingBox()     # min, max points of graphics
            if xAxis == None:
                xAxis = self._axisInterval(
                    self._xSpec, p1[0], p2[0])  # in user units
            if yAxis == None:
                yAxis = self._axisInterval(self._ySpec, p1[1], p2[1])
            # Adjust bounding box for axis spec
            # lower left corner user scale (xmin,ymin)
            p1[0], p1[1] = xAxis[0], yAxis[0]
            # upper right corner user scale (xmax,ymax)
            p2[0], p2[1] = xAxis[1], yAxis[1]
        else:
            # Both axis specified in Draw
            # lower left corner user scale (xmin,ymin)
            p1 = np.array([xAxis[0], yAxis[0]])
            # upper right corner user scale (xmax,ymax)
            p2 = np.array([xAxis[1], yAxis[1]])

        # saves most recient values
        self.last_draw = (graphics, np.array(xAxis), np.array(yAxis))

        # Get ticks and textExtents for axis if required
        if self._xSpec != 'none':
            xticks = self._xticks(xAxis[0], xAxis[1])
        else:
            xticks = None
        if xticks:
            # w h of x axis text last number on axis
            xTextExtent = dc.GetTextExtent(xticks[-1][1])
        else:
            xTextExtent = (0, 0)  # No text for ticks
        if self._ySpec != 'none':
            yticks = self._yticks(yAxis[0], yAxis[1])
        else:
            yticks = None
        if yticks:
            if self.getLogScale()[1]:
                yTextExtent = dc.GetTextExtent('-2e-2')
            else:
                yTextExtentBottom = dc.GetTextExtent(yticks[0][1])
                yTextExtentTop = dc.GetTextExtent(yticks[-1][1])
                yTextExtent = (max(yTextExtentBottom[0], yTextExtentTop[0]),
                               max(yTextExtentBottom[1], yTextExtentTop[1]))
        else:
            yticks = None
            yTextExtent = (0, 0)  # No text for ticks

        # TextExtents for Title and Axis Labels
        titleWH, xLabelWH, yLabelWH = self._titleLablesWH(dc, graphics)

        # TextExtents for Legend
        legendBoxWH, legendSymExt, legendTextExt = self._legendWH(dc, graphics)

        # room around graph area
        # use larger of number width or legend width
        rhsW = max(xTextExtent[0], legendBoxWH[0]) + 5 * self._pointSize[0]
        lhsW = yTextExtent[0] + yLabelWH[1] + 3 * self._pointSize[0]
        bottomH = max(
            xTextExtent[1], yTextExtent[1] / 2.) + xLabelWH[1] + 2 * self._pointSize[1]
        topH = yTextExtent[1] / 2. + titleWH[1]
        # make plot area smaller by text size
        textSize_scale = np.array([rhsW + lhsW, bottomH + topH])
        # shift plot area by this amount
        textSize_shift = np.array([lhsW, bottomH])

        # draw title if requested
        if self._titleEnabled:
            dc.SetFont(self._getFont(self._fontSizeTitle))
            titlePos = (self.plotbox_origin[0] + lhsW + (self.plotbox_size[0] - lhsW - rhsW) / 2. - titleWH[0] / 2.,
                        self.plotbox_origin[1] - self.plotbox_size[1])
            dc.DrawText(graphics.getTitle(), titlePos[0], titlePos[1])

        # draw label text
        dc.SetFont(self._getFont(self._fontSizeAxis))
        xLabelPos = (self.plotbox_origin[0] + lhsW + (self.plotbox_size[0] - lhsW - rhsW) / 2. - xLabelWH[0] / 2.,
                     self.plotbox_origin[1] - xLabelWH[1])
        dc.DrawText(graphics.getXLabel(), xLabelPos[0], xLabelPos[1])
        yLabelPos = (self.plotbox_origin[0] - 3 * self._pointSize[0],
                     self.plotbox_origin[1] - bottomH - (self.plotbox_size[1] - bottomH - topH) / 2. + yLabelWH[0] / 2.)
        if graphics.getYLabel():  # bug fix for Linux
            dc.DrawRotatedText(
                graphics.getYLabel(), yLabelPos[0], yLabelPos[1], 90)

        # drawing legend makers and text
        if self._legendEnabled:
            self._drawLegend(
                dc, graphics, rhsW, topH, legendBoxWH, legendSymExt, legendTextExt)

        # allow for scaling and shifting plotted points
        scale = (self.plotbox_size - textSize_scale) / \
            (p2 - p1) * np.array((1, -1))
        shift = -p1 * scale + self.plotbox_origin + \
            textSize_shift * np.array((1, -1))
        # make available for mouse events
        self._pointScale = scale / self._pointSize
        self._pointShift = shift / self._pointSize
        self._drawAxes(dc, p1, p2, scale, shift, xticks, yticks)

        graphics.scaleAndShift(scale, shift)
        # thicken up lines and markers if printing
        graphics.setPrinterScale(self.printerScale)

        # set clipping area so drawing does not occur outside axis box
        ptx, pty, rectWidth, rectHeight = self._point2ClientCoord(p1, p2)
        # allow graph to overlap axis lines by adding units to width and height
        dc.SetClippingRegion(ptx * self._pointSize[0], pty * self._pointSize[
                             1], rectWidth * self._pointSize[0] + 2, rectHeight * self._pointSize[1] + 1)
        # Draw the lines and markers
        #start = _time.clock()
        graphics.draw(dc)
        # print("entire graphics drawing took: %f second"%(_time.clock() - start))
        # remove the clipping region
        dc.DestroyClippingRegion()

        self._adjustScrollbars()

    def Redraw(self, dc=None):
        """Redraw the existing plot."""
        if self.last_draw is not None:
            graphics, xAxis, yAxis = self.last_draw
            self._Draw(graphics, xAxis, yAxis, dc)

    def Clear(self):
        """Erase the window."""
        self.last_PointLabel = None  # reset pointLabel
        dc = wx.BufferedDC(wx.ClientDC(self.canvas), self._Buffer)
        bbr = wx.Brush(self.GetBackgroundColour(), wx.SOLID)
        dc.SetBackground(bbr)
        dc.SetBackgroundMode(wx.SOLID)
        dc.Clear()
        if self._antiAliasingEnabled:
            try:
                dc = wx.GCDC(dc)
            except Exception:
                pass
        dc.SetTextForeground(self.GetForegroundColour())
        dc.SetTextBackground(self.GetBackgroundColour())
        self.last_draw = None





    def UpdatePointLabel(self, mDataDict):
        """Updates the pointLabel point on screen with data contained in
            mDataDict.

            mDataDict will be passed to your function set by
            SetPointLabelFunc.  It can contain anything you
            want to display on the screen at the scaledXY point
            you specify.

            This function can be called from parent window with onClick,
            onMotion events etc.
        """
        if self.last_PointLabel != None:
            # compare pointXY
            if np.sometrue(mDataDict["pointXY"] != self.last_PointLabel["pointXY"]):
                # closest changed
                self._drawPointLabel(self.last_PointLabel)  # erase old
                self._drawPointLabel(mDataDict)  # plot new
        else:
            # just plot new with no erase
            self._drawPointLabel(mDataDict)  # plot new
        # save for next erase
        self.last_PointLabel = mDataDict

    # event handlers **********************************
    def OnMotion(self, event):
        if self._zoomEnabled and event.LeftIsDown():
            if self._hasDragged:
                self._drawRubberBand(
                    self._zoomCorner1, self._zoomCorner2)  # remove old
            else:
                self._hasDragged = True
            self._zoomCorner2[0], self._zoomCorner2[1] = self._getXY(event)
            self._drawRubberBand(
                self._zoomCorner1, self._zoomCorner2)  # add new
        elif self._dragEnabled and event.LeftIsDown():
            coordinates = event.GetPosition()
            newpos, oldpos = map(np.array, map(
                self.PositionScreenToUser, [coordinates, self._screenCoordinates]))
            dist = newpos - oldpos
            self._screenCoordinates = coordinates

            if self.last_draw is not None:
                graphics, xAxis, yAxis = self.last_draw
                yAxis -= dist[1]
                xAxis -= dist[0]
                self._Draw(graphics, xAxis, yAxis)



    def OnPaint(self, event):
        #self.SwapBuffers()
        # All that is needed here is to draw the buffer to screen
        if self.last_PointLabel != None:
            self._drawPointLabel(self.last_PointLabel)  # erase old
            self.last_PointLabel = None
        dc = wx.BufferedPaintDC(self.canvas, self._Buffer)
        if self._antiAliasingEnabled:
            try:
                dc = wx.GCDC(dc)
            except Exception:
                pass

    def OnSize(self, event):
        # The Buffer init is done here, to make sure the buffer is always
        # the same size as the Window
        Size = self.canvas.GetClientSize()
        Size.width = max(1, Size.width)
        Size.height = max(1, Size.height)

        # Make new offscreen bitmap: this bitmap will always have the
        # current drawing in it, so it can be used to save the image to
        # a file, or whatever.
        self._Buffer = wx.Bitmap(Size.width, Size.height)
        self._setSize()

        self.last_PointLabel = None  # reset pointLabel

        if self.last_draw is None:
            self.Clear()
        else:
            graphics, xSpec, ySpec = self.last_draw
            self._Draw(graphics, xSpec, ySpec)

    def OnLeave(self, event):
        """Used to erase pointLabel when mouse outside window"""
        if self.last_PointLabel != None:
            self._drawPointLabel(self.last_PointLabel)  # erase old
            self.last_PointLabel = None


    # Private Methods **************************************************
    def _setSize(self, width=None, height=None):
        """DC width and height."""
        if width == None:
            (self.width, self.height) = self.canvas.GetClientSize()
        else:
            self.width, self.height = width, height
        self.width *= self._pointSize[0]  # high precision
        self.height *= self._pointSize[1]  # high precision
        self.plotbox_size = 0.97 * np.array([self.width, self.height])
        xo = 0.5 * (self.width - self.plotbox_size[0])
        yo = self.height - 0.5 * (self.height - self.plotbox_size[1])
        self.plotbox_origin = np.array([xo, yo])

    def _setPrinterScale(self, scale):
        """Used to thicken lines and increase marker size for print out."""
        # line thickness on printer is very thin at 600 dot/in. Markers small
        self.printerScale = scale

    def _printDraw(self, printDC):
        """Used for printing."""
        if self.last_draw != None:
            graphics, xSpec, ySpec = self.last_draw
            self._Draw(graphics, xSpec, ySpec, printDC)

    def _drawPointLabel(self, mDataDict):
        """Draws and erases pointLabels"""
        width = self._Buffer.GetWidth()
        height = self._Buffer.GetHeight()
        if sys.platform != "darwin":
            tmp_Buffer = wx.EmptyBitmap(width,height)
            dcs = wx.MemoryDC()
            dcs.SelectObject(tmp_Buffer)
            dcs.Clear()
        else:
            tmp_Buffer = self._Buffer.GetSubBitmap((0, 0, width, height))
            dcs = wx.MemoryDC(self._Buffer)
        self._pointLabelFunc(dcs, mDataDict)  # custom user pointLabel function

        dc = wx.ClientDC(self.canvas)
        dc = wx.BufferedDC(dc, self._Buffer)
        # this will erase if called twice
        dc.Blit(0, 0, width, height, dcs, 0, 0, self._logicalFunction)
        if sys.platform == "darwin":
            self._Buffer = tmp_Buffer

    def _drawLegend(self, dc, graphics, rhsW, topH, legendBoxWH, legendSymExt, legendTextExt):
        """Draws legend symbols and text"""
        # top right hand corner of graph box is ref corner
        trhc = self.plotbox_origin + \
            (self.plotbox_size - [rhsW, topH]) * [1, -1]
        # border space between legend sym and graph box
        legendLHS = .091 * legendBoxWH[0]
        # 1.1 used as space between lines
        lineHeight = max(legendSymExt[1], legendTextExt[1]) * 1.1
        dc.SetFont(self._getFont(self._fontSizeLegend))
        for i in range(len(graphics)):
            o = graphics[i]
            s = i * lineHeight
            if isinstance(o, PolyMarker):
                # draw marker with legend
                pnt = (trhc[0] + legendLHS + legendSymExt[0] / 2.,
                       trhc[1] + s + lineHeight / 2.)
                o.draw(dc, self.printerScale, coord=np.array([pnt]))
            elif isinstance(o, PolyLine):
                # draw line with legend
                pnt1 = (trhc[0] + legendLHS, trhc[1] + s + lineHeight / 2.)
                pnt2 = (trhc[0] + legendLHS + legendSymExt[0],
                        trhc[1] + s + lineHeight / 2.)
                o.draw(dc, self.printerScale, coord=np.array([pnt1, pnt2]))
            else:
                raise TypeError(
                    "object is neither PolyMarker or PolyLine instance")
            # draw legend txt
            pnt = (trhc[0] + legendLHS + legendSymExt[0] + 5 * self._pointSize[0],
                   trhc[1] + s + lineHeight / 2. - legendTextExt[1] / 2)
            dc.DrawText(o.getLegend(), pnt[0], pnt[1])
        dc.SetFont(self._getFont(self._fontSizeAxis))  # reset

    def _titleLablesWH(self, dc, graphics):
        """Draws Title and labels and returns width and height for each"""
        # TextExtents for Title and Axis Labels
        dc.SetFont(self._getFont(self._fontSizeTitle))
        if self._titleEnabled:
            title = graphics.getTitle()
            titleWH = dc.GetTextExtent(title)
        else:
            titleWH = (0, 0)
        dc.SetFont(self._getFont(self._fontSizeAxis))
        xLabel, yLabel = graphics.getXLabel(), graphics.getYLabel()
        xLabelWH = dc.GetTextExtent(xLabel)
        yLabelWH = dc.GetTextExtent(yLabel)
        return titleWH, xLabelWH, yLabelWH

    def _legendWH(self, dc, graphics):
        """Returns the size in screen units for legend box"""
        if self._legendEnabled != True:
            legendBoxWH = symExt = txtExt = (0, 0)
        else:
            # find max symbol size
            symExt = graphics.getSymExtent(self.printerScale)
            # find max legend text extent
            dc.SetFont(self._getFont(self._fontSizeLegend))
            txtList = graphics.getLegendNames()
            txtExt = dc.GetTextExtent(txtList[0])
            for txt in graphics.getLegendNames()[1:]:
                txtExt = np.maximum(txtExt, dc.GetTextExtent(txt))
            maxW = symExt[0] + txtExt[0]
            maxH = max(symExt[1], txtExt[1])
            # padding .1 for lhs of legend box and space between lines
            maxW = maxW * 1.1
            maxH = maxH * 1.1 * len(txtList)
            dc.SetFont(self._getFont(self._fontSizeAxis))
            legendBoxWH = (maxW, maxH)
        return (legendBoxWH, symExt, txtExt)

    def _drawRubberBand(self, corner1, corner2):
        """Draws/erases rect box from corner1 to corner2"""
        ptx, pty, rectWidth, rectHeight = self._point2ClientCoord(
            corner1, corner2)
        # draw rectangle
        dc = wx.ClientDC(self.canvas)
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.SetBrush(wx.Brush(wx.WHITE, wx.BRUSHSTYLE_TRANSPARENT))
        dc.SetLogicalFunction(wx.INVERT)
        dc.DrawRectangle(ptx, pty, rectWidth, rectHeight)
        dc.SetLogicalFunction(wx.COPY)

    def _getFont(self, size):
        """Take font size, adjusts if printing and returns wx.Font"""
        s = size * self.printerScale * self._fontScale
        of = self.GetFont()
        # Linux speed up to get font from cache rather than X font server
        key = (int(s), of.GetFamily(), of.GetStyle(), of.GetWeight())
        font = self._fontCache.get(key, None)
        if font:
            return font                 # yeah! cache hit
        else:
            font = wx.Font(
                int(s), of.GetFamily(), of.GetStyle(), of.GetWeight())
            self._fontCache[key] = font
            return font

    def _point2ClientCoord(self, corner1, corner2):
        """Converts user point coords to client screen int coords x,y,width,height"""
        c1 = np.array(corner1)
        c2 = np.array(corner2)
        # convert to screen coords
        pt1 = c1 * self._pointScale + self._pointShift
        pt2 = c2 * self._pointScale + self._pointShift
        # make height and width positive
        pul = np.minimum(pt1, pt2)  # Upper left corner
        plr = np.maximum(pt1, pt2)  # Lower right corner
        rectWidth, rectHeight = plr - pul
        ptx, pty = pul
        return ptx, pty, rectWidth, rectHeight

    def _axisInterval(self, spec, lower, upper):
        """Returns sensible axis range for given spec"""
        if spec == 'none' or spec == 'min' or isinstance(spec, (float, int)):
            if lower == upper:
                return lower - 0.5, upper + 0.5
            else:
                return lower, upper
        elif spec == 'auto':
            range = upper - lower
            if range == 0.:
                return lower - 0.5, upper + 0.5
            log = np.log10(range)
            power = np.floor(log)
            fraction = log - power
            if fraction <= 0.05:
                power = power - 1
            grid = 10. ** power
            lower = lower - lower % grid
            mod = upper % grid
            if mod != 0:
                upper = upper - mod + grid
            return lower, upper
        elif type(spec) == type(()):
            lower, upper = spec
            if lower <= upper:
                return lower, upper
            else:
                return upper, lower
        else:
            raise ValueError(str(spec) + ': illegal axis specification')

    def _drawAxes(self, dc, p1, p2, scale, shift, xticks, yticks):

        # increases thickness for printing only
        penWidth = self.printerScale * self._pointSize[0]
        dc.SetPen(wx.Pen(self._gridColour, penWidth))

        # set length of tick marks--long ones make grid
        if self._gridEnabled:
            x, y, width, height = self._point2ClientCoord(p1, p2)
            if self._gridEnabled == 'Horizontal':
                yTickLength = (width / 2.0 + 1) * self._pointSize[1]
                xTickLength = 3 * self.printerScale * self._pointSize[0]
            elif self._gridEnabled == 'Vertical':
                yTickLength = 3 * self.printerScale * self._pointSize[1]
                xTickLength = (height / 2.0 + 1) * self._pointSize[0]
            else:
                yTickLength = (width / 2.0 + 1) * self._pointSize[1]
                xTickLength = (height / 2.0 + 1) * self._pointSize[0]
        else:
            # lengthens lines for printing
            yTickLength = 3 * self.printerScale * self._pointSize[1]
            xTickLength = 3 * self.printerScale * self._pointSize[0]

        if self._xSpec != 'none':
            lower, upper = p1[0], p2[0]
            text = 1
            # miny, maxy and tick lengths
            for y, d in [(p1[1], -xTickLength), (p2[1], xTickLength)]:
                for x, label in xticks:
                    pt = scale * np.array([x, y]) + shift
                    # draws tick mark d units
                    dc.DrawLine(pt[0], pt[1], pt[0], pt[1] + d)
                    if text:
                        dc.DrawText(
                            label, pt[0], pt[1] + 2 * self._pointSize[1])
                a1 = scale * np.array([lower, y]) + shift
                a2 = scale * np.array([upper, y]) + shift
                # draws upper and lower axis line
                dc.DrawLine(a1[0], a1[1], a2[0], a2[1])
                text = 0  # axis values not drawn on top side

        if self._ySpec != 'none':
            lower, upper = p1[1], p2[1]
            text = 1
            h = dc.GetCharHeight()
            for x, d in [(p1[0], -yTickLength), (p2[0], yTickLength)]:
                for y, label in yticks:
                    pt = scale * np.array([x, y]) + shift
                    dc.DrawLine(pt[0], pt[1], pt[0] - d, pt[1])
                    if text:
                        dc.DrawText(label, pt[0] - dc.GetTextExtent(label)[0] - 3 * self._pointSize[0],
                                    pt[1] - 0.75 * h)
                a1 = scale * np.array([x, lower]) + shift
                a2 = scale * np.array([x, upper]) + shift
                dc.DrawLine(a1[0], a1[1], a2[0], a2[1])
                text = 0    # axis values not drawn on right side

        if self._centerLinesEnabled:
            if self._centerLinesEnabled in ('Horizontal', True):
                y1 = scale[1] * p1[1] + shift[1]
                y2 = scale[1] * p2[1] + shift[1]
                y = (y1 - y2) / 2.0 + y2
                dc.DrawLine(
                    scale[0] * p1[0] + shift[0], y, scale[0] * p2[0] + shift[0], y)
            if self._centerLinesEnabled in ('Vertical', True):
                x1 = scale[0] * p1[0] + shift[0]
                x2 = scale[0] * p2[0] + shift[0]
                x = (x1 - x2) / 2.0 + x2
                dc.DrawLine(
                    x, scale[1] * p1[1] + shift[1], x, scale[1] * p2[1] + shift[1])

        if self._diagonalsEnabled:
            if self._diagonalsEnabled in ('Bottomleft-Topright', True):
                dc.DrawLine(scale[0] * p1[0] + shift[0], scale[1] * p1[1] +
                            shift[1], scale[0] * p2[0] + shift[0], scale[1] * p2[1] + shift[1])
            if self._diagonalsEnabled in ('Bottomright-Topleft', True):
                dc.DrawLine(scale[0] * p1[0] + shift[0], scale[1] * p2[1] +
                            shift[1], scale[0] * p2[0] + shift[0], scale[1] * p1[1] + shift[1])

    def _xticks(self, *args):
        if self._logscale[0]:
            return self._logticks(*args)
        else:
            attr = {'numticks': self._xSpec}
            return self._ticks(*args, **attr)

    def _yticks(self, *args):
        if self._logscale[1]:
            return self._logticks(*args)
        else:
            attr = {'numticks': self._ySpec}
            return self._ticks(*args, **attr)

    def _logticks(self, lower, upper):
        #lower,upper = map(np.log10,[lower,upper])
        # print('logticks',lower,upper)
        ticks = []
        mag = np.power(10, np.floor(lower))
        if upper - lower > 6:
            t = np.power(10, np.ceil(lower))
            base = np.power(10, np.floor((upper - lower) / 6))

            def inc(t):
                return t * base - t
        else:
            t = np.ceil(np.power(10, lower) / mag) * mag

            def inc(t):
                return 10 ** int(np.floor(np.log10(t) + 1e-16))
        majortick = int(np.log10(mag))
        while t <= pow(10, upper):
            if majortick != int(np.floor(np.log10(t) + 1e-16)):
                majortick = int(np.floor(np.log10(t) + 1e-16))
                ticklabel = '1e%d' % majortick
            else:
                if upper - lower < 2:
                    minortick = int(t / pow(10, majortick) + .5)
                    ticklabel = '%de%d' % (minortick, majortick)
                else:
                    ticklabel = ''
            ticks.append((np.log10(t), ticklabel))
            t += inc(t)
        if len(ticks) == 0:
            ticks = [(0, '')]
        return ticks

    def _ticks(self, lower, upper, numticks=None):
        if isinstance(numticks, (float, int)):
            ideal = (upper - lower) / float(numticks)
        else:
            ideal = (upper - lower) / 7.
        log = np.log10(ideal)
        power = np.floor(log)
        if isinstance(numticks, (float, int)):
            grid = ideal
        else:
            fraction = log - power
            factor = 1.
            error = fraction
            for f, lf in self._multiples:
                e = np.fabs(fraction - lf)
                if e < error:
                    error = e
                    factor = f
            grid = factor * 10. ** power
        if self._useScientificNotation and (power > 4 or power < -4):
            format = '%+7.1e'
        elif power >= 0:
            digits = max(1, int(power))
            format = '%' + repr(digits) + '.0f'
        else:
            digits = -int(power)
            format = '%' + repr(digits + 2) + '.' + repr(digits) + 'f'
        ticks = []
        t = -grid * np.floor(-lower / grid)
        while t <= upper:
            if t == -0:
                t = 0
            ticks.append((t, format % (t,)))
            t = t + grid
        return ticks

    _multiples = [(2., np.log10(2.)), (5., np.log10(5.))]

    def _adjustScrollbars(self):
        if self._sb_ignore:
            self._sb_ignore = False
            return

        if not self.GetShowScrollbars():
            return

        self._adjustingSB = True
        needScrollbars = False

        # horizontal scrollbar
        r_current = self._getXCurrentRange()
        r_max = list(self._getXMaxRange())
        sbfullrange = float(self.sb_hor.GetRange())

        r_max[0] = min(r_max[0], r_current[0])
        r_max[1] = max(r_max[1], r_current[1])

        self._sb_xfullrange = r_max

        unit = (r_max[1] - r_max[0]) / float(self.sb_hor.GetRange())
        pos = int((r_current[0] - r_max[0]) / unit)

        if pos >= 0:
            pagesize = int((r_current[1] - r_current[0]) / unit)

            self.sb_hor.SetScrollbar(pos, pagesize, sbfullrange, pagesize)
            self._sb_xunit = unit
            needScrollbars = needScrollbars or (pagesize != sbfullrange)
        else:
            self.sb_hor.SetScrollbar(0, 1000, 1000, 1000)

        # vertical scrollbar
        r_current = self._getYCurrentRange()
        r_max = list(self._getYMaxRange())
        sbfullrange = float(self.sb_vert.GetRange())

        r_max[0] = min(r_max[0], r_current[0])
        r_max[1] = max(r_max[1], r_current[1])

        self._sb_yfullrange = r_max

        unit = (r_max[1] - r_max[0]) / sbfullrange
        pos = int((r_current[0] - r_max[0]) / unit)

        if pos >= 0:
            pagesize = int((r_current[1] - r_current[0]) / unit)
            pos = (sbfullrange - 1 - pos - pagesize)
            self.sb_vert.SetScrollbar(pos, pagesize, sbfullrange, pagesize)
            self._sb_yunit = unit
            needScrollbars = needScrollbars or (pagesize != sbfullrange)
        else:
            self.sb_vert.SetScrollbar(0, 1000, 1000, 1000)

        self.SetShowScrollbars(needScrollbars)
        self._adjustingSB = False

#-------------------------------------------------------------------------

#----------------------------------------------------------------------
from wx.lib.embeddedimage import PyEmbeddedImage

MagPlus = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAOFJ"
    "REFUeJy1VdEOxCAIo27//8XbuKfuPASGZ0Zisoi2FJABbZM3bY8c13lo5GvbjioBPAUEB0Yc"
    "VZ0iGRRc56Ee8DcikEgrJD8EFpzRegQASiRtBtzuA0hrdRPYQxaEKyJPG6IHyiK3xnNZvUSS"
    "NvUuzgYh0il4y14nCFPk5XgmNbRbQbVotGo9msj47G3UXJ7fuz8Q8FAGEu0/PbZh2D3NoshU"
    "1VUydBGVZKMimlGeErdNGUmf/x7YpjMjcf8HVYvS2adr6aFVlCy/5Ijk9q8SeCR9isJR8SeJ"
    "8pv7S0Wu2Acr0qdj3w7DRAAAAABJRU5ErkJggg==")

GrabHand = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAARFJ"
    "REFUeJy1VdESgzAIS2j//4s3s5fRQ6Rad5M7H0oxCZhWSpK1TjwUBCBJAIBItL1fijlfe1yJ"
    "8noCGC9KgrXO7f0SyZEDAF/H2opsAHv9V/548nplT5Jo7YAFQKQ1RMWzmHUS96suqdBrHkuV"
    "uxpdJjCS8CfGXWdJ2glzcquKSR5c46QOtCpgNyIHj6oieAXg3282QvMX45hy8a8H0VonJZUO"
    "clesjOPg/dhBTq64o1Kacz4Ri2x5RKsf8+wcWQaJJL+A+xRcZHeQeBKjK+5EFiVJ4xy4x2Mn"
    "1Vk4U5/DWmfPieiqbye7a3tV/cCsWKu76K76KUFFchVnhigJ/hmktelm/m3e3b8k+Ec8PqLH"
    "CT4JRfyK9o1xYwAAAABJRU5ErkJggg==")

Hand = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAARBJ"
    "REFUeJytluECwiAIhDn1/Z942/UnjCGoq+6XNeWDC1xAqbKr6zyo61Ibds60J8GBT0yS3IEM"
    "ABuIpJTa4IOLiAAQksuKyixLH1ShHgTgZl8KiALxOsODPoEMkgJ25Su6zoO3ZrjRnI96OLIq"
    "k7dsqOCboDa4XV/nwQEQVeFtmMnvbSJja+oagKBUaLn9hzd7VipRa9ostIv0O1uhzzaqNJxk"
    "hViwDVxqg51kksMg9r2rDDIFwHCap130FBhdMzeAfWg//6Ki5WWQrHSv6EIUeVs0g3wT3J7r"
    "FmWQp/JJDXeRh2TXcJa91zAH2uN2mvXFsrIrsjS8rnftWmWfAiLIStuD9m9h9belvzgS/1fP"
    "X7075IwDENteAAAAAElFTkSuQmCC")

#---------------------------------------------------------------------------
# if running standalone...
#
#     ...a sample implementation using the above
#

