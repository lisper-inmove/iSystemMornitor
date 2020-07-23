# -*- coding: utf-8 -*-


import os
import sys


uname = os.uname()
system = uname.sysname
system = system.lower()
if system not in ("linux",):
    print("只支持在linux下使用")
    sys.exit()
