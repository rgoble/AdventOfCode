
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

# Now that the tree is loaded, time to start navigating it
numSteps = 0
numDir = len(directions)
node = tree.getNode('AAA')
while node.name != 'ZZZ':
    currDir = numSteps % numDir
    if directions[currDir] == 'L':
        newNode = tree.left(node)
    else:
        newNode = tree.right(node)
    
    numSteps += 1
    if numSteps < 10 or (numSteps % 100 == 1) or (numSteps == numDir - 1) or (numSteps == numDir):
        print("Step #%6d: PrevNode[%s] => %s(%d) => NewNode[%s]" % (numSteps, node, directions[currDir], currDir, newNode))

    # Advance the node
    node = newNode

print('='*8)
print("NumSteps = %d" % numSteps)
print('Is not   = 2555')