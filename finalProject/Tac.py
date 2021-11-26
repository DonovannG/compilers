from Semantic import res,SymbolTable,Node,absTree

blocks = []

def assignGenerator(node,file,y):
    tmpN = y
    if not node.type == "=":
        print("Recursion Error")
    else:
        if node.childrens[1].type == "OPERATION" or node.childrens[1].type == "CONCATENATION":
            tmpN = opGenerator(node.childrens[1],file,y)
            file.write(node.childrens[0].val + " = " +"T"+str(tmpN-1)+ "\n")
        else:
            file.write(node.childrens[0].val + " = " + node.childrens[1].val + "\n")
    return tmpN

def getStrAssign(node,y):
    tmpN = y
    tmpStr=""
    if node.childrens[1].type == "OPERATION" or node.childrens[1].type == "CONCATENATION":
        tmpN,holder = getStringOp(node.childrens[1],y)
        tmpStr = holder+(node.childrens[0].val + " = " +"T"+str(tmpN-1)+ "\n")
    else:
        tmpStr=(node.childrens[0].val + " = " + node.childrens[1].val + "\n")
    return tmpN+1,tmpStr

def setPrint(node,file,y):
    tmpN = y
    if node.childrens[0].type == "OPERATION" or node.childrens[0].type == "CONCATENATION":
        tmpN = opGenerator(node.childrens[0],file,y)
        file.write("print "+"T"+str(tmpN-1)+ "\n")
    else:
        file.write("print "+ node.childrens[0].val + "\n")
    return tmpN

def getStringPrint(node,y):
    tmpN = y
    tmpStr=""
    if node.childrens[0].type == "OPERATION" or node.childrens[0].type == "CONCATENATION":
        tmpN,holder = getStringOp(node.childrens[0],y)
        tmpStr = holder+("print "+"T"+str(tmpN-1)+ "\n")
    else:
        tmpStr=("print "+ node.childrens[0].val + "\n")
    return tmpN+1,tmpStr

def opGenerator(node,file,y):
    tmpN = y
    if node.childrens[1].type == "OPERATION":
        tmpN = opGenerator(node.childrens[1],file,y)
        file.write("T"+str(tmpN)+" = "+node.childrens[0].val+" "+node.val+" "+"T"+str(tmpN-1)+ "\n")
    else:
        file.write("T"+str(tmpN)+" = "+node.childrens[0].val+" "+node.val+" "+node.childrens[1].val+ "\n")
    return tmpN+1

def getStringOp(node,y):
    tmpN = y
    tmpStr=""
    if node.childrens[1].type == "OPERATION" or node.childrens[1].type == "CONCATENATION":
        tmpN,holder = getStringOp(node.childrens[1],y)
        tmpStr = holder+("T"+str(tmpN)+" = "+node.childrens[0].val+" "+node.val+" "+"T"+str(tmpN-1)+ "\n")
    else:
        tmpStr = ("T"+str(tmpN)+" = "+node.childrens[0].val+" "+node.val+" "+node.childrens[1].val+ "\n")
    return tmpN+1,tmpStr

