# author Pedro Garcia Lopez, PhD (pedro.garcia@urv.net)

import skip
from skip import *

skip.k = 6
skip.MAX = 2**skip.k
nodes = []
for i in range(skip.MAX/2):
    num=i+2
    nodes.append(Node(i,num))
for node in nodes:
    node.join(nodes[0])



toPajek(nodes[0],'skip2.net')
