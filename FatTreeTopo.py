from mininet.topo import Topo

class FatTreeTopo(Topo):
    "Fat-Tree Topology"

    def build(self, k=4):
        if k % 2 != 0 or k <= 0:
            raise ValueError("k should be a positive even number.")

        # Core switches
        core_switches = []
        for i in range(1, (k//2) + 1):
            for j in range(1, (k//2) + 1):
                sw = self.addSwitch('c{:02d}{:02d}'.format(i, j), dpid='00:00:00:00:00:{:02x}:{:02x}:01'.format(k, i*10+j))
                core_switches.append(sw)

        # Pods
        for pod in range(k):
            # Aggregation switches in this pod
            aggregation_switches = []
            for agg in range(k//2, k):
                sw = self.addSwitch('a{:02d}{:02d}'.format(pod, agg), dpid='00:00:00:00:00:{:02x}:{:02x}:01'.format(pod, agg))
                aggregation_switches.append(sw)
                # Connect to core switches
                for c in range((agg - k//2) * (k//2), (agg - k//2 + 1) * (k//2)):
                    self.addLink(aggregation_switches[-1], core_switches[c])

            # Edge switches in this pod
            for edge in range(k//2):
                sw = self.addSwitch('e{:02d}{:02d}'.format(pod, edge), dpid='00:00:00:00:00:{:02x}:{:02x}:01'.format(pod, edge))
                # Connect to aggregation switches
                for agg_sw in aggregation_switches:
                    self.addLink(sw, agg_sw)

                # Hosts in this edge switch
                for h in range(2, (k//2) + 2):
                    host = self.addHost('h{:02d}{:02d}{:02d}'.format(pod, edge, h), ip='10.{:d}.{:d}.{:d}'.format(pod, edge, h))
                    self.addLink(sw, host)

def make_fat_tree(k):
    topo = FatTreeTopo(k=k)
    return topo

topos = {'fat_tree': (lambda k=4: make_fat_tree(k))}
