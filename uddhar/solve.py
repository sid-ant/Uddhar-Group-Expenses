
"""

Modified Krushkull's Algo. 

"""

import queue

def main():
    solved=[]
    edge_list = [list(map(int,line.rstrip().split(","))) for line in open('edges.csv')]
    print(edge_list)
    link = [i for i in range(4)]
    size = [1 for i in range(4)]

    adj=[[] for i in range(4)]

    for e in edge_list:
        node_a = e[0]
        node_b = e[1]
        weight_ab = e[2]
        if not same(node_a,node_b,link):
            unite(node_a,node_b,size,link)
            adj[node_a].append(node_b)
            adj[node_b].append(node_a)
            solved.append(e)
        else:
            traversal_order = bfs(node_a,node_b,adj)
            if traversal_order == None:
                print ("found no  path ")
                exit()
            first = node_a
            print("order=",traversal_order)
            '''
            Dumb working solution for now
            '''
            for t in traversal_order:
                for dumb in enumerate(solved):
                    print ("dumb",dumb)
                    if first==dumb[1][0] and t==dumb[1][1]:
                        solved[dumb[0]][2]+=weight_ab
                    elif t==dumb[1][0] and first==dumb[1][1]:
                        solved[dumb[0]][2]-=weight_ab
                first = t
    
    print(solved)

def bfs(start,destination,adj):
    path_q = queue.Queue()
    currrentpath = []
    currrentpath.append(start)
    path_q.put(currrentpath)
    while not path_q.empty():
        currrentpath = path_q.get()
        if currrentpath[-1] == destination:
            return currrentpath
        for neighbour in adj[currrentpath[-1]]:
            if neighbour in currrentpath: 
                continue
            currrentpath.append(neighbour)
            path_q.put(currrentpath)

def find(node,link):
    x = node
    while(x!=link[x]): 
        x = link[x]
    return x 

def same(node_a,node_b,link):
    if find(node_a,link)!=find(node_b,link):
        return False
    return True 

def unite(node_a,node_b,size,link):
    a = find(node_a,link)
    b = find(node_b,link)
    if (size[a]<size[b]):
        a,b=b,a
    size[a]+=size[b]
    link[b]=a

if __name__=="__main__":
    main()