from Semantic import res,SymbolTable,Node,absTree

blockList = []

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

def blockGenerator(node,tmp,temp):
    tmpC=tmp
    tmpBG=temp
    x = "L"+str(temp)+"\n"
    for child in node.childrens:
        if child.type == "=":
            tmpC,inst=getStrAssign(child,tmp)
            x=x+inst
        elif child.type == "PRINT":
            tmpC,inst=getStringPrint(child,tmp)
            x=x+inst
        elif child.type == "IF":
            tmpN, k = getStringOp(child.childrens[0],tmp)
            for ifChild in child.childrens:
                if ifChild.type == "if":
                    x=x+(k)
                    tmpA,tmpB=blockGenerator(ifChild,tmpN,temp)
                    x=x+("T"+str(tmpN-1)+" IFGOTO L"+str(tmpB-1)+"\n")
                    tmpC=tmpA
                    tmpBG=tmpB
                elif ifChild.type == "ELIF":
                    tmpN, k = getStringOp(ifChild.childrens[0],tmp)
                    for elifChild in ifChild.childrens:
                        if elifChild.type == "elif":
                            x=x+(k)
                            tmpA,tmpB=blockGenerator(elifChild,tmpN,temp)
                            x=x+("T"+str(tmpN-1)+" ELSEIFGOTO L"+str(tmpB-1)+"\n")
                            tmpC=tmpA
                            tmpBG=tmpB
                elif ifChild.type == "ELSE":
                    if ifChild.childrens[0]:
                        tmpA,tmpB=blockGenerator(ifChild.childrens[0],tmpN,temp)
                        x=x+("ELSEGOTO L"+str(tmpB-1)+"\n")
                        tmp=tmpA
                        temp=tmpB
        elif child.type == "WHILE":
            tmpN, k = getStringOp(child.childrens[0],tmp)
            x=x+(k)
            tmpA,tmpB=whileBlockGenerator(child.childrens[1],tmpN,temp,tmpN)
            x=x+("T"+str(tmpN-1)+" IFGOTO L"+str(tmpB-1)+"\n")
            tmpC=tmpA
            tmpBG=tmpB
        elif child.type == "FOR":
            tmpC,op=getStrAssign(child.childrens[0],tmp)
            x=x+(op)
            tmpC,op=getStringOp(child.childrens[1],tmpC)
            x=x+(op)
            tmpA,tmpB=forBlockGenerator(child.childrens[3],tmpC,temp,"T"+str(tmpC-1)+" IFGOTO L"+str(temp)+"\n",child.childrens[2],op)
            x=x+("T"+str(tmpC-1)+" IFGOTO L"+str(tmpB-1)+"\n")
            tmpC=tmpA
            tmpBG=tmpB
    blockList.append(x)
    return tmpC+1,tmpBG+1

def whileBlockGenerator(node,tmp,temp,j):
    tmpC=tmp
    tmpBG=temp
    x = "L"+str(temp)+"\n"
    for child in node.childrens:
        if child.type == "=":
            tmpC,inst=getStrAssign(child,tmp)
            x=x+inst
        elif child.type == "PRINT":
            tmpC,inst=getStringPrint(child,tmp)
            x=x+inst
        elif child.type == "IF":
            tmpN, k = getStringOp(child.childrens[0],tmp)
            for ifChild in child.childrens:
                if ifChild.type == "if":
                    x=x+(k)
                    tmpA,tmpB=blockGenerator(ifChild,tmpN,temp)
                    x=x+("T"+str(tmpN-1)+" IFGOTO L"+str(tmpB-1)+"\n")
                    tmpC=tmpA
                    tmpBG=tmpB
                elif ifChild.type == "ELIF":
                    tmpN, k = getStringOp(ifChild.childrens[0],tmp)
                    for elifChild in ifChild.childrens:
                        if elifChild.type == "elif":
                            x=x+(k)
                            tmpA,tmpB=blockGenerator(elifChild,tmpN,temp)
                            x=x+("T"+str(tmpN-1)+" ELSEIFGOTO L"+str(tmpB-1)+"\n")
                            tmpC=tmpA
                            tmpBG=tmpB
                elif ifChild.type == "ELSE":
                    if ifChild.childrens[0]:
                        tmpA,tmpB=blockGenerator(ifChild.childrens[0],tmpN,temp)
                        x=x+("ELSEGOTO L"+str(tmpB-1)+"\n")
                        tmpC=tmpA
                        tmpBG=tmpB
        elif child.type == "WHILE":
            tmpN, k = getStringOp(child.childrens[0],tmp)
            x=x+(k)
            tmpA,tmpB=whileBlockGenerator(child.childrens[1],tmpN,temp,tmpN)
            x=x+("T"+str(tmpN-1)+" IFGOTO L"+str(tmpB-1)+"\n")
            tmpC=tmpA
            tmpBG=tmpB
        elif child.type == "FOR":
            tmpC,op=getStrAssign(child.childrens[0],tmp)
            x=x+(op)
            tmpC,op=getStringOp(child.childrens[1],tmpC)
            x=x+(op)
            tmpA,tmpB=forBlockGenerator(child.childrens[3],tmpC,temp,"T"+str(tmpC-1)+" IFGOTO L"+str(temp)+"\n",child.childrens[2],op)
            x=x+("T"+str(tmpC-1)+" IFGOTO L"+str(tmpB-1)+"\n")
            tmpC=tmpA
            tmpBG=tmpB


    x=x+"T"+str(j-1)+" IFGOTO L"+str(tmpBG)+"\n"
    blockList.append(x)
    return tmpC+1,tmpBG+1

def forBlockGenerator(node,tmp,temp,j,step,compar):
    tmpC=tmp
    tmpBG=temp
    x = "L"+str(temp)+"\n"
    for child in node.childrens:
        if child.type == "=":
            tmpC,inst=getStrAssign(child,tmp)
            x=x+inst
        elif child.type == "PRINT":
            tmpC,inst=getStringPrint(child,tmp)
            x=x+inst
        elif child.type == "IF":
            tmpN, k = getStringOp(child.childrens[0],tmp)
            for ifChild in child.childrens:
                if ifChild.type == "if":
                    x=x+(k)
                    tmpA,tmpB=blockGenerator(ifChild,tmpN,temp)
                    x=x+("T"+str(tmpN-1)+" IFGOTO L"+str(tmpB-1)+"\n")
                    tmpC=tmpA
                    tmpBG=tmpB
                elif ifChild.type == "ELIF":
                    tmpN, k = getStringOp(ifChild.childrens[0],tmp)
                    for elifChild in ifChild.childrens:
                        if elifChild.type == "elif":
                            x=x+(k)
                            tmpA,tmpB=blockGenerator(elifChild,tmpN,temp)
                            x=x+("T"+str(tmpN-1)+" ELSEIFGOTO L"+str(tmpB-1)+"\n")
                            tmpC=tmpA
                            tmpBG=tmpB
                elif ifChild.type == "ELSE":
                    if ifChild.childrens[0]:
                        tmpA,tmpB=blockGenerator(ifChild.childrens[0],tmpN,temp)
                        x=x+("ELSEGOTO L"+str(tmpB-1)+"\n")
                        tmpC=tmpA
                        tmpBG=tmpB
        elif child.type == "WHILE":
            tmpN, k = getStringOp(child.childrens[0],tmp)
            x=x+(k)
            tmpA,tmpB=whileBlockGenerator(child.childrens[1],tmpN,temp,tmpN)
            x=x+("T"+str(tmpN-1)+" IFGOTO L"+str(tmpB-1)+"\n")
            tmpC=tmpA
            tmpBG=tmpB
        elif child.type == "FOR":
            tmpC,op=getStrAssign(child.childrens[0],tmp)
            x=x+(op)
            tmpC,op=getStringOp(child.childrens[1],tmpC)
            x=x+(op)
            tmpA,tmpB=forBlockGenerator(child.childrens[3],tmpC,temp,"T"+str(tmpC-1)+" IFGOTO L"+str(temp)+"\n",child.childrens[2],op)
            x=x+("T"+str(tmpC-1)+" IFGOTO L"+str(tmpB-1)+"\n")
            tmpC=tmpA
            tmpBG=tmpB
    strng=""
    if step.childrens[1].type == "OPERATION":
        tmpA,strng=getStringOp(step.childrens[1])
        x=x+strng+step.childrens[0].val+" = T"+str(tmpN-1)+"\n"
        tmpC=tmpA
    else:
        x=x+step.childrens[0].val+" = "+step.childrens[0].val+" "+step.val+" "+step.childrens[1].val+"\n"
    x=x+compar
    x=x+j
    blockList.append(x)
    return tmpC+1,tmpBG+1

def tasGenerator(node,filename):
    file = open("finalProject/"+filename,"w")
    tmp = 1
    temp = 1
    for child in node.childrens:
        if child.type == "=":
            tmp=assignGenerator(child,file,tmp)
        elif child.type == "PRINT":
            tmp=setPrint(child,file,tmp)
        elif child.type == "IF":
            tmpN, k = getStringOp(child.childrens[0],tmp)
            for ifChild in child.childrens:
                if ifChild.type == "if":
                    file.write(k)
                    tmpA,tmpB=blockGenerator(ifChild,tmpN,temp)
                    file.write("T"+str(tmpN-1)+" IFGOTO L"+str(tmpB-1 )+"\n")
                    tmp=tmpA
                    temp=tmpB
                elif ifChild.type == "ELIF":
                    tmpN, k = getStringOp(ifChild.childrens[0],tmp)
                    for elifChild in ifChild.childrens:
                        if elifChild.type == "elif":
                            file.write(k)
                            tmpA,tmpB=blockGenerator(elifChild,tmpN,temp)
                            file.write("T"+str(tmpN-1)+" ELSEIFGOTO L"+str(tmpB-1)+"\n")
                            tmp=tmpA
                            temp=tmpB
                elif ifChild.type == "ELSE":
                    if ifChild.childrens[0]:
                        tmpA,tmpB=blockGenerator(ifChild.childrens[0],tmpN,temp)
                        file.write("ELSEGOTO L"+str(tmpB-1)+"\n")
                        tmp=tmpA
                        temp=tmpB
        elif child.type == "WHILE":
            tmpN, k = getStringOp(child.childrens[0],tmp)
            file.write(k)
            tmpA,tmpB=whileBlockGenerator(child.childrens[1],tmpN,temp,tmpN)
            file.write("T"+str(tmpN-1)+" IFGOTO L"+str(tmpB-1)+"\n")
            tmp=tmpA
            temp=tmpB
        elif child.type == "FOR":
            tmpC,op=getStrAssign(child.childrens[0],tmp)
            file.write(op)
            tmpC,op1=getStringOp(child.childrens[1],tmpC)
            file.write(op1)
            tmpA,tmpB=forBlockGenerator(child.childrens[3],tmpC,temp,"T"+str(tmpC-1)+" IFGOTO L"+str(temp)+"\n",child.childrens[2],op1)
            file.write("T"+str(tmpC-1)+" IFGOTO L"+str(tmpB-1)+"\n")
            tmp=tmpA
            temp=tmpB
    for x in blockList:
        file.write("\n"+x)
    file.close()

tasGenerator(res,"tac.txt")
print("Done!")