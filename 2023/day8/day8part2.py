from math import gcd

class Node:
    def __init__(self, str) -> None:
        # SGR = (JLL, VRV)
        self.name = str[0:3]
        self.left = str[7:10]
        self.right = str[12:15]
    
    def __str__(self) -> str:
        return "%s = (%s, %s)" % (self.name, self.left, self.right)

class Tree:
    def __init__(self) -> None:
        self.nodes = {}

    def parse(self, str):
        # Create a new node
        n = Node(str)      
        # Add it to the map of nodes
        self.nodes[n.name] = n

    def getNode(self, name):
        return self.nodes[name]

    def left(self, currNode):
        return self.nodes[currNode.left]

    def right(self, currNode):
        return self.nodes[currNode.right]

    def allLeft(self, currNodes):
        allZ = True
        newNodes = []
        for n in currNodes:
            tmpNode = self.nodes[n.left]
            newNodes.append(tmpNode)
            # See if the new node ends with a Z. Once we find one
            # that doesn't we can stop checking, hence the short
            # circuit check on if its true
            if allZ == True and tmpNode.name[-1] != 'Z':
                allZ = False

        return newNodes, allZ

    def allRight(self, currNodes):
        allZ = True
        newNodes = []
        for n in currNodes:
            tmpNode = self.nodes[n.right]
            newNodes.append(tmpNode)
            # See if the new node ends with a Z. Once we find one
            # that doesn't we can stop checking, hence the short
            # circuit check on if its true
            if allZ == True and tmpNode.name[-1] != 'Z':
                allZ = False

        return newNodes, allZ

def lcm(cycleCnts):
    fact = 1
    for c in cycleCnts:
        fact = (c*fact)//gcd(c, fact)
    
    return fact

# Parse the input
tree = Tree()
directions = None
with open("input.txt", "rt") as inp:
    for line in inp:
        # First line is the directions
        if directions is None:
            directions = line[:-1]
        elif line != '\n':
            # Its not a blank line so parse it
            tree.parse(line)


# Now that the tree is loaded, lets find all of the starting
# points, nodes with a name that end with A
nodes = []
cycles = {}
for x in tree.nodes.keys():
    if x[-1] == 'A':
        # The node ends with A, so add it to our list of nodes to track
        nodes.append(tree.getNode(x))

numNodes = len(nodes)
print("Found %d starting nodes" % numNodes)

# Now that we have all of the starting nodes we can begin iterating over the tree
numSteps = 0
numDir = len(directions)
atEnd = False
while atEnd == False:

    currDir = numSteps % numDir
    numSteps += 1

    if directions[currDir] == 'L':
        nodes, atEnd = tree.allLeft(nodes)
    else:
        nodes, atEnd = tree.allRight(nodes)
    
    for i in range(numNodes):
        if nodes[i].name[-1] == 'Z' and cycles.get(i) is None:
            cycles[i] = numSteps

    if len(cycles) == numNodes:
        # We found the number of steps it takes to cycle each node back
        # to its starting value. So use the chinese remainder theorem
        # to solve the factors 
        numSteps = lcm (cycles.values())
        atEnd = True

print('='*8)
print("NumSteps = %d" % numSteps)