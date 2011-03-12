# Epidemics
# author: Pedro Garcia Lopez
# 




def toPajekTime(graph, filename):
    f = open(filename,'w')
    size = len(graph)
    f.write('*Vertices '+str(size)+'\n')
    f.write('*Events\n')
    f.write('TI 1\n')
    for i in range(1,size+1):
        f.write('AV '+str(i)+' "'+str(i)+'" ic Yellow\n')
    for i in range(1,size+1):
        for conn in graph[i]:
            f.write('AE '+str(i)+' '+str(conn)+' 1\n')
    steps = 3
    cnt = 2
    for step in range(steps):
        infected = epidemics(1,conns,step)
        f.write('TI '+str(cnt) +'\n')
        cnt = cnt + 1
        for node in infected:
            f.write('CV '+str(node)+' ic Red\n')     
    f.close()


def show(graph):
    size = len(graph)
    print '-------REGULAR GRAPH-------'
    for x in range(1,size+1):
        print x,conns[x]

def concat(src,dst):
    for elem in dst:
        if not (src.__contains__(elem)):
            src.append(elem)
    return src

def epidemics(src, graph, time):
    if time==0:
        infected = [src]
        infected = infected + infect(src,infected,graph)
        return infected
    else:
        infected = [src]
        infected = infected + infect(src,infected,graph)
        result = []
        for i in range(time):
            for node in infected:
                result = concat(result,infect(node,infected,graph))
            infected = concat(infected,result)
    return infected
        

    
def infect(node,infected,graph):
    newvictims = []
    for victim in graph[node]:
        if not(infected.__contains__(victim)):
            newvictims.append(victim)
    return newvictims
    


size = 12
k = 4
conns = {}
for i in range(1,size+1):
    conns[i] = []
    for conn in range(1,k/2+1):
            newcon = ((i+conn)%size)
            if newcon==0:
            	newcon = size
            conns[i].append(newcon)
            newcon2 = ((i-conn)%size)
            if newcon2==0:
            	newcon2 = size
            conns[i].append(newcon2)

print epidemics(1,conns,2)

show(conns)
toPajekTime(conns,'gossip.tim')


