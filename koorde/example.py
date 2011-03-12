# author Pedro Garcia Lopez, PhD (pedro.garcia@urv.net)

from koorde import *

n0 = Node(0)
n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n4 = Node(4)
n5 = Node(5)
n6 = Node(6)
n7 = Node(7)

n0.join(n0)
n1.join(n0)
n2.join(n0)
n3.join(n0)
n4.join(n0)
n5.join(n0)
n6.join(n0)
n7.join(n0)


import koorde
koorde.DEBUG = True
n2.findSuccessor(6)

toPajek(n0,'koord.net')
toPajek2(n0,'koord2.net')


