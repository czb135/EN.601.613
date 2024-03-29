'''
Your name:
Your matric number:
'''

import sys
from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.topo import Topo

class CustomTopo(Topo):
    def build(self, input_file='topology.in'):
        # Read the topology input file
        with open(input_file, 'r') as f:
            lines = f.readlines()

        # Parse the first line for the number of hosts and switches
        n_hosts, n_switches, n_links = map(int, lines[0].split())

        # Add switches
        for i in range(1, n_switches + 1):
            self.addSwitch('s%d' % i)

        # Add hosts
        for i in range(1, n_hosts + 1):
            self.addHost('h%d' % i, ip='10.0.0.%d' % i)

        # Add links
        for line in lines[1:]:
            endpoints = line.strip().split(',')
            self.addLink(endpoints[0], endpoints[1])

if __name__ == '__main__':
    setLogLevel('info')

    # Allow custom topology input file as an argument
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'topology.in'
    topo = CustomTopo(input_file=input_file)

    # Create the network
    net = Mininet(topo=topo, controller=Controller, switch=OVSSwitch, link=TCLink)
    net.start()

    # Start the command-line interface
    CLI(net)

    # Stop the network
    net.stop()
