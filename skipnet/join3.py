# author Pedro Garcia Lopez, PhD (pedro.garcia@urv.net)

from skip import *

import skip
skip.k = 6

n0 = Node(0,0)
n1 = Node(1,2)
n2 = Node(2,4)
n3 = Node(3,6)
n4 = Node(4,8)
n5 = Node(5,10)
n6 = Node(6,12)
n7 = Node(7,14)


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

##import skip
##skip.DEBUG = True

msg = Msg()
msg.operation = findKey
n2.SendMsg(6,msg)
n2.RouteByNumericID(12,msg)


toPajek(n0,'skip.net')
