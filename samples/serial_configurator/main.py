import os
import sys
import time
import wx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), '..'), '..')))

from netautomation import SerialDevice
from netautomation import Handler
from netautomation import WRONG_PORT
from netautomation import AUTH_ERROR
from netautomation import GENERAL_FAILURE


MIN_WIDTH = 350 + 600
MIN_HEIGHT = 300 + 300


def get_default_port():
    if sys.platform == 'win32':
        return 'COM0'
    if sys.platform == 'linux':


class Connection:

    def __init__(self, port, baudrate, username=None, password=None):
        self.device = SerialDevice(port, baudrate)
        self.handler = Handler()
        self.handler.bind_device(self.device)
        if username and password:
            self.device.set_credentials(username, password)

    def open_connection(self):
        is_connected = self.device.connect()
        if is_connected == 1:
            return True
        else:
            self.set_hint(is_connected)
            self.device.close()
            del self.device
            del self.handler
            return False

    def set_hint(self, error_value):
        if error_value == AUTH_ERROR:
            self._hint = 'Authentication error.'
        elif error_value == WRONG_PORT:
            self._hint = 'No serial device on this port.'
        elif self._hint == GENERAL_FAILURE:
            self._hint = 'General failure.'

    def get_hint(self):
        return self._hint


class Frame(wx.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._hint = None
        self._connection = None

        self.SetTitle('Serial Configurator')
        self.SetSize((MIN_WIDTH, MIN_HEIGHT))
        self.SetMinSize((MIN_WIDTH, MIN_HEIGHT))
        self.display()

    def display(self):
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panel = ConnectionPanel(self)
        self.hsizer.Add(self.panel, 0, flag=wx.ALIGN_CENTER)
        self.vsizer.Add(self.hsizer, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(self.vsizer)
        self.Fit()

    def set_connection(self, connection):
        self._connection = connection

    def connect(self, port, baudrate, username, password):
        connection = Connection(port, baudrate, username, password)
        is_connected = connection.open_connection()
        if not is_connected:
            return connection.get_hint()




class ConnectionPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.sizer = wx.GridBagSizer()

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.erase_background)
        
        big_font = wx.Font()
        big_font.SetPointSize(16)
        self.title = wx.StaticText(self, label='Connect to Serial Port', style=wx.TEXT_ALIGNMENT_CENTER)
        self.title.SetFont(big_font)
        self.sizer.Add(self.title, pos=(0, 0), span=(1, 4), flag=wx.ALIGN_CENTER|wx.ALL, border=10)

        font = wx.Font()
        font.SetPointSize(12)
        self.port_st = wx.StaticText(self, label='Port:')
        self.port_st.SetFont(font)
        self.port = wx.TextCtrl(self)
        self.port.SetFont(font)
        default_port = get_default_port()
        self.port.SetValue(default_port)
        self.port.SetMinClientSize((150, 22))
        self.sizer.Add(self.port_st, pos=(2, 0), span=(1, 1), flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT, border=10)
        self.sizer.Add(self.port, pos=(2, 1), span=(1, 1))

        self.bd_st = wx.StaticText(self, label='Baudrate:')
        self.bd_st.SetFont(font)
        self.bd = wx.TextCtrl(self, value='9600')
        self.bd.SetFont(font)
        self.bd.SetMinClientSize((150, 22))
        self.sizer.Add(self.bd_st, pos=(3, 0), span=(1, 1), flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT, border=10)
        self.sizer.Add(self.bd, pos=(3, 1), span=(1, 1))

        self.un_st = wx.StaticText(self, label='Username:')
        self.un_st.SetFont(font)
        self.un = wx.TextCtrl(self)
        self.un.SetFont(font)
        self.un.SetMinClientSize((150, 22))
        self.sizer.Add(self.un_st, pos=(5, 0), span=(1, 1), flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT, border=10)
        self.sizer.Add(self.un, pos=(5, 1), span=(1, 1))

        self.pd_st = wx.StaticText(self, label='Password:')
        self.pd_st.SetFont(font)
        self.pd = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        self.pd.SetFont(font)
        self.pd.SetMinClientSize((150, 22))
        self.sizer.Add(self.pd_st, pos=(6, 0), span=(1, 1), flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT, border=10)
        self.sizer.Add(self.pd, pos=(6, 1), span=(1, 1))

        self.hint = wx.StaticText(self, label='')
        self.hint.SetForegroundColour('red')
        self.sizer.Add(self.hint, pos=(8, 0), span=(1, 4), flag=wx.ALIGN_CENTER)

        self.connect_bt = wx.Button(self, label='Connect')
        self.connect_bt.Bind(wx.EVT_BUTTON, self.button_pressed)
        self.sizer.Add(self.connect_bt, pos=(9, 0), span=(1, 4), flag=wx.ALIGN_CENTER|wx.BOTTOM, border=10)

        for i in range(4):
            self.sizer.AddGrowableCol(i)

        self.SetSizer(self.sizer)
        self.Layout()

    def button_pressed(self, e):
        self.hint.SetLabel('')
        hint = self.parent.connect(self.port.GetValue(), self.bd.GetValue(),
                                   self.un.GetValue(), self.pd.GetValue())
        if not hint:
            return
        self.hint.SetLabel(hint)
        self.Layout()

    def erase_background(self, e):
        pass

    def on_paint(self, e):
        dc = wx.BufferedPaintDC(self)
        self.draw(dc)

    def draw(self, dc):
        dc.Clear()
        dc.SetPen(wx.Pen('black', 1))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, self.GetSize().Width, self.GetSize().Height)

def start_gui():
    app = wx.App()
    frame = Frame(None).Show()
    app.MainLoop()

if __name__ == '__main__':
    start_gui()


