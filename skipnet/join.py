# author Pedro Garcia Lopez, PhD (pedro.garcia@urv.net)

from skip import *

n0 = Node(0,0)
n5 = Node(5,5)
n1 = Node(1,1)
n0.join(n0)
n5.join(n0)
n1.join(n0)
print n0.RouteTable
print '----------------------'
print n1.RouteTable
print '----------------------'
print n5.RouteTable
