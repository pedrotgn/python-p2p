# author Pedro Garcia Lopez, PhD (pedro.garcia@urv.net)

from math import log

b = 3
size = 2**b


def bin2dec(bits):
    size = len(bits)-1
    result = 0
    for bit in bits:
        result = result + int(bit)*(2**size)
        size = size -1
    return result


def dec2bin2(dec,top=b):
    result = ''
    remainder = dec
    if (dec == 0):
            for i in range(top):
                result = result + '0'
            return result
    for i in range(top-1,-1,-1):
        result = result+ str(remainder/2**i)
        remainder = remainder % 2**i
    return result


def toPajek(graph, filename):
    f = open(filename,'w')
    size = len(graph)
    f.write('*Vertices '+str(size)+'\n')
    for i in graph:
        f.write(' '+str(i+1)+' "'+str(i)+'"\n')
    f.write('*Arcs\n')
    for i in graph:
        for conn in graph[i]:
            f.write(' '+str(i+1)+' '+str(conn+1)+' 1\n')
    f.close()

def toPajek2(graph, filename):
    f = open(filename,'w')
    size = len(graph)
    f.write('*Vertices '+str(size)+'\n')
    for i in graph:
        f.write(' '+str(i+1)+' "'+str(dec2bin2(i,b))+'"\n')
    f.write('*Arcs\n')
    for i in graph:
        for conn in graph[i]:
            f.write(' '+str(i+1)+' '+str(conn+1)+' 1\n')
    f.close()

def topBit(elem):
    bit = 2**(b-1)
    topBi = 0
    if elem & bit == bit:
        topBi = 1
    return topBi

def route(src,dst):
    result = [src]
    k = dst
    t = src
    if src==dst:
        return result
    while (t!=dst):
        t = (t<<1)%size + topBit(k)
        result.append(t)
        k = (k<<1)%size
    return result


graph = {}
for i in range(size):
    graph[i]=[]
    graph[i].append((i<<1)%size)
    graph[i].append(((i<<1)+1)%size)

toPajek(graph,'bruijn.net')
toPajek2(graph,'bruijn2.net')


print route(2,6)
print map(dec2bin2,route(2,6))
