# author Pedro Garcia Lopez, PhD (pedro.garcia@urv.net)

from skip import *


n0 = Node(0,0)
n1 = Node(1,1)
n2 = Node(2,2)
n3 = Node(3,3)
n4 = Node(4,4)
n5 = Node(5,5)
n6 = Node(6,6)
n7 = Node(7,7)


n0.join(n0)
n1.join(n0)
n2.join(n0)
n3.join(n0)
n4.join(n0)
n5.join(n0)
n6.join(n0)
n7.join(n0)


print n0.RouteTable
print '----------------------'
print n1.RouteTable
print '----------------------'
print n2.RouteTable
print '----------------------'
print n3.RouteTable
print '----------------------'
print n4.RouteTable
print '----------------------'
print n5.RouteTable
print '----------------------'
print n5.RouteTable
print '----------------------'
print n7.RouteTable