import wx


FONT_SIZE = 12

class ConsoleFrame(wx.Panel):

    def __init__(self, device, **kwargs):
        super().__init__(**kwargs)

        self.bound_device = device

        font = wx.Font()
        font.SetPointSize(FONT_SIZE)

        style = wx.TE_MULTILINE | wx.TE_READONLY | wx.NO_BORDER
        self.console = wx.TextCtrl(self, size=(600, 400), style=style)
        self.console.SetBackgroundColour('black')
        self.console.SetForegroundColour('white')
        self.console.SetFont(font)

        self.input_field = wx.TextCtrl(self, size=(600, 20), style=wx.TE_LEFT|wx.TE_NO_VSCROLL|wx.TE_PROCESS_ENTER|wx.NO_BORDER)
        self.input_field.SetBackgroundColour('black')
        self.input_field.SetForegroundColour('white')
        self.input_field.SetFont(font)

        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sizer.Add(self.console, 1, flag=wx.EXPAND|wx.ALL, border=5)
        self.sizer.Add(self.input_field, 0, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.SetSizer(self.sizer)
        self.Layout()