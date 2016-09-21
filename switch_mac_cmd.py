#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @brief:     switch_mac_cmd.py  交换机mac相关命令
# @author:    zhukunbo@ruijie.com.cn
# @version:   1.0
# @date:      2016-09-06

import time
import string

from cases_set.bridge.brg_com_cmd import *
from libcom.lib_pub.logging_drv import log_info
from libcom.lib_cmd.inter_mode import *
from libcom.lib_cmd.config_mode import *
from libcom.lib_cmd.shell_mode import *
from libcom.lib_cmd.chg_mode import *
from libcom.device_adapt.device_adapt import *
from libcom.device_adapt.nt_adapt import *
from libcom.packet_drv.Tester import *
from libcom.console_drv.console_drv import *
from libcom.config_topo.topo_controller import *

class SwitchRuijie(object):
    'switch class mathod'

    def show_mac(self, *args):
        cmd = "show rookie mac-address-table "
        for member in args:
            cmd = cmd + str(member)
        return run_cmd(self.sw_name, cmd)

    def add_static_addr(self, addr, vid, port):
        configure(self.sw_name)
        cmd = "rookie " + "mac-address-table static " + str(addr) + " vlan " + str(vid) \
              + " interface " + " GigabitEthernet " + str(port)
        run_cmd(self.sw_name, cmd)
        run_cmd(self.sw_name, "exit")

    def set_age_time(self, timer):
        configure(self.sw_name)
        cmd = "rookie " + "mac-address-table age-time " + str(timer)
        run_cmd(self.sw_name, cmd)
        run_cmd(self.sw_name, "exit")

    def set_global_learn(self, status):
        configure(self.sw_name)
        cmd = "rookie " + "mac-address-learing " + str(status)
        run_cmd(self.sw_name, cmd)
        run_cmd(self.sw_name, "exit")

    def clear_addr_entry(self, *args):
        cmd = "clear rookie mac-address-table "
        for member in args :
            cmd = cmd + str(member)
        run_cmd(self.sw_name, cmd)

    def __init__(self, sw_name):
        self.sw_name = sw_name
