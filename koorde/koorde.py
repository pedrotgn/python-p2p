# author Pedro Garcia Lopez, PhD (pedro.garcia@urv.net)

k = 3
MAX = 2**k
DEBUG = False

class Node:
    def __init__(self,id):
        self.id = id
        
    def join(self,node):
        if node == self:
            self.successor = self
            self.predecessor = self
            self.d = self
        else:
            enter = node.findSuccessor(self.id)
            self.successor = enter
            self.predecessor = enter.predecessor
            enter.predecessor.successor = self
            enter.predecessor = self
            self.d = enter.findSuccessor((2*self.id)% MAX)
            self.updateOther()
            
    def findSuccessor(self,id):
        #i = self.nextHop(id)
        i = self.bestHop(id)
        return self.lookup(id,id,i)
    
    def updateOther(self):
        pred = self.predecessor.id + 1
        prednode = (pred>>1)%8
        if (prednode<<1)%8==pred:
            updatenode = self.findSuccessor(prednode)
            updatenode.d = self
    
    def lookup(self,k,kshift,i):
        if DEBUG:
            print 'lookup in node '+str(self.id)+' with key '+str(k) + ' and i= ' + str(i)
            print dec2bin2(k,3),dec2bin2(kshift,3), dec2bin2(i,3)
        if betweenE(k,self.id, self.successor.id):
                return self.successor
        elif betweenE(i,self.id, self.successor.id):
            return self.d.lookup(k,(kshift<<1)%MAX,(i<<1)%MAX+topBit(kshift))
        else:
            return self.successor.lookup(k,kshift,i)
         
    def nextHop(self,key):
        return (self.id<<1)%MAX+topBit(key)
    
    def bestHop(self,key):
        bruijn = []
        tmp = self.id
        for i in range(k-1):
            next = (tmp<<1)%MAX+topBit(key)
            bruijn.append(next)
            key = (key << 1)%MAX
            tmp = next
        bruijn.reverse()
        i = 0
        while not betweenE(bruijn[i],self.id, self.successor.id) and i>0:
            i = i + 1
        
        return bruijn[i]
        
        
            
    def updateD(self):
        self.d = self.findSuccessor((2*self.id)% MAX)
    
    def __repr__(self):
        return '('+str(self.id)+','+str(self.successor.id)+','+str(self.d.id)+')'


def topBit(elem):
    bit = 2**(k-1) 
    if elem & bit == bit:
        return 1
    else:
        return 0 

def between(value,init,end):
    if init == end:
        return True
    elif init > end :
        shift = MAX - init
        init = 0
        end = (end +shift)%MAX
        value = (value + shift)%MAX
    return init < value < end

def betweenE(value,init,end):
    if value == end:
        return True
    else:
        return between(value,init,end)
    
def Ebetween(value,init,end):
    if value == init:
        return True
    else:
        return between(value,init,end)
    
def dec2bin2(dec,top):
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

def half (num):
    if num==0:
        return MAX
    else:
        return num/2


# ----------------------The next functions are related to Pajek file generation ---------------------

def node2graph(node):
    graph = {}
    addNode(graph,node)
    current = node.successor
    while current!=node:    
        addNode(graph,current)
        current = current.successor
    return graph

def addNode(graph,node):
    graph[node.id] = []
    graph[node.id].append(node.successor.id)
    graph[node.id].append(node.d.id)
        
def toPajek(node, filename):
    graph = node2graph(node)
    f = open(filename,'w')
    size = len(graph)
    f.write('*Vertices '+str(size)+'\n')
    for i in range(size):
        f.write(' '+str(i+1)+' "'+str(graph.keys()[i])+'"\n')
    f.write('*Arcs\n')
    for i in graph:
        for conn in graph[i]:
            f.write(' '+str(graph.keys().index(i)+1)+' '+str(graph.keys().index(conn)+1)+' 1\n')
    f.close()
    
def toPajek2(node, filename):
    graph = node2graph(node)
    f = open(filename,'w')
    size = len(graph)
    f.write('*Vertices '+str(size)+'\n')
    for i in range(size):
        f.write(' '+str(i+1)+' "'+dec2bin2(graph.keys()[i],k)+'"\n')
    f.write('*Arcs\n')
    for i in graph:
        for conn in graph[i]:
            f.write(' '+str(graph.keys().index(i)+1)+' '+str(graph.keys().index(conn)+1)+' 1\n')
    f.close()