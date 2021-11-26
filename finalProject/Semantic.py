from Parser import Node, absTree, names, parseText
from copy import deepcopy

class SymbolTable:
    vars=dict({})
    ancestor=None
    blk=0
    id=''
    def __init__(self,id,blk,ancestor=None):
        self.id=id
        self.ancestor=ancestor
        self.blk=blk
        self.vars=deepcopy(dict({}))


    def printInfo(self):
        print("id: ",self.id)
        if self.ancestor:
            print("ancestor: ", self.ancestor.id)
        print("Variables: ", self.vars)
    
    def addVar(self,name,type):
        self.vars[name]=type


symTable=[]

def getScopes(id):
    for count in symTable:
        if count.blk==id:
            return count
    return None

def setScopes(node,ancScope):
    if node:
        curScp = SymbolTable(node.val,id(node),ancScope)
        symTable.append(curScp)
        for child in node.childrens:
            if child:
                if child.type == "=":
                    curScp.addVar(child.childrens[0].val,child.childrens[0].type)
                elif child.type == "IF":
                    addVars(child.childrens[1],curScp)
                    setScopes(child,curScp)
                elif child.type == "ELIF":
                    addVars(child.childrens[1],curScp)
                    setScopes(child,ancScope)
                elif child.type == "ELSE":
                    addVars(child.childrens[0],curScp)
                    setScopes(child,ancScope)
                elif child.type == "WHILE":
                    addVars(child.childrens[1],curScp)
                    setScopes(child,curScp)
                elif child.type == "FOR":
                    addVars(child.childrens[3],curScp)
                    setScopes(child,curScp)
        
def viewScopes(node,scope):
    if not scope:
        curScp = getScopes(id(node))
    else:
        curScp=scope
    if node:
        for child in node.childrens:
            if child:
                if child.type == "IF":
                    subcheck=viewScopes(child,None)
                    if not subcheck:
                        return False
                elif child.type == "ELIF":
                    subcheck=viewScopes(child,None)
                    if not subcheck:
                        return False
                elif child.type == "ELSE":
                    subcheck=viewScopes(child,None)
                elif child.type == "WHILE":
                    subcheck=viewScopes(child,None)
                elif child.type == "FOR":
                    subcheck=viewScopes(child,None)
                elif child.var:
                    if not checkVar(child.childrens[0].val,curScp):
                        return False
                else:
                    subcheck=viewScopes(child,curScp)
                    if not subcheck:
                        return False
    return True

def addVars(node,scope):
    if node:
        for child in node.childrens:
            if child:
                if child.type == "=":
                    scope.addVar(child.childrens[0].val,child.childrens[0].type)
                elif child.type == "IF":
                    setScopes(child,scope)
                elif child.type == "ELIF":
                    setScopes(child,scope)
                elif child.type == "ELSE":
                    setScopes(child,scope)
                elif child.type == "WHILE":
                    setScopes(child,scope)
                elif child.type == "FOR":
                    setScopes(child,scope)
        

def checkVar(var,scope):
    if not scope:
        return False
    else:
        if var in scope.vars:
            return True
        else:
            checkVar(var,scope.ancestor)

#Implementing the tree inside de file, sorry
res=None
def generateTestTree():
    res = Node("Start","Start")
    decInt=Node("assign","=",[Node("a","INT",var=True),Node("2","INT")])
    res.childrens.append(decInt)
    decFlt=Node("assign","=",[Node("b","FLOAT",var=True),Node("3","INT")])
    res.childrens.append(decFlt)
    decStr=Node("assign","=",[Node("c","STRING",var=True),Node("tree","STRING")])
    res.childrens.append(decStr)
    decElif=Node("elif","ELIF",[Node(">","OPERATION",[Node("a","INT",var=True),Node("2","INT")]),Node("assign","=",[Node("d","BOOLEAN",var=True),Node("true","BOOLEAN")])])
    decElse=Node("else","ELSE",[Node("block","else",[Node("PRINT","PRINT",[Node("s", "STRING", var=True)])])])
    decIF=Node("if","IF",[Node("<","OPERATION",[Node("a","FLOAT",var=True),Node("2","INT")]),Node("block","if",[Node("PRINT","PRINT",[Node("b","FLOAT",var=True)])]),decElif,decElse])
    res.childrens.append(decIF)
    decI=Node("assign","=",[Node("i","INT",var=True),Node("0","INT")])
    res.childrens.append(decI)
    decForStart=Node("assign","=",[Node("i","INT",var=True),Node("0","INT")])
    decOpFor=Node("<","OPERATION",[Node("i","INT",var=True),Node("5","INT")])
    decIncFor=Node("+","step",[Node("i","INT",var=True),Node("1","INT")])
    decForPrint=Node("block","for",[Node("PRINT","PRINT",[Node("i","INT",var=True)])])
    decFor=Node("for","FOR",[decForStart,decOpFor,decIncFor,decForPrint])
    res.childrens.append(decFor)
    decWhile=Node("while","WHILE",[Node("==","OPERATION",[Node("a","INT", var=True),Node("3","INT")]),
    Node("block","while",[Node("PRINT","PRINT",[Node("c","STRING",var=True)])])])
    res.childrens.append(decWhile)

    return res
     
res=generateTestTree()
#parseText("Example.txt")
#res=absTree

setScopes(res,None)
for count in symTable:
    count.printInfo()
print(viewScopes(res,None))

print("Semantic Analisys done")

