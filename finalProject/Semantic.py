from Parser import Node, absTree, names, parseText
from copy import deepcopy

class SymbolTable:
    vars=dict({})
    id=''
    ancestor=None
    children=None
    block=0
    def __init__(self,id,block,ancestor=None):
        self.id=id
        self.ancestor=ancestor
        self.block=block
        self.vars=deepcopy(dict({}))
        if ancestor:
            ancestor.children=[self]
            ancestor.children.append(self)

    def printInfo(self):
        print("id: ",self.id)
        if self.ancestor:
            print("ancestor: ", self.ancestor.id)
        print("Variables: ", self.vars)
        if self.children:
            print("children:")
            for c in self.children:
                print(c.id)
    
    def addVar(self,name,type):
        self.vars[name]=type

res=None

parseText("example.txt")
res=absTree
globalvars = SymbolTable("Global",id(res))
symTable=[]

def getScopes(id):
    for tab in symTable:
        if tab.block==id:
            return tab
    return None

def setScopes(node,parentScope):
    if node:
        curScp = SymbolTable(node.val,id(node),parentScope)
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
                    setScopes(child,parentScope)
                elif child.type == "ELSE":
                    addVars(child.childrens[0],curScp)
                    setScopes(child,parentScope)
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

setScopes(res,None)
for tab in symTable:
    tab.printInfo()
print(viewScopes(res,None))
if not viewScopes(res,None):
    exit("Missmatch scope")
print(symTable[0].printInfo())
print("Semantic Analisys done")

