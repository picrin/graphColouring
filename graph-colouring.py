graph = {}
colouring = {}

import sys

argNum = len(sys.argv)

if argNum != 2:
    print("usage is: `" + sys.argv[0] + " <graphFile>`, where graphFile contains a graph in any supported format.")
    sys.exit(1)


def mergeUniqueSorted(lista1, lista2):
    index1, index2 = 0, 0
    result = []
    while index1 < len(lista1) or index2 < len(lista2):
        if index1 >= len(lista1):
            output = lista2[index2]
            index2 += 1
        elif index2 >= len(lista2):
            output = lista1[index1]
            index1 += 1
        elif lista1[index1] < lista2[index2]:
            output = lista1[index1]
            index1 += 1
        else: # lista1[index1] > lista2[index2]:
            output = lista2[index2]
            index2 += 1
        if len(result) > 0 and output == result[-1]:
           continue
        result.append(output)
    return result

def upsertVertex(graph, vertex, adjacency):
    if vertex not in graph:
        adjacency.sort()
        graph[vertex] = mergeUniqueSorted(adjacency, [])
    else:
        graph[vertex] = mergeUniqueSorted(vertices[vertex], adjacency)

with open(sys.argv[1]) as g:
    for line in g.readlines():
        line = line.rstrip("\n")
        line = line.split(": ")
        vertex = int(line[0])
        adjacency = line[1]
        adjacency = [int(a) for a in adjacency.split(" ")]
        upsertVertex(graph, vertex, adjacency)
        colouring[vertex] = None
availableColours = ["red", "green", "blue"]

def checkColourOK(graph, colouring, vertex):
    for a in graph[vertex]:
        if colouring[a] == colouring[vertex]:
            return False
    return True and colouring[vertex] != None

def pickVertex(graph, sortedVertices, colouring, vertexIndex):
    if vertexIndex == len(graph):
        return
    colourIndex = 0
    vertex = sortedVertices[vertexIndex]
    while colourIndex < len(availableColours):
        colouring[vertex] = availableColours[colourIndex]
        isOK = checkColourOK(graph, colouring, vertex)
        if isOK:
            if vertexIndex + 1 == len(graph):
                print("success")
                print(colouring)
                sys.exit(0)
            else:
                pickVertex(graph, sortedVertices, colouring, vertexIndex + 1)
        colouring[vertex] = None
        colourIndex += 1
    if vertexIndex == 0:
        print("failure")
        sys.exit(1)

def colourGraph(graph, sortedVertices, colouring):
    pickVertex(graph, sortedVertices, colouring, 0)

sortedVertices = [key for key in graph]
sortedVertices.sort()

colourGraph(graph, sortedVertices, colouring)
