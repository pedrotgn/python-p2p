# author: Pedro Garcia Lopez, PhD
# README !!!! : Set the variable k to 160 in chord.py. The hash function generates keys of size 2^160.
from chord import *
from time import time

def main():

    k = 160
    t1  = time()
    nodes = {}
    for i in range(100):
        nodes[i] = Node(id())
       # print nodes[i].id
    
    for i in range(100):
        nodes[i].join(nodes[0])
    
    t2 = time()
    print 'Time to create 100 nodes'
    print t2 - t1

       
    key = hash('pedro')
    print key
    found = nodes[0].find_predecessor(key)
    print found.id
    
   
    print 'finish !!!'
    



if __name__ == "__main__":

    main()
