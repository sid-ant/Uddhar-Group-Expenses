
"""

Modified Krushkull's Algo. 

"""

def main():
    edge_list = []
    edges = open("edges.txt","r")
    for e in edges:
        edge = tuple(e.split())
        edge_list.append(edge)
    
    #assuming 10 nodes for this poc
    link = [i for i in range(11)]
    size = [1 for i in range(11)]
    
    solved=[]
    
    for e in edge_list:
        node_a = e[0]
        node_b = e[1]
        weight_ab = e[2]

        if(!same(node_a,node_b)):
            unite(node_a,node_b)
            solved.append(e)
        else:


def dfs(node):
    if visited(node):
        continue
    visited[node]=True
    for i in adj[node]:
        djs(i)

def find(node):
    x = node
    while(x!=link[x]): 
        x = link[x]
    return x 

def same(node_a,node_b):
    if find(node_a)!=find(node_b):
        return False
    return True 

def unite(node_a,node_b):
    a = find(node_a)
    b = find(node_b)
    if (size[a]<size[b]):
        a,b=b,a
    size[a]+=size[b]
    link[b]=a

    
