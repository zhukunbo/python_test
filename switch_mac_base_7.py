#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @brief:     switch_mac_base_7.py - 测试交换机批PI进程重启
# @author:    zhukunbo@ruijie.com.cn
# @version:   1.0
# @date:      2016-09-04

import time
import string
import random

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
from cases_set.bridge.brg_com_cmd import *
from cases_set.bridge.mac.mac_com_cmd import *
from switch_mac_cmd import SwitchRuijie

__all__ = ["switch_mac_base_7"]

SUCCESS = 0
FAIL = -1

def switch_mac_base_7(cb_arg):
    result = 0

    dev_name = cb_arg.dev_names[0]
    wake_up_console(dev_name)

    # 设置老化时间为400
    enable(dev_name)
    sw = SwitchRuijie(dev_name)
    sw.set_age_time("400")
    sw.show_mac("aging-time")

    time.sleep(1)
    # 杀死进程
    run_cmd(dev_name, 'en')
    time.sleep(1)
    run_cmd(dev_name, 'run-system-shell')
    time.sleep(1)
    run_cmd(dev_name, 'killall -9 se.elf')
    time.sleep(5)
    run_cmd(dev_name, './se.elf &')
    time.sleep(10)
    run_cmd(dev_name, 'exit')


    # 重新查看老化时间
    sw.show_mac("age-time")
    sw.show_mac()

    print "pi reboot test is over "

    return result
