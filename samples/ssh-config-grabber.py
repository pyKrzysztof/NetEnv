import wx

from context import *
from netautomation import SSHDevice
from netautomation import AUTH_ERROR
from netautomation import GENERAL_FAILURE


FONTSIZE = 16


class MyFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.SetTitle('SSH Config Grabber')
        self.panel = MainPanel(self)
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()
        self.SetMinClientSize((self.GetSize().Width + 100, self.GetSize().Height))

class MainPanel(wx.Panel):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.sizer = wx.GridBagSizer()

        font = wx.Font()
        font.SetPointSize(FONTSIZE)

        address_string = wx.StaticText(self, label='Host:', style=wx.ALIGN_CENTER_VERTICAL)
        address_string.SetFont(font)
        username_string = wx.StaticText(self, label='Username:')
        username_string.SetFont(font)
        password_string = wx.StaticText(self, label='Password:')
        password_string.SetFont(font)
        self.address_field = wx.TextCtrl(self)
        self.address_field.SetFont(font)
        self.username_field = wx.TextCtrl(self)
        self.username_field.SetFont(font)
        self.password_field = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        self.password_field.SetFont(font)
        self.execute_button = wx.Button(self, label='Execute')

        self.get_vlan_data_checkbox = wx.CheckBox(self, label=' get vlan data', style=wx.NO_BORDER)
        self.get_vlan_data_checkbox.SetFont(font)
        self.get_config_checkbox = wx.CheckBox(self, label=' get config', style=wx.NO_BORDER)
        self.get_config_checkbox.SetFont(font)

        self.sizer.Add(address_string, pos=(0, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=20)
        self.sizer.Add(username_string, pos=(1, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=20)
        self.sizer.Add(password_string, pos=(2, 0), flag=wx.EXPAND|wx.ALL, border=20)
        self.sizer.Add(self.address_field, pos=(0, 1), span=(1, 2), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=20)
        self.sizer.Add(self.username_field, pos=(1, 1), span=(1, 2), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=20)
        self.sizer.Add(self.password_field, pos=(2, 1), span=(1, 2), flag=wx.EXPAND|wx.ALL, border=20)

        self.sizer.Add(self.get_vlan_data_checkbox, pos=(3, 0), span=(1, 3), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=40)
        self.sizer.Add(self.get_config_checkbox, pos=(4, 0), span=(1, 3), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=40)
        self.sizer.Add((-1, 30), pos=(5, 0), span=(1, 3), flag=wx.EXPAND)
        self.sizer.Add(self.execute_button, pos=(6, 0), span=(1, 3), flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, border=5)
        
        self.sizer.AddGrowableCol(2)
        for i in range(5):
            self.sizer.AddGrowableRow(i)

        self.SetSizer(self.sizer)
        self.Layout()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None).Show()
    app.MainLoop()