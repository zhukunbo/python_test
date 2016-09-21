#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @brief:     switch_mac_base_3.py - 测试交换机老化时间
# @author:    zhukunbo@ruijie.com.cn
# @version:   1.0
# @date:      2016-09-04

import time
import string

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

__all__ = ["switch_mac_base_3"]

SUCCESS = 0
FAIL = -1

def switch_mac_base_3(cb_arg):
    result = 0

    nt_name = cb_arg.nt_names[0]
    dev_name = cb_arg.dev_names[0]
    wake_up_console(dev_name)

    active_intf = list()
    get_sw_active_intf(dev_name, active_intf)

    nt_active_inft = list()
    nt_active_inft = NTAdapter.get_intf_key_list(nt_name)
    nt_send_pt_key = nt_active_inft[1]
    nt_send_pt = NTAdapter.get_intf_name(nt_name, nt_send_pt_key)
    total_send_pkt = '2000'
    nt_ip = get_nt_ip(nt_name)
    nt_usrname = get_nt_usrname(nt_name)

    # configure nettester
    te = Tester()
    te.ConnectTester(nt_ip)
    te.TesterLogin(nt_usrname)
    te.TakeOwnership(nt_send_pt)
    te.ResetPort(nt_send_pt)
    medium3 = get_intf_medium(nt_name, nt_send_pt_key)
    te.interface_config(nt_send_pt, "config", phy_mode=medium3)
    te.traffic_config(nt_send_pt, "create", rate_pps="1000", transmit_mode="single_burst",pkts_per_burst=total_send_pkt,
        mac_dst="00.00.00.00.00.01", mac_src="00.00.00.00.00.11", mac_src_mode="increment", mac_src_step="1",
        mac_src_count="100", l3_protocol="ipv4", ip_dst_addr="1.1.1.1", ip_src_addr="1.1.1.2")
    te.CloseConnect()
    time.sleep(10)

    # clear dynamic mac address and send packet
    enable(dev_name)
    sw = SwitchRuijie(dev_name)
    sw.clear_addr_entry("dynamic")
    # 设置定时时间为100s
    sw.set_age_time("100")
    sw.show_mac("age-time")

    time.sleep(10)
    te = Tester()
    te.ConnectTester(nt_ip)
    te.TesterLogin(nt_usrname)
    te.TakeOwnership(nt_send_pt)
    te.traffic_control(nt_send_pt, "run")
    te.CloseConnect()
    time.sleep(30)

    sw.show_mac("count")
    sw.show_mac("count")
    time.sleep(150)
    print "90s later ,show syn entry"
    sw.show_mac("count")
    sw.show_mac("count")

    # 恢复配置
    sw.set_age_time("300")
    sw.clear_addr_entry("dynamic")

    print "age time test is over"

    return result
