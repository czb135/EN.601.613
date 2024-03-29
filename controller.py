'''
Please add your name:
Please add your matric number: 
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.addresses import IPAddr
import pox.openflow.discovery
import pox.openflow.spanning_tree

log = core.getLogger()

class SDNFirewall(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        self.firewall_rules = []
        self.premium_hosts = []
        self.load_policies("policy.in")

    def load_policies(self, filename):
        with open(filename, 'r') as f:
            n, m = map(int, f.readline().split())
            for _ in range(n):
                line = f.readline().strip()
                if ',' in line:
                    parts = line.split(',')
                    if len(parts) == 2: # dst_ip,dst_port
                        self.firewall_rules.append((None, parts[0], int(parts[1])))
                    elif len(parts) == 3: # src_ip,dst_ip,dst_port
                        self.firewall_rules.append((parts[0], parts[1], int(parts[2])))
            for _ in range(m):
                line = f.readline().strip()
                self.premium_hosts.append(line)

    def install_firewall_rule(self, event, src_ip, dst_ip, dst_port):
        match = of.ofp_match()
        match.dl_type = 0x0800 # IP protocol
        match.nw_proto = 6 # TCP protocol
        if src_ip:
            match.nw_src = IPAddr(src_ip)
        match.nw_dst = IPAddr(dst_ip)
        match.tp_dst = dst_port
        fm = of.ofp_flow_mod()
        fm.match = match
        fm.priority = 65535 # Highest priority
        fm.actions.append(of.ofp_action_output(port = of.OFPP_NONE)) # Drop
        event.connection.send(fm)

    def _handle_ConnectionUp(self, event):
        for rule in self.firewall_rules:
            self.install_firewall_rule(event, *rule)
        # Configure QoS for premium hosts here if necessary
        # ...

def launch():
    core.registerNew(SDNFirewall)
