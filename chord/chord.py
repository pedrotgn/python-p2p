# author: Pedro Garcia Lopez, PhD

import random

k = 6
MAX = 2**k


def decr(value,size):
    if size <= value:
        return value - size
    else:
        return MAX-(size-value)
        

def between(value,init,end):
    if init == end:
        return True
    elif init > end :
        shift = MAX - init
        init = 0
        end = (end +shift)%MAX
        value = (value + shift)%MAX
    return init < value < end

def Ebetween(value,init,end):
    if value == init:
        return True
    else:
        return between(value,init,end)

def betweenE(value,init,end):
    if value == end:
        return True
    else:
        return between(value,init,end)


class Node:
    def __init__(self,id):
        self.id = id
        self.finger = {}
        self.start = {}
        for i in range(k):
            self.start[i] = (self.id+(2**i)) % (2**k)

    def successor(self):
        return self.finger[0]
    
    def find_successor(self,id):  
        if betweenE(id,self.predecessor.id,self.id):
            return self
        n = self.find_predecessor(id)
        return n.successor()
    
    def find_predecessor(self,id):
        if id == self.id:
            return self.predecessor
        n1 = self
        while not betweenE(id,n1.id,n1.successor().id):
            n1 = n1.closest_preceding_finger(id)
        return n1
    
    def closest_preceding_finger(self,id):
        for i in range(k-1,-1,-1):
            if between(self.finger[i].id,self.id,id):
                return self.finger[i]
        return self
        
    
    def join(self,n1):
        if self == n1:
            for i in range(k):
                self.finger[i] = self
            self.predecessor = self
        else:
            self.init_finger_table(n1)
            self.update_others()  
           # Move keys !!! 
            
    def init_finger_table(self,n1):
        self.finger[0] = n1.find_successor(self.start[0])
        self.predecessor = self.successor().predecessor
        self.successor().predecessor = self
        self.predecessor.finger[0] = self
        for i in range(k-1):
            if Ebetween(self.start[i+1],self.id,self.finger[i].id):
                self.finger[i+1] = self.finger[i]
            else :
                self.finger[i+1] = n1.find_successor(self.start[i+1])

    def update_others(self):
        for i in range(k):
            prev  = decr(self.id,2**i)
            p = self.find_predecessor(prev)
            if prev == p.successor().id:
                p = p.successor()
            p.update_finger_table(self,i)
            
    def update_finger_table(self,s,i):
        if Ebetween(s.id,self.id,self.finger[i].id) and self.id!=s.id:
                self.finger[i] = s
                p = self.predecessor
                p.update_finger_table(s,i)

    def update_others_leave(self):
        for i in range(k):
            prev  = decr(self.id,2**i)
            p = self.find_predecessor(prev)
            p.update_finger_table(self.successor(),i)
    # not checked 
    def leave(self):
        self.successor().predecessor = self.predecessor
        self.predecessor.setSuccessor(self.successor())
        self.update_others_leave()
        
    def setSuccessor(self,succ):
        self.finger[0] = succ
        

def hash(line):
    import sha
    key=long(sha.new(line).hexdigest(),16)
    return key
    

def id():
    return long(random.uniform(0,2**k))


def printNodes(node):
    print ' Ring nodes:'
    end = node
    print node.id
    while end != node.successor():
        node = node.successor()
        print node.id
    print '-----------'

def showFinger(node):
    print 'Finger table of node ' + str(node.id)
    print 'start:node'
    for i in range(k):
        print str(node.start[i]) +' : ' +str(node.finger[i].id)  
    print '-----------'


# ----------------------The next functions are related to Pajek file generation ---------------------

def node2graph(node):
    graph = {}
    addNode(graph,node)
    current = node.successor()
    while current!=node:    
        graph[current.id] = []
        addNode(graph,current)
        current = current.successor()
    return graph

def addNode(graph,node):
    graph[node.id] = []
    for n in node.finger.values():
        graph[node.id].append(n.id)

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


def toPajek2(node, filename):
    graph = node2graph(node)
    f = open(filename,'w')
    size = len(graph)
    f.write('*Vertices '+str(size)+'\n')
    for i in range(size):
        id1 = dec2bin2(graph.keys()[i],k)
        f.write(' '+str(i+1)+' "'+str(id1)+'"\n')
    f.write('*Arcs\n')
    for i in graph:
        for conn in graph[i]:
            f.write(' '+str(graph.keys().index(i)+1)+' '+str(graph.keys().index(conn)+1)+' 1\n')
    f.close()




