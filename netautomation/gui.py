import wx

class NetEnv(wx.App):
    pass

class ConsoleFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display()

    def display(self):
        self.SetBackgroundColour('black')
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.panel = ConsolePanel(self)
        self.sizer.Add(self.panel)
        self.Layout()

class ConsolePanel(wx.Panel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        style = wx.TE_MULTILINE | wx.TE_READONLY
        self.console = wx.TextCtrl(self, size=(600, 400), style=style)
        
        input_field = wx.TextCtrl(self, size=(600, 20), style=wx.TE_LEFT|wx.TE_NO_VSCROLL)
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sizer.Add(self.console, 1, flag=wx.EXPAND|wx.ALL, border=5)
        self.sizer.Add(input_field, 0, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.SetSizer(self.sizer)
        self.Layout()

    def write_to_console(self, stdin, stdout):
        if stdin:
            self.console.AppendText(stdin)
        if stdout:
            self.console.AppendText(stdout)

    def on_enter_pressed(self, e):
        self.write_to_console()

# class MyForm(wx.Frame):
 
#     def __init__(self):
#         wx.Frame.__init__(self, None, 
#                           title="wxPython Redirect Tutorial")
 
#         # Add a panel so it looks the correct on all platforms
#         panel = wx.Panel(self, wx.ID_ANY)
#         style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL
#         log = wx.TextCtrl(panel, wx.ID_ANY, size=(300,100),
#                           style=style)
#         btn = wx.Button(panel, wx.ID_ANY, 'Push me!')
#         self.Bind(wx.EVT_BUTTON, self.onButton, btn)
 
#         # Add widgets to a sizer
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(log, 1, wx.ALL|wx.EXPAND, 5)
#         sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
#         panel.SetSizer(sizer)
 
#         # redirect text here
#         sys.stdout=log
 
#     def onButton(self, event):
#         print("You pressed the button!")