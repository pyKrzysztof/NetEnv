from context import *

from netautomation import Automation

import os

auto = Automation()
path = os.path.join(os.path.dirname(__file__), 'automation.json')
auto.set_file(path)

auto.get_script('new vlan')