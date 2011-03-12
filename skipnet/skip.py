# author Pedro Garcia Lopez, PhD (pedro.garcia@urv.net)

import random

k = 3
MAX = 2**k
clockwise = 0
counterclockwise = 1
findTopLevelRing = 2
findKey = 3
updateRings = 4
DEBUG = False

class Msg:
    pass
class Node:
    def __init__(self,nameID=-1,numID=-1):
        self.nameID = nameID
        self.RouteTable = {0:{},1:{}}
        self.maxHeight = k-1
        self.numID = numID
        
    def initRoutingTable(self,nodes):
        for i in range(k):
            self.RouteTable[clockwise][i] = nodes[(self.nameID + (2**i))%MAX]
            self.RouteTable[counterclockwise][i] = nodes[(self.nameID - (2**i))%MAX]

    
    def join (self,node):
        for i in range(self.maxHeight+1):
            self.RouteTable[clockwise][i]= self
            self.RouteTable[counterclockwise][i]= self
        if node==self:
            return             
        else:
            node.insertNode(self)
        

    def RouteByNameID(self,msg):
        h = self.maxHeight
        if msg.nameID ==self.nameID:
            h = -1
        while h>=0:
            nbr = self.RouteTable[msg.dir][h]
            if LiesBetween(self.nameID,nbr.nameID,msg.nameID,msg.dir):
                if DEBUG:
                    print 'NAMEID HOP:',nbr.nameID
                nbr.RouteByNameID(msg)
                return
            h = h - 1
        self.DeliverMessage(msg)
        
    def SendMsg(self,nameID,msg=Msg()):
        if LongestPrefix(nameID, self.nameID)==0:
            msg.dir = random.choice([0,1])
        elif nameID < self.nameID:
            msg.dir = clockwise
        else:
            msg.dir = counterclockwise
        msg.nameID = nameID
        self.RouteByNameID(msg)

    def RouteByNumericID(self,numericID,msg=Msg()):
        msg.ringLv1 = -1
        msg.startNode = msg.bestNode = None
        msg.finalDestination = False
        msg.numID = numericID
        self.RouteNumID(msg)
        
    def RouteNumID(self, msg):
        if msg.numID == self.numID or msg.finalDestination:
            self.DeliverMessage(msg)
            return
        if msg.startNode!=None:
            if self == msg.startNode:
                msg.finalDestination = True
                msg.bestNode.DeliverMessage(msg)
                return
        h = CommonPrefixLen(msg.numID,self.numID)
        if h > msg.ringLv1:
            msg.ringLv1 = h
            msg.startNode = msg.bestNode = self
        elif abs(self.numID-msg.numID) < abs(msg.bestNode.numID-msg.numID):
            msg.bestNode = self
        nbr = self.RouteTable[clockwise][msg.ringLv1]
        if DEBUG:
            print 'NUMID HOP:',nbr.nameID
        nbr.RouteNumID(msg)
            
    def DeliverMessage(self,msg):
        if msg.operation == findTopLevelRing:
            msg.ringLv1 = CommonPrefixLen(self.numID,msg.numID)
            msg.ringNbrClockWise = {}
            msg.ringNbrCClockWise = {}
            msg.doInsertions = False
            self.CollectRingInsertionNeighbors(msg)
        elif msg.operation == updateRings:
            self.CollectRingInsertionNeighbors(msg)
        else:
            print self.nameID, self.numID,'encontrado !'        

    def __cmp__(self,aNode):
        if aNode==None:
            return 1
        a =  self.nameID == aNode.nameID
        b =  self.numID == aNode.numID
        if a and b:
            return 0
        else:
            return 1
    
    def insertNode(self,node):
        msg = Msg()
        msg.operation = findTopLevelRing
        msg.joiningNode = node
        msg.numID = node.numID
        msg.nameID = node.nameID
        self.RouteByNumericID(node.numID,msg)
        
    def CollectRingInsertionNeighbors(self,msg):
        if msg.doInsertions:
            self.InsertIntoRings(msg.ringNbrClockWise,msg.ringNbrCClockWise)
            return
        while msg.ringLv1 >= 0:
            nbr = self.RouteTable[clockwise][msg.ringLv1]
            if LiesBetween(self.nameID,msg.nameID,nbr.nameID,clockwise):
                msg.ringNbrClockWise[msg.ringLv1] = nbr
                msg.ringNbrCClockWise[msg.ringLv1]  = self
                msg.ringLv1 = msg.ringLv1 - 1
            else:
                nbr.SendMsg(msg.nameID,msg)
                return
        msg.doInsertions = True
        msg.operation = updateRings
        msg.joiningNode.SendMsg(msg.nameID,msg)
        
    def InsertIntoRings(self,ringNbrClockWise,ringNbrCClockWise):
        for i in ringNbrClockWise:
            self.RouteTable[clockwise][i]=ringNbrClockWise[i]
            self.RouteTable[counterclockwise][i]=ringNbrCClockWise[i]
            ringNbrClockWise[i].setNeighbour(counterclockwise,i,self)
            ringNbrCClockWise[i].setNeighbour(clockwise,i,self)

        
    def setNeighbour(self,dir,level,node):
        self.RouteTable[dir][level]=node
        
    def successor(self):
        return self.RouteTable[clockwise][0]
    
    def __repr__(self):
        return '(nameID:'+str(self.nameID)+ ' , numID:'+str(self.numID)+')'
        
def LiesBetween(anameID,bnameID,cnameID,dir):
    if dir==clockwise:
        return between(bnameID,anameID,cnameID)
    else:
        return between(bnameID,cnameID,anameID)

def LongestPrefix(anameID, bnameID):
    bin1 = dec2bin2(anameID,k)
    bin2 = dec2bin2(bnameID,k)
    if bin1[0]!=bin2[0]:
        return 0
    else:
        return 1

   
def CommonPrefixLen(anumID, bnumID):
    bin1 = dec2bin2(anumID,k)
    bin2 = dec2bin2(bnumID,k)
    i = 0
    while bin1[i]==bin2[i] and i<k:
       i = i + 1
    return i    

def bin2dec(bits):
    size = len(bits)-1
    result = 0
    for bit in bits:
        result = result + int(bit)*(2**size)
        size = size -1
    return result

def dec2bin(dec):
    if (dec == 0):
            return '0'
    top =  int(log(dec,2))
    result = '1'
    remainder = dec % 2**top
    for i in range(top-1,-1,-1):
        result = result+ str(remainder/2**i)
        remainder = remainder % 2**i
    return result

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
    
# ----------------------The next functions are related to Pajek file generation ---------------------

def node2graph(node):
    graph = {}
    addNode(graph,node)
    current = node.successor()
    while current!=node:    
        addNode(graph,current)
        current = current.successor()
    return graph

def addNode(graph,node):
    graph[node.nameID] = []
    for i in range(node.maxHeight):
        graph[node.nameID].append(node.RouteTable[clockwise][i].nameID)
        graph[node.nameID].append(node.RouteTable[counterclockwise][i].nameID)
        
def toPajek(node, filename):
    graph = node2graph(node)
    f = open(filename,'w')
    size = len(graph)
    f.write('*Vertices '+str(size)+'\n')
    for i in range(size):
        f.write(' '+str(i+1)+' "'+str(graph.keys()[i])+'"\n')
    f.write('*Edges\n')
    for i in graph:
        for conn in graph[i]:
            f.write(' '+str(graph.keys().index(i)+1)+' '+str(graph.keys().index(conn)+1)+' 1\n')
    f.close()
                                  