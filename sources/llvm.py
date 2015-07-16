#############################################################################################
#  llvm.py,																				#
#																							#
# llvm traductor for the Raccoon language.												#
#																																							#
#																							#
# May 2015, CATUSANU Paul, EWBANK Tom and VAN DE GOOR Elodie.								#
#############################################################################################

import AST
from AST import * 
import semantic
from semantic import * 
import re

def add_alloc(s):
	'''This function take an llvm code as argument (in the form of a string)
	   and add to it the missing "alloc" statements. The modified llvm is
	   returned as a string'''
	   
	result = ""
	rest = s
	encountered_var = {}
	while len(rest) > 0:
		try:
			i = rest.index('%') # search for a variable
		except:
			result = result + rest
			break
		
		result = result + rest[0:i+1]
		
		if rest[i-6:i] != "label ": # no need for an "alloc" statement if the variable is preceded by "label"
			
			allocNeeded = True
			
			# Find the variable name that follows the "%" character
			matchObj = re.match(r'[a-zA-Z_][a-zA-Z_0-9]*', rest[i+1:], re.I)
			if matchObj == None:
				allocNeeded = False
			else :
				j = len(matchObj.group())
				varName = rest[i:i+j+1]
				
				# only one "alloc" is need by variable, so check that we didn't encountered it before
				if not encountered_var.has_key(varName):
					encountered_var[varName] = 1
					#print(varName)
					
					k = len(result)-1
					char = result[k]
					# going back to the previous line to insert the alloc statement
					while char != '\n':
						k -= 1
						char = result[k]
						# if "define" encountered in the line, variable is an argument and don't need an "alloc"
						if k+6 <= len(result) and result[k:k+6] == "define":
							allocNeeded = False
							break							
				else: allocNeeded = False
			
			if allocNeeded:
				if varName[1] == 'I':
					alloca = " = alloca i32 "
				elif varName[1] == 'D': 
					alloca = " = alloca double "
				elif varName[1] == 'B':
					alloca = " = alloca i1 "
				elif varName[1] == 'L':
					alloca = " = alloca list "
				else:
					print("llvm error: unkown type")
					alloca = " = alloca undef "
				result = result[0:k+1] + "  " + varName + alloca + result[k:]
				
		rest = rest[i+1:]
	return result

	
@addToClass(AST.Node)	
def findList(self):
	self.next[0].findList()
	
@addToClass(AST.ProgramNode)	
def findList(self):
	return
	
@addToClass(AST.ListNode)	
def findList(self):
	global lists
	if self.parent.type == 'Assignment':	 
		lists.append(str(self.parent.children[0].tok))
		lists.append(len(self.children))
	self.next[0].findList()
	
@addToClass(AST.Node)	
def llvm(self):
	global s
	s+= str(self.lineNb) + self.type
	
@addToClass(AST.ProgramNode)	
def llvm(self):
	global s
		
	#lecture de l'arbre
	for i in self.children:
		i.llvm()
		s+="\n\n"
	#Ajout des alloc
	s = add_alloc(s)
	
	snew = s.replace("   "," ") 
	s = snew.replace("  "," ") 
	#incertion des fonction display pour les floats, les integers et les boolens (identifier compris)
	s += "\n\n@.strf = private unnamed_addr constant [4 x i8] c\"\\0A%f\\00\"\ndefine void @display_f(float %n)  {\nentry:\n  %n.addr = alloca float\n  store float %n, float* %n.addr\n  %0 = load float* %n.addr\n  %1 = fpext float %0 to double\n  %2 = getelementptr inbounds [4 x i8]* @.strf, i32 0, i32 0\n  %call = call i32 (i8*, ...)* @printf(i8* %2, double %1)\n  ret void\n}\n\n@.str = private unnamed_addr constant [4 x i8] c\"\\0A%d\\00\"	\ndefine void @display_i(i32 %n) {\nentry:\n  %n.addr = alloca i32\n  store i32 %n, i32* %n.addr\n  %0 = load i32* %n.addr\n  %1 = getelementptr inbounds [4 x i8]* @.str, i32 0, i32 0\n  %2 = call i32 (i8*, ...)* @printf(i8* %1, i32 %0)\n  ret void\n}\ndefine void @display_b(i1 %n) {\nentry:\n  %n.addr = alloca i1\n  store i1 %n, i1* %n.addr\n  %0 = load i1* %n.addr\n  %1 = getelementptr inbounds [4 x i8]* @.str, i32 0, i32 0\n  %2 = call i32 (i8*, ...)* @printf(i8* %1, i1 %0)\n  ret void\n}\n\n\ndeclare i32 @printf(i8*, ...)\n\n"
	

@addToClass(AST.FuncDefNode)
def llvm(self):
	global s
	a = self.children[0] 
	a.llvm()#head
	s+="{\n\nentry: "
	for i in range(1, len(a.children)):
		s+="\nstore "+str(a.children[i].typeI())+" %"+str(a.children[i].tok).replace(" ","")+"_arg, "+a.children[i].typeI()+"* %"+str(a.children[i].tok)
	self.children[1].llvm()#body
	if self.children[0].children[0].typeI()=='void':
		s+="\nret void\n} "# a return read only if there is no return un the function
	else:
		s+="\nret "+ self.children[0].children[0].typeI()+" 0\n} "# a return read only if there is no return un the function
	
	#remplacement des ?1? et ?2? par %0, %1, %2, etc
	i=0
	while 1:              
		snew = s.replace("?1?", "%"+str(i),1)
		snew = snew.replace("?2?", "%"+str(i),1)
		if s == snew:
			break
		i=i+1
		s = snew
	
	
		
@addToClass(AST.HeadNode)
def llvm(self):
	global s
	s+="\ndefine "+self.children[0].typeI()+" @"+str(self.children[0].tok)+"("
	for i in range(1, len(self.children)):
		#self.children[i].llvm()
		#s+="_arg"
		
		s+=str(self.children[i].typeI())+" %"+str(self.children[i].tok).replace(" ","")+"_arg"
		if (i != len(self.children)-1):
			s+=", "
	s+=")"

@addToClass(AST.IntNode)
def llvm(self):
	global s
	s+=" i32 " +str(self.tok)+" "
	
@addToClass(AST.TrueNode)
def llvm(self):
	global s
	s+=" i1 true"

@addToClass(AST.FalseNode)
def llvm(self):
	global s
	s+=" i1 false" 

@addToClass(AST.DoubleNode)
def llvm(self):
	global s
	s+="double " +str(self.tok)+" "
	
@addToClass(AST.ListNode)
def llvm(self):
	global s
	#s+= 

@addToClass(AST.TokenNode)	
def llvm(self):
	global s
	s += self.typeI()+" %"+str(self.tok)+" "

@addToClass(AST.BodyNode)
def llvm(self):
	global s
	for i in self.children:
		s+="\n"
		i.llvm()
		
@addToClass(AST.IdNode)	
def llvm(self):
	global s
	s += self.typeI()+" %"+str(self.tok)+" "

@addToClass(AST.FuncDefNameNode)
def typeI(self):
	t = self.tok
	global e
	if t[0]=='I':#integer
		return 'i32'
	elif t[0]=='D':#double
		return 'double'
	elif t[0]=='B':#boolean
		return 'i1'
	elif t[0]=='L':#list
		return '?undef?'
	elif t[0]=='S':#string
		return '?undef'
	else:
		return 'void'
		e+="\nError : begin the identifier name with its type (I, D, B, L or S)"
	
@addToClass(AST.IntNode)
def typeI(self):
	return"i32" 
	
@addToClass(AST.TrueNode)
def typeI(self):
	return"i1"

@addToClass(AST.FalseNode)
def typeI(self):
	return"i1"

@addToClass(AST.DoubleNode)
def typeI(self):
	return"double"
	
@addToClass(AST.ListElementNode)
def typeI(self):
	return"[ x i32]"
	
@addToClass(AST.FuncDefArgNode)	
@addToClass(AST.IdNode)	
@addToClass(AST.FuncCallNameNode)	
@addToClass(AST.TokenNode)	
def typeI(self):
	t = self.tok
	global e
	if t[0]=='I':#integer
		return 'i32'
	elif t[0]=='D':#double
		return 'double'
	elif t[0]=='B':#boolean
		return 'i1'
	elif t[0]=='L':#list
		return '?undef?'
	else:
		return '?undef'
		e+="\nError : begin the identifier name with its type (I, D, B or L)"

@addToClass(AST.OpNode)	
def typeI(self):
	global e
	a = self.children[0]
	b = self.children[0]
	if a.type=='Identifier' or a.type=='Operation' or a.type == 'Integer' or a.type == 'Double' or a.type == 'True' or a.type == 'False':
		return a.typeI()
	elif b.type=='Identifier' or b.type=='Operation' or b.type == 'Integer' or b.type == 'Double' or b.type == 'True' or b.type == 'False':
		return b.typeI()
	else:
		e+="\n\n undefine type for node:"+ a.type+ " and "+b.type


@addToClass(AST.OpNode)	
def llvm(self):
	global s
	if self.children[0].type == 'Operation':
		self.children[0].llvm()
	if self.children[0].type == 'Identifier':
		s+="\n?1? = load "+self.children[0].typeI()+"* %"+str(self.children[0].tok)
	if self.children[1].type == 'Operation':
		self.children[1].llvm()
	if self.children[1].type == 'Identifier':
		s+="\n?1? = load "+self.children[1].typeI()+"* %"+str(self.children[1].tok)
		
	s+="\n?1? = "
	#Si on a des Double, ajouter "f" juste devant
	if self.op == '+':
		s+="add"
	elif self.op == '-':
		s+="sub"
	elif self.op == '\*':
		s+="mul"
	elif self.op == '/':
		s+="div"
	elif self.op == '=?':
		s+="icmp eq"
	elif self.op == '!=':
		s+="icmp ne"
	elif self.op == '<':
		s+="icmp slt"
	elif self.op == '<=':
		s+="icmp sle"
	elif self.op == '>':
		s+="icmp sgt"
	elif self.op == '>=':
		s+="icmp sge"
	elif self.op == 'mod ':
		s+="srem"
	elif self.op == 'or':
		s+="icmp or"
	elif self.op == 'and':
		s+="icmp and"
	else:
		#s+="!! " +self.op
		self.llvm()
	s+=" "
		
	a = self.children[0]
	if a.type == 'Integer' or a.type == 'Double' or a.type == 'True' or a.type == 'False':
		a.llvm()
		s += ", "
	elif a.type == 'Identifier' or a.type == 'Operation':
		s += a.typeI()+" ?2?, "	
	else:
		#s+=" undef" + self.children[0].type+", "
		a.llvm()
		
	a = self.children[1]
	if a.type == 'Integer' or a.type == 'Double' or a.type == 'True' or a.type == 'False':
		s+= str(a.tok)
	elif a.type == 'Identifier' or a.type == 'Operation':
		s+= " ?2?"	
	else:
		#s+= a.type
		a.llvm()
		
	s+="\n"
		
@addToClass(AST.ForNode)#incomplete
def llvm(self):
	global s
	rangeNode= self.children[0]
	if rangeNode.type == 'In range':
		rangeNode.llvm()
		s+="\n\nfor_body_"+str(self.lineNb)+":"
		self.children[1].llvm()
		s+="\n?1? = load i32* %"+str(rangeNode.children[0].tok)
		s+="\n?1? = add i32 ?2?, 1"
		s+="\nstore "+rangeNode.children[2].typeI()+" ?2?, i32* %"+str(rangeNode.children[0].tok)
		s+="\nbr label %for_"+str(self.lineNb)+"\n\nfor_end_"+str(self.lineNb)+":"
		
	else: # for iterator in list: not implemented yet
		s+="\nbr label %for_" +str(self.lineNb)+"\n\nfor_" +str(self.lineNb)+":"
	
@addToClass(AST.InRangeNode)
def llvm(self):
	global s
	nbr = str(self.parent.lineNb)
	
	if self.children[1].type == 'Operation':
		self.children[1].llvm()
		s+="\nstore "+self.children[1].typeI()+" ?2?, i32* %"+str(self.children[0].tok)
	elif self.children[1].type == 'Integer' or self.children[1].type == 'Double' or self.children[1].type == 'True' or self.children[1].type == 'False':
		s+="\nstore "
		self.children[1].llvm()
		s+=", i32* %"+str(self.children[0].tok)
	elif self.children[1].type == 'Identifier':
		s+="\nstore "+self.children[1].typeI()+" %"+str(self.children[1].tok)+", i32* %"+str(self.children[0].tok)
			
	s+="\nbr label %for_"+nbr
	s+="\n\nfor_"+nbr+":"
	#s+= "\n?1? = load i32* %"+str(self.children[0].tok)
	if self.children[2].type == 'Operation':
		self.children[2].llvm()
		s+= "\n?1? = load i32* %"+str(self.children[0].tok)
		s+="\n?1? = icmp sge i32 ?2?, ?2?"
	elif self.children[2].type == 'Integer' or self.children[2].type == 'Double' or self.children[2].type == 'True' or self.children[2].type == 'False':
		s+= "\n?1? = load i32* %"+str(self.children[0].tok)
		s+="\n?1? = icmp sle i32 ?2?, "
		self.children[2].llvm()
	elif self.children[2].type == 'Identifier':
		s+= "\n?1? = load i32* %"+str(self.children[0].tok)
		s+="\n?1? = icmp sle i32 ?2?, %"+str(self.children[2].tok)
	s+="\nbr i1 ?2?, label %for_body_"+nbr+", label %for_end_"+nbr
	
@addToClass(AST.ReturnNode)
def llvm(self):
	global s
	
	a = self.children[0]
	if a.type == 'Operation':
		a.llvm()
		s+="ret "+a.typeI()+" ?2?"
	elif a.type == 'Integer' or a.type == 'Double' or a.type == 'True' or a.type == 'False' or a.type == 'Identifier':
		s+="ret " 
		a.llvm()
	else:
		s+="ret " 
		a.llvm()


@addToClass(AST.ConditionnalNode)
def llvm(self):
	global s
	nbr = self.children[0].lineNb
	s+="\nbr label %if_begin_" +str(nbr)
	s+="\n\nif_begin_" +str(nbr)+":"
	self.children[0].llvm()#les deux lignes + le corps du if
	if len(self.children)>1:#if + else/else if
		for i in range(1, len(self.children)):
			self.children[i].llvm()#les deux lignes + le corps du else if

@addToClass(AST.IfNode)
@addToClass(AST.ElseifNode)
def llvm(self):
	global s
	#s+="?2? = icmp +operator+ undef + ??1, ??2" )#fcmp si Double, icmp si i32
	a = self.children[0]
	if a.type=='Operation':
		a.llvm()
		s+="\nbr i1 ?2?, label %if_" +str(self.lineNb)+", label %end_if_" +str(self.lineNb)
	elif a.type == 'Integer' or a.type == 'Double' or a.type == 'True' or a.type == 'False':
		s+="\nbr"
		a.llvm()
		s+=", label %if_" +str(self.lineNb)+", label %end_if_" +str(self.lineNb)
	elif a.type=='Identifier':
		s+="\nbr i1 %"+str(a.tok)+", label %if_" +str(self.lineNb)+", label %end_if_" +str(self.lineNb)
	s+="\n\nif_" +str(self.lineNb)+":"
	self.children[1].llvm()
	if len(self.parent.children)>self.childNum+1:
		if self.parent.children[self.childNum+1].type == 'Else':
			s+="\nbr label %end_else_" +str(self.lineNb)
	s+="\n\nend_if_" +str(self.lineNb)+":"

@addToClass(AST.ElseNode)
def llvm(self):
	global s
	self.children[0].llvm()
	s+="\n\nend_else_" +str(self.parent.children[self.childNum-1].lineNb)+":"

@addToClass(AST.AssignNode)
def llvm(self):
	global s
	a = self.children[1]
	if a.type == 'Operation':
		a.llvm()
		s+="\nstore "+a.typeI()+" ?2?, " 
		s += self.children[0].typeI()+"* %"+str(self.children[0].tok)
	elif a.type == 'Function call':
		a.llvm()
		s+="\nstore "+a.children[0].typeI()+" ?2?, "+self.children[0].typeI()+"* %"+str(self.children[0].tok)
	elif self.children[0].type != 'List element':
		s+="\nstore " 
		if a.type == 'Identifier':
			s += a.typeI()+"* %"+str(a.tok)+" "
			a.llvm()
		elif a.type == a.type == 'Integer' or a.type == 'Double' or a.type == 'True' or a.type == 'False': 
			a.llvm()		
		else:
			s+= a.type
			a.llvm()
		s += ", "+self.children[0].typeI()+"* %"+str(self.children[0].tok)

@addToClass(AST.WhileNode)
def llvm(self):
	global s
	s+= "\nbr label %while_"+str(self.lineNb)
	s+="\n\nwhile_" +str(self.lineNb)+":"
	self.children[0].llvm()
	s+="\nbr i1 ?2?, label %"
	s+="while_body_" +str(self.lineNb)
	s+=", label %"
	s+="while_end_" +str(self.lineNb)
	s+="\n\nwhile_body_" +str(self.lineNb)+":"
	self.children[1].llvm()
	s+="\nbr label %"
	s+="while_" +str(self.lineNb)
	s+="\n\nwhile_end_" +str(self.lineNb)+":"

@addToClass(AST.FuncCallNode)
def llvm(self):
	global s
	for i in range(0, len(self.children)):
		if self.children[i].type == 'Operation':
			self.children[i].llvm()
	s+="?1? = call "+self.children[0].typeI()+" @"+str(self.children[0].tok)+"("
	for i in range(1, len(self.children)):
		if self.children[i].type == 'Identifier' or self.children[i].type == 'Integer' or self.children[i].type == 'Double' or self.children[i].type == 'True' or self.children[i].type == 'False': 
			self.children[i].llvm()
		elif self.children[i].type == 'Operation':
			s+= self.children[i].typeI()+" %2%" 
		if (i != len(self.children)-1):
			s+=", "
	s+=")"

@addToClass(AST.DisplayNode)#incomplete
def llvm(self):
	global s
	global e
	a = self.children[0]
	
	if a.type == 'Identifier':
		s += "\n?1? = load "+a.typeI()+"* %"+str(a.tok)
	
	s+="\ncall void @display_"
	if a.type == 'Integer' or a.typeI() == 'i32':
		s+= "i(i32 " 
	elif a.type == 'Double' or a.typeI() == 'double':
		s+= "f(double " 
	elif a.type == 'True' or a.type == 'False' or a.typeI() == 'i1':
		s+= "b(i1 "

	if a.type == 'Identifier':
		s+="?2?)"
	else:
		s+=str(self.children[0].tok)+ ")"
	


###############################################################

if __name__ == "__main__":
	from parsing import parse
	import sys, os
	prog = file(sys.argv[1]).read()
	ast = parse(prog)
	
	entry = thread(ast)
	entry.semAnalysis()
	
	global lists
	lists = []
	entry.findList()
	print(lists)
	
	global s
	s = ""
	global e
	e = ""
	ast.llvm()
	print e
	
	outfile = open('generatedLlvm.ll', 'w')
	outfile.write(s)
	outfile.close()
	print "llvm wrote to generatedLlvm.ll"





