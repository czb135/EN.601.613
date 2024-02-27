#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def create_topology():
    net = Mininet(controller=Controller, switch=OVSSwitch, link=TCLink)

    # Add controller
    net.addController('c0')

    # Add switches
    core_switch = net.addSwitch('c1')
    aggregation_switches = [net.addSwitch('a1'), net.addSwitch('a2')]
    edge_switches = [net.addSwitch('e1'), net.addSwitch('e2'), net.addSwitch('e3'), net.addSwitch('e4')]

    # Add hosts
    hosts = [net.addHost('h%d' % n) for n in range(1, 9)]

    # Create links between core switch and aggregation switches
    for agg_switch in aggregation_switches:
        net.addLink(core_switch, agg_switch)

    # Create links between aggregation switches and edge switches
    for i, edge_switch in enumerate(edge_switches):
        net.addLink(aggregation_switches[i // 2], edge_switch)

    # Create links between edge switches and hosts
    for i, host in enumerate(hosts):
        net.addLink(edge_switches[i // 2], host)

    # Start the network
    net.build()
    net.start()

    # Run CLI
    CLI(net)

    # After the user exits the CLI, stop the network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_topology()
