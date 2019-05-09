
"""

Modified Krushkull's Algo. 

"""

import queue

def main():
    solved=[]
    edge_list = open("edges.txt","r").readlines
    link = [i for i in range(3)]
    size = [1 for i in range(3)]

    adj=[[] for i in range(3)]

    for e in edge_list:
        node_a = e[0]
        node_b = e[1]
        weight_ab = e[2]
        if(!same(node_a,node_b,link)):
            unite(node_a,node_b,size,link)
            adj[node_a].extend(node_b)
            adj[node_b].extend(node_a)
            solved.append(e)
        else:
            traversal_order = bfs(node_a,node_b,adj)
            first = node_a
            '''
            Dumb solution
            '''
            for t in traversal_order:
                for dumb in enumerate(solved):
                    if first==dumb[1][0] & t = dumb[1][1]:
                        solved[dumb[0]][2]+=weight_ab
                    elif t==dumb[1][0] & first = dumb[1][1]:
                        solved[dumb[0]][2]-=weight_ab
                first = t
    
    print(solution)

def bfs(start,destination,adj):
    bfs_q = queue.Queue
    processed = [False for i in range(3)]
    traversal_order = []
    q.put(start)
    processed[start]=True
    while(!q.empty()):
        node = q.get()
        traversal_order.append(node)
        if node == destination:
            return node
        for neighbour in adj[node]:
            if processed[neighbour]: 
                continue
            processed[node]=True
            q.put(neighbour)

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
    a = find(node_a)
    b = find(node_b)
    if (size[a]<size[b]):
        a,b=b,a
    size[a]+=size[b]
    link[b]=a
