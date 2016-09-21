#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @brief:     switch_mac_base_1.py - 测试交换机静态MAC地址
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

__all__ = ["switch_mac_base_1"]

SUCCESS = 0
FAIL = -1

# 清除端口统计值
def clear_pt_count(dev_name):
    enable(dev_name)
    run_cmd(dev_name, "clear counters")

# 向测试交换机发包
def snd_untag_pkt(nt_name, nt_send_pt_key, str_mac_dst, total_send_pkt):
    nt_send_pt = NTAdapter.get_intf_name(nt_name, nt_send_pt_key)
    nt_ip = get_nt_ip(nt_name)
    nt_usrname = get_nt_usrname(nt_name)

    te = Tester()
    te.ConnectTester(nt_ip)
    te.TesterLogin(nt_usrname)
    te.TakeOwnership(nt_send_pt)
    te.ResetPort(nt_send_pt)
    medium1 = get_intf_medium(nt_name, nt_send_pt_key)
    te.interface_config(nt_send_pt, "config", phy_mode=medium1)
    te.traffic_config(nt_send_pt, "create", rate_pps="1000", transmit_mode="single_burst",
                      pkts_per_burst=str(total_send_pkt), mac_dst=str_mac_dst, mac_src="00.00.00.00.00.01",
                      mac_src_mode="increment",
                      mac_src_step="1", mac_src_count=str(total_send_pkt), l3_protocol="ipv4", ip_dst_addr="1.1.1.1",
                      ip_src_addr="1.1.1.2")
    te.CloseConnect()
    time.sleep(10)

    te.ConnectTester(nt_ip)
    te.TesterLogin(nt_usrname)
    te.traffic_control(nt_send_pt, "run")
    te.CloseConnect()

def switch_mac_base_1(cb_arg):
    result = 0

    dev_name = cb_arg.dev_names[0]
    wake_up_console(dev_name)

    active_intf = list()
    get_sw_active_intf(dev_name, active_intf)
    rev_port = 'intf' + active_intf[0]
    out_port = 'intf' + active_intf[1]
    out_port_1 = 'intf' + active_intf[2]

    static_addr = '1010.2255.4466'
    vid = '1'
    # 添加静态地址
    sw = SwitchRuijie(dev_name)
    sw.add_static_addr(static_addr, vid, active_intf[1])
    print '添加静态地址：'
    # 显示静态地址
    sw.show_mac("static")

    nt_name = cb_arg.nt_names[0]
    nt_active_inft = NTAdapter.get_intf_key_list(nt_name)
    nt_send_pt_key = nt_active_inft[0]
    total_send_pkt = 2000
    snd_untag_pkt(nt_name, nt_send_pt_key, convert_mac_addr(static_addr, 1), total_send_pkt)
    time.sleep(30)

    pkt_count_in = get_spec_pt_count(dev_name, rev_port, True, 0)
    pkt_count_out1 = get_spec_pt_count(dev_name, out_port, False, 0)
    pkt_count_out2 = get_spec_pt_count(dev_name, out_port_1, False, 0)

    print "package in num %d " % pkt_count_in
    print "package out num %d" % pkt_count_out1
    print "package leak out num %d" % pkt_count_out2

    # 恢复配置
    sw.clear_addr_entry("vlan ", "1")

    print "static test is over"
    return result
