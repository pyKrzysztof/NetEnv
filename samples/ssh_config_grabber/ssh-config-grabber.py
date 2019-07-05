import wx
import sys
import time
import os

path = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), '..'), '..'))
sys.path.insert(0, path)

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

        self.statusbar = self.CreateStatusBar(1)

        self.Fit()
        self.SetMinClientSize((self.GetSize().Width + 100, self.GetSize().Height))
        self.Fit()
        self.Refresh()

class MainPanel(wx.Panel):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.sizer = wx.GridBagSizer()
        self.parent = self.GetParent()

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
        self.execute_button.Bind(wx.EVT_BUTTON, self.execute)

        self.get_vlan_data_checkbox = wx.CheckBox(self, label=' get vlan data', style=wx.NO_BORDER)
        self.get_vlan_data_checkbox.SetFont(font)
        self.get_vlan_data_checkbox.SetValue(True)
        self.get_config_checkbox = wx.CheckBox(self, label=' get config', style=wx.NO_BORDER)
        self.get_config_checkbox.SetFont(font)
        self.get_config_checkbox.SetValue(True)

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

    def execute(self, event):
        if self.get_vlan_data_checkbox.GetValue():
            result = self.get_vlans()
            if result:
                self.parent.statusbar.SetStatusText('vlan.dat created successfuly.')
            else:
                self.parent.statusbar.SetStatusText("Couldn't get vlan info.")
        if self.get_config_checkbox.GetValue():
            self.get_config()
            if result:
                self.parent.statusbar.SetStatusText('config.text created successfuly.')
            else:
                self.parent.statusbar.SetStatusText("Couldn't get config info.")
        time.sleep(1)
        self.parent.statusbar.SetStatusText('Done.')

    def get_vlans(self):
        device = SSHDevice(self.address_field.GetValue())
        device.set_credentials(
            self.username_field.GetValue(), 
            self.password_field.GetValue()
        )
        connected = device.connect()

        if connected == AUTH_ERROR:    return 0
        elif connected == GENERAL_FAILURE:    return 0

        vlan_data = device.send_command('more flash:vlan.dat')
        device.client.close()
        with open('vlan.dat', 'w') as f:
            f.write(vlan_data)
        return 1

    def get_config(self):
        device = SSHDevice(self.address_field.GetValue())
        device.set_credentials(
            self.username_field.GetValue(), 
            self.password_field.GetValue()
        )
        connected = device.connect()

        if connected == AUTH_ERROR:    return 0
        elif connected == GENERAL_FAILURE:    return 0

        config = device.send_command('more flash:config.text')
        device.client.close()
        with open('config.text', 'w') as f:
            f.write(config)
        return 1

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None).Show()
    app.MainLoop()