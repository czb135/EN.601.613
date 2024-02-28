from mininet.topo import Topo

class FatTreeTopo(Topo):
    def __init__(self, k=4, **opts):
        """Initialize custom Fat-tree topology with parameter k"""
        Topo.__init__(self, **opts)

        # Validate k to be even
        if k % 2 != 0:
            raise Exception("k value should be even")

        # Initialize core, aggregation, and edge switches and hosts
        core_switches = []
        aggregation_switches = []
        edge_switches = []
        hosts = []

        # Create core switches
        for i in range((k//2)**2):
            core_switch = self.addSwitch('c{}'.format(i))
            core_switches.append(core_switch)

        # Create pods with aggregation and edge switches and hosts
        for pod in range(k):
            pod_aggregation_switches = []
            pod_edge_switches = []
            pod_hosts = []
            
            # Create aggregation switches
            for agg in range(k//2):
                aggregation_switch = self.addSwitch('a{}_{}'.format(pod, agg))
                pod_aggregation_switches.append(aggregation_switch)
                aggregation_switches.append(aggregation_switch)
            
            # Create edge switches and hosts
            for edge in range(k//2):
                edge_switch = self.addSwitch('e{}_{}'.format(pod, edge))
                pod_edge_switches.append(edge_switch)
                edge_switches.append(edge_switch)
                
                # Create hosts and connect them to the edge switches
                for h in range(k//2):
                    host = self.addHost('h{}_{}_{}'.format(pod, edge, h))
                    pod_hosts.append(host)
                    hosts.append(host)
                    self.addLink(edge_switch, host)

            # Interconnect aggregation and edge switches
            for agg_switch in pod_aggregation_switches:
                for edge_switch in pod_edge_switches:
                    self.addLink(agg_switch, edge_switch)

        # Interconnect core switches to aggregation switches
        for i, core_switch in enumerate(core_switches):
            for j, agg_switch in enumerate(aggregation_switches):
                if j // (k//2) == i % (k//2):
                    self.addLink(core_switch, agg_switch)

# If your script is being executed (not imported), run the topology:
if __name__ == '__main__':
    from mininet.net import Mininet
    from mininet.log import setLogLevel, info
    from mininet.cli import CLI

    def runFatTree():
        "Bootstrap a Mininet network using the FatTree topology"

        topo = FatTreeTopo(k=4)
        net = Mininet(topo=topo)
        net.start()

        # You can insert code here that does something with the network before the CLI

        CLI(net)  # Start the Mininet CLI
        net.stop()  # Stop the network

    # Tell mininet to print useful information
    setLogLevel('info')
    runFatTree()
