
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
					while (char != '\n') and (k >0):
						k -= 1
						char = result[k]
						# if "define" encountered in the line, variable is an argument and don't need an "alloc"
						if k+6 <= len(result) and result[k:k+6] == "define":
							allocNeeded = False
							break							
				else: allocNeeded = False
			
			if allocNeeded:
				#print("alloc added")
				if varName[1] == 'I':
					alloca = " = alloca i32 "
					result = result[0:k+1] + "  " + varName + alloca + result[k:]
				elif varName[1] == 'D': 
					alloca = " = alloca double "
					result = result[0:k+1] + "  " + varName + alloca + result[k:]
				elif varName[1] == 'B':
					alloca = " = alloca i1 "
					result = result[0:k+1] + "  " + varName + alloca + result[k:]
				elif varName[1:3] == 'LI':
					alloca = " = alloca i32* "
					result = result[0:k+1] + "  " + varName + alloca + result[k:]
				elif varName[1:3] == 'LD':
					alloca = " = alloca double* "
					result = result[0:k+1] + "  " + varName + alloca + result[k:]
				elif varName[1:3] == 'LB':
					alloca = " = alloca i1* "
					result = result[0:k+1] + "  " + varName + alloca + result[k:]
				else:
					print("llvm error: unknown type for '%s'" %varName)
					
				
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
		lists.append(str(self.parent.children[0].getLlvmTok()))
		lists.append(len(self.children))
	self.next[0].findList()
	
@addToClass(AST.DisplayNode)
def findList(self):
	global printlists
	if self.children[0].typeI()=='i32*' :
		printlists.append(self.children[0].getLlvmTok())
	self.next[0].findList()
	
@addToClass(AST.Node)	
def llvm(self):
	global s
	s+= str(self.lineNb) + self.type
	
@addToClass(AST.ProgramNode)	
def llvm(self):
	global s
	global end
	#lecture de l'arbre
	for i in self.children:
		i.llvm()
	snew =""
	snew = ''.join(s)
	#Ajout des alloc
	s = add_alloc(snew)

	
	snew = s.replace("   "," ") 
	s = snew.replace("  "," ") 
	#incertion des fonction display pour les floats, les integers et les boolens (identifier compris)
	end += "\n\n@.strf = private unnamed_addr constant [4 x i8] c\"%f\\0A\\00\"\ndefine void @display_f(float %n)  {\nentry:\n  %n.addr = alloca float\n  store float %n, float* %n.addr\n  %0 = load float* %n.addr\n  %1 = fpext float %0 to double\n  %2 = getelementptr inbounds [4 x i8]* @.strf, i32 0, i32 0\n  %call = call i32 (i8*, ...)* @printf(i8* %2, double %1)\n  ret void\n}\n\n@.str = private unnamed_addr constant [4 x i8] c\"%d\\0A\\00\"	\ndefine void @display_i(i32 %n) {\nentry:\n  %n.addr = alloca i32\n  store i32 %n, i32* %n.addr\n  %0 = load i32* %n.addr\n  %1 = getelementptr inbounds [4 x i8]* @.str, i32 0, i32 0\n  %2 = call i32 (i8*, ...)* @printf(i8* %1, i32 %0)\n  ret void\n}\ndefine void @display_b(i1 %n) {\nentry:\n  %n.addr = alloca i1\n  store i1 %n, i1* %n.addr\n  %0 = load i1* %n.addr\n  %1 = getelementptr inbounds [4 x i8]* @.str, i32 0, i32 0\n  %2 = call i32 (i8*, ...)* @printf(i8* %1, i1 %0)\n  ret void\n}\n\n\ndeclare i32 @printf(i8*, ...)\n\n"
	#insertion d'une fonction d'affichage adapte a la demande
	
	s+=end  

@addToClass(AST.FuncDefNode)
def llvm(self):
	global s
	a = self.children[0] 
	a.llvm()#head
	s+="{\n\nentry: "
	for i in range(1, len(a.children)):
		s+="\nstore "+str(a.children[i].typeI())+" %"+str(a.children[i].getLlvmTok()).replace(" ","")+"_arg, "+a.children[i].typeI()+"* %"+str(a.children[i].getLlvmTok())
	self.children[1].llvm()#body
	if self.children[0].children[0].typeI()=='void':
		s+="\nret void\n} "# a return read only if there is no return un the function
	else:
		s+="\nret "+ self.children[0].children[0].typeI()+" 0\n} "# a return read only if there is no return un the function
	
	#remplacement des ?1? et ?2? par %0, %1, %2, etc
	i=0
	sstr = ""
	sstr = ''.join(s)
	while 1:              
		snew = sstr.replace("?1?", "%"+str(i),1)
		snew = snew.replace("?2?", "%"+str(i),1)
		if sstr == snew:
			break
		i=i+1
		sstr = snew
	s = [sstr]
		
@addToClass(AST.HeadNode)
def llvm(self):
	global s
	s+="\ndefine "+self.children[0].typeI()+" @"+str(self.children[0].getLlvmTok())+"("
	for i in range(1, len(self.children)):
		#self.children[i].llvm()
		#s+="_arg"
		
		s+=str(self.children[i].typeI())+" %"+str(self.children[i].getLlvmTok()).replace(" ","")+"_arg"
		if (i != len(self.children)-1):
			s+=", "
	s+=")"

@addToClass(AST.IntNode)
def llvm(self):
	global s
	s+=" i32 " +str(self.getLlvmTok())+" "
	
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
	s+="double " +str(self.getLlvmTok())+" "
	
@addToClass(AST.ListNode)
def llvm(self):
	global s
	
@addToClass(AST.TokenNode)	
def llvm(self):
	global s
	s += self.typeI()+" %"+str(self.getLlvmTok())+" "

@addToClass(AST.BodyNode)
def llvm(self):
	global s
	for i in self.children:
		s+="\n"
		i.llvm()
		
@addToClass(AST.IdNode)	
def llvm(self):
	global s
	s += self.typeI()+" %"+str(self.getLlvmTok())+" "


@addToClass(AST.TokenNode)	
@addToClass(AST.IdNode)	
@addToClass(AST.FuncCallNode)	
@addToClass(AST.FuncDefArgNode)	

@addToClass(AST.ListNode)	
@addToClass(AST.FuncDefNameNode)	
@addToClass(AST.NumIteratorNode)
def typeI(self):

	if self.var_type == 'Integer':
		return 'i32'
	elif self.var_type == 'Double':
		return 'double'
	elif self.var_type == 'Boolean':
		return 'i1'
	elif self.var_type == 'List Integer':
		return 'i32*'
	elif self.var_type == 'List Double':
		return 'double*'
	elif self.var_type == 'List Boolean':
		return 'i1*'
	elif self.var_type == 'Void':
		return 'void'
	else :
		print ("\nerror (llvm generation): unknown type: "+self.var_type)
		
@addToClass(AST.ListElementNode)
def typeI(self):
	if self.var_type == 'List Integer':
		return 'i32'
	elif self.var_type == 'List Double':
		return 'double'
	elif self.var_type == 'List Boolean':
		return 'i1'
	else :
		print ("\nerror (llvm generation): unknown type: "+self.var_type)
	
@addToClass(AST.FuncCallNameNode)
def typeI(self):
	return self.parent.typeI()
	
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
	
@addToClass(AST.OpNode)	
def typeI(self):
	if self.children[0].typeI()==self.children[1].typeI():
		return self.children[0].typeI()
	else:
		print ("\nerror: undefine type for node:"+ self.children[0].type+ " and "+self.children[1].type)

		
@addToClass(AST.OpNode)	
def llvm(self):
	global s
	if self.children[0].type == 'Operation':
		self.children[0].llvm()
	elif self.children[0].type == 'Identifier':
		s+="\n?1? = load "+self.children[0].typeI()+"* %"+str(self.children[0].getLlvmTok())
	elif self.children[0].type == 'List element':
		self.children[0].llvm()
		s+= "\n?1? = load i32* ?2?"
	
	if self.children[1].type == 'Operation':
		self.children[1].llvm()
	elif self.children[1].type == 'Identifier':
		s+="\n?1? = load "+self.children[1].typeI()+"* %"+str(self.children[1].getLlvmTok())
	elif self.children[1].type == 'List element':
		self.children[1].llvm()
		s+= "\n?1? = load i32* ?2?"
	
	s+="\n?1? = "
	#Si on a des Double, ajouter "f" juste devant
	if self.op == '+':
		s+="add"
	elif self.op == '-':
		s+="sub"
	elif self.op == '*':
		s+="mul"
	elif self.op == '/':
		if self.var_type == "Integer" or self.var_type == "Boolean":
			s+="sdiv"
		else:
			s+="fdiv"
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
	elif self.op == '%':
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
	if a.type == 'Integer' or a.type == 'Double':
		a.llvm()
		s += ", "
	elif  a.type == 'True' or a.type == 'False':
		s += " i1 "
		a.llvm()
		s += ", "
	elif a.type == 'Identifier' or a.type == 'Operation':
		s += a.typeI()+" ?2?, "	
	elif a.type == 'List element':
		s+="i32 ?2?, "
	else:
		#s+=" undef" + self.children[0].type+", "
		a.llvm()

	
	a = self.children[1]

	if a.type == 'Integer' or a.type == 'Double'  :

		s+= str(a.getLlvmTok())
		
	elif a.type == 'True' or a.type == 'False':
		s+= a.type
	elif a.type == 'Identifier' or a.type == 'Operation':
		s+= " ?2?"	
	else:
		#s+= a.type
		a.llvm()
		
	s+="\n"
		
@addToClass(AST.ForNode)
def llvm(self):
	global s
	rangeNode= self.children[0]
	if rangeNode.type == 'In range':
		rangeNode.llvm()
		s+="\n\nfor_body_"+str(self.lineNb)+":"
		self.children[1].llvm()
		s+="\n?1? = load i32* %"+str(rangeNode.children[0].getLlvmTok())
		s+="\n?1? = add i32 ?2?, 1"
		s+="\nstore "+rangeNode.children[2].typeI()+" ?2?, i32* %"+str(rangeNode.children[0].getLlvmTok())
		s+="\nbr label %for_"+str(self.lineNb)+"\n\nfor_end_"+str(self.lineNb)+":"
		
	else: 
		s+="\nbr label %for_" +str(self.lineNb)+"\n\nfor_" +str(self.lineNb)+":"
	
@addToClass(AST.InRangeNode)
def llvm(self):
	global s
	nbr = str(self.parent.lineNb)
	
	if self.children[1].type == 'Operation':
		self.children[1].llvm()
		s+="\nstore "+self.children[1].typeI()+" ?2?, i32* %"+str(self.children[0].getLlvmTok())
	elif self.children[1].type == 'Integer' or self.children[1].type == 'Double' or self.children[1].type == 'True' or self.children[1].type == 'False':
		s+="\nstore "
		self.children[1].llvm()
		s+=", i32* %"+str(self.children[0].getLlvmTok())
	elif self.children[1].type == 'Identifier':
		s+="\nstore "+self.children[1].typeI()+" %"+str(self.children[1].getLlvmTok())+", i32* %"+str(self.children[0].getLlvmTok())
			
	s+="\nbr label %for_"+nbr
	s+="\n\nfor_"+nbr+":"
	#s+= "\n?1? = load i32* %"+str(self.children[0].getLlvmTok())
	if self.children[2].type == 'Operation':
		self.children[2].llvm()
		
	s+= "\n?1? = load i32* %"+str(self.children[0].getLlvmTok())
	
	if self.children[2].type == 'Operation':
		s+="\n?1? = icmp sge i32 ?2?, ?2?"
	elif self.children[2].type == 'Integer' or self.children[2].type == 'Double' or self.children[2].type == 'True' or self.children[2].type == 'False':
		s+="\n?1? = icmp sle i32 ?2?, "
		self.children[2].llvm()
	elif self.children[2].type == 'Identifier':
		s+= "\n?1? = load i32* %"+str(self.children[2].getLlvmTok())
		s+="\n?1? = icmp sle i32 ?2?, ?2?" #str(self.children[2].getLlvmTok())
	else:
		s+="\n?1? = icmp sle i32 ?2?, ?2?" 
	
	s+="\nbr i1 ?2?, label %for_body_"+nbr+", label %for_end_"+nbr
	
@addToClass(AST.ReturnNode)
def llvm(self):
	global s
	
	a = self.children[0]
	if a.type == 'Operation':
		a.llvm()
		s+="\nret "+a.typeI()+" ?2?"
	elif a.type == 'Integer' or a.type == 'Double' or a.type == 'True' or a.type == 'False' :
		s+="\nret " 
		a.llvm()
	elif  a.type == 'Identifier':
		s+="?1? = load "+a.typeI()+"* %" +a.getLlvmTok()#%0 = load i32* %b
		s+="\nret "+a.typeI()+" ?2?" #ret i32 %0
		
		
	else:
		s+="\nret " 
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
		s+="\nbr i1 %"+str(a.getLlvmTok())+", label %if_" +str(self.lineNb)+", label %end_if_" +str(self.lineNb)
	s+="\n\nif_" +str(self.lineNb)+":"
	self.children[1].llvm()
	if (len(self.parent.children)>self.childNum+1) and (self.parent.children[self.childNum+1].type == 'Else'):
		s+="\nbr label %end_else_" +str(self.lineNb)
	else:
		s+="\nbr label %end_if_" +str(self.lineNb)
	s+="\n\nend_if_" +str(self.lineNb)+":"

@addToClass(AST.ElseNode)
def llvm(self):
	global s
	self.children[0].llvm()
	s+="\n\nend_else_" +str(self.parent.children[self.childNum-1].lineNb)+":"

@addToClass(AST.ListElementNode)
def llvm(self):
	global s
	s+="\n?1? = load i32* %"+ str(self.children[1].getLlvmTok())
	s+="\n?1? = load i32** %"+ str(self.children[0].getLlvmTok())
	s+="\n?1? = sext i32 ?2? to i64"
	s+="\n?1? = getelementptr inbounds i32* ?2?, i64 ?2?"
	
	
@addToClass(AST.AssignNode)
def llvm(self):
	global s
	global end
	a = self.children[1]
	b = self.children[0] # b becomes a
		
	if a.type == 'List':
		end+="\n@"+b.getLlvmTok()+"= global"
		nbr = len(a.children)
		end+="["+str(nbr) + " x i32] ["
		for i in a.children:
			end+="i32 "+str(i.getLlvmTok())
			if a.children[nbr-1] != i:
				end+=","
		end+="]\n"
		s+="\n?1? = getelementptr inbounds ["+str(nbr) + "x i32]* @"+b.getLlvmTok()+", i32 0, i32 0"
		s+="\nstore i32* ?2?, i32** %"+b.getLlvmTok()+"\n"
		return
			
	global counter
#gerer le type de a
	if b.type == 'List element':
		if a.type == 'List element':
			a.llvm()
			s+= " \n%ait"+str(counter)+" = load i32* ?2?"
			
		elif a.type == 'Identifier':
			s+= "\n%ait"+str(counter)+" = load "+a.typeI()+"* %"+str(a.getLlvmTok())
		else:
			print("check error in assignement")
	else:
		if a.type == 'List element':
			a.llvm()
			s+= " \n?1? = load i32* ?2?"
		elif a.type == 'Identifier':
			s+= "\n?1? = load "+a.typeI()+"* %"+str(a.getLlvmTok())
		elif a.type == 'Operation':
			a.llvm()
		elif a.type == 'Function call':
			a.llvm()

#gerer le type de b
	if b.type == 'List element':
		b.llvm()
		s+="\nstore " +a.typeI()	+ " %ait"+str(counter)+", " +b.typeI()+"* ?2?"
		counter+=1
	elif b.type == 'Assignment variable' and ( a.type == 'Integer' or a.type == 'Double' or a.type == 'True' or a.type == 'False'):
		s+="\nstore " 
		a.llvm()
		s+=", " +b.typeI()+"* %"+str(b.getLlvmTok())
	else:
		s+="\nstore " +a.typeI()	+ " ?2?, " +b.typeI()+"* %"+str(b.getLlvmTok())
	
		

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
	global counter
	j = 0
	
	for i in range(0, len(self.children)):
		
		if self.children[i].type == 'Operation':
			self.children[i].llvm()
		elif self.children[i].type == 'Identifier':
			s+="\n%arg"+str(j+counter) +"= load "+self.children[i].typeI()+"* %"+self.children[i].getLlvmTok()
			j+=1
	if self.children[0].typeI() == 'void':
		s+="\ncall void" 
	else:
		s+="\n?1? = call " +self.children[0].typeI()
	s+=" @"+str(self.children[0].getLlvmTok())+"("

	for i in range(1, len(self.children)):
		if self.children[i].type == 'Integer' or self.children[i].type == 'Double' or self.children[i].type == 'True' or self.children[i].type == 'False': 
			self.children[i].llvm()
		elif self.children[i].type == 'Operation' :
			s+= self.children[i].typeI()+" ?2?"
		elif self.children[i].type == 'Identifier':
			s+= self.children[i].typeI()+" %arg"+str(counter) 
			counter+=1
		if (i != len(self.children)-1):
			s+=", "
	s+=")\n"

@addToClass(AST.DisplayNode)
def llvm(self): 
	global s
	a = self.children[0]
	if a.type == 'Identifier':
		s += "\n?1? = load "+a.typeI()+"* %"+str(a.getLlvmTok())
	
	s+="\ncall void @display_"
	if a.type == 'Integer' or a.typeI() == 'i32':
		s+= "i(i32 " 
	elif a.type == 'Double' or a.typeI() == 'double':
		s+= "f(double " 
	elif a.type == 'True' or a.type == 'False' or a.typeI() == 'i1':
		s+= "b(i1 "
	elif a.typeI() == 'i32*': 
		s+="l_"+str(a.getLlvmTok())+"("
		
	
	if a.typeI() == 'i32*': 
		s+=")"
	elif a.type == 'Identifier':
		s+="?2?)"		
	else:
		s+=str(self.children[0].getLlvmTok())+ ")"
	

def add_displayList():
	global end
	global lists
	global printlists
	for i in printlists:
		end+="\ndefine void @display_l_"+i+"() {\nentry:"
		nbrelem =  lists[lists.index(i)+1] 
		for j in range(0,nbrelem):
			#print "add element "+str(j)
			end+= "\n%"+str(j*2)+"= getelementptr inbounds ["+str(nbrelem)+" x i32]* @"+str(i)+", i32 0, i64 "+str(j)
			end+= "\n%"+str(j*2+1)+"= load i32* %"+str(j*2)
			end+= "\ncall void @display_i(i32 %"+str(j*2+1)+")\n"
		end+="\nret void\n}\n"
		
	


###############################################################

if __name__ == "__main__":
	from parsing import parse
	import sys, os
	prog = file(sys.argv[1]).read()
	ast = parse(prog)
	
	entry = thread(ast)
	entry.semAnalysis()
	
	global s
	s = []
	global end
	end = ""
	global lists
	lists = []
	global printlists
	printlists = []
	entry.findList()
	printlists = list(set(printlists)) 
	add_displayList()
	global counter
	counter = 0
	
	ast.llvm()
	
	name = sys.argv[1].replace('.rac', '.ll')
	outfile = open(name, 'w')
	outfile.write(s)
	outfile.close()
	print "llvm wrote to "+name

#Integer, Double, Boolean et List Integer, List Double, List Boolean. 
