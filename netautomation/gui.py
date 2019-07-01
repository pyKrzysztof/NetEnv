import wx

FONT_SIZE = 12


class DeviceNotBoundException(Exception):
    pass


class NetEnv(wx.App):
    pass

class ConsoleFrame(wx.Frame):

    def __init__(self, device, **kwargs):
        super().__init__(**kwargs)
        if not device:
            raise DeviceNotBoundException
        self.device = device
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
        # self.SetBackgroundColour('black')

        font = wx.Font()
        font.SetPointSize(FONT_SIZE)

        style = wx.TE_MULTILINE | wx.TE_READONLY | wx.NO_BORDER
        self.console = wx.TextCtrl(self, size=(600, 400), style=style)
        # self.console.SetBackgroundColour('black')
        # self.console.SetForegroundColour('white')
        self.console.SetFont(font)

        self.input_field = wx.TextCtrl(self, size=(600, 20), style=wx.TE_LEFT|wx.TE_NO_VSCROLL|wx.TE_PROCESS_ENTER|wx.NO_BORDER)
        # self.input_field.SetBackgroundColour('#434343')
        # self.input_field.SetForegroundColour('white')
        self.input_field.SetFont(font)
        self.input_field.WriteText(self.GetParent().device.get_prompt())

        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sizer.Add(self.console, 1, flag=wx.EXPAND|wx.ALL, border=5)
        self.sizer.Add(self.input_field, 0, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=1)
        self.SetSizer(self.sizer)
        self.Layout()

        self.input_field.Bind(wx.EVT_TEXT_ENTER, self.on_enter_pressed)

    def write_to_console(self, stdin, stdout):
        if stdin:
            self.console.AppendText(stdin)
        if stdout:
            self.console.AppendText(stdout)

    def on_enter_pressed(self, e):
        input_field = e.GetEventObject()
        content = input_field.GetValue()
        index = content.find(' ')
        host, command = content[:index], content[index:]
        stdout = self.GetParent().device.send_command(command)
        stdin = host + command + '\n'
        if stdout:    stdout = stdout + '\n'
        self.write_to_console(stdin, stdout)
        input_field.SetValue('')
        input_field.WriteText(self.GetParent().device.get_prompt())