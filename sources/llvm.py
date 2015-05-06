#############################################################################################
#  llvm.py,																				#
#																							#
# llvm traductor for the Raccoon language.												#
#																							#
# Th																	#
#																							#
# May 2015, CATUSANU Paul, EWBANK Tom and VAN DE GOOR Elodie.								#
#############################################################################################

import AST
from AST import * 
import semantic
from semantic import * 

#### Functions for the llvm transcription ####

@addToClass(AST.Node)	
def llvm(self):
	global s
	s+= str(self.lineNb) + self.type
	#self.next[0].llvm()


@addToClass(AST.ProgramNode)	
def llvm(self):
	global s
	for i in self.children:
		s+="\n\n        //PROGRAM CHILD " + i.type 
		i.llvm()
	#remplacement des ?1? et ?2? par %0, %1, %2, etc
	#i=0
	#while 1:              
	#	snew = s.replace("?1?","%"+str(i),1)
	#	snew = snew.replace("?2?","%"+str(i),1)
	#	if s == snew:
	#		break
	#	i=i+1
	#	s = snew


@addToClass(AST.FuncDefNode)
def llvm(self):
	global s
	self.children[0].llvm()#head
	s+="{\n  entry: "
	self.children[1].llvm()#body
	s+="\n} "


@addToClass(AST.HeadNode)
def llvm(self):
	global s
	s+="\n define fastcc OO @"
	self.children[0].llvm()
	s+="("
	for i in range(1, len(self.children)):
		s+=" OO %"
		self.children[i].llvm()
		if (i != len(self.children)-1):
			s+=","
	s+=")"


@addToClass(AST.IntNode)
def llvm(self):
	global s
	#s+="%s  -   %s  -  " %( self.lineNb,self.type,self.tok))
	s+=" i32 " +str(self.tok)+" "
	

@addToClass(AST.TrueNode)
def llvm(self):
	global s
	s+=" i1 1"

@addToClass(AST.FalseNode)
def llvm(self):
	global s
	s+=" i1 0" 

@addToClass(AST.DoubleNode)
def llvm(self):
	global s
	s+="double " +str(self.tok)+" "

@addToClass(AST.TokenNode)	
def llvm(self):
	global s
	s+= str(self.tok)

@addToClass(AST.BodyNode)
def llvm(self):
	global s
	for i in self.children:
		s+="\n"
		i.llvm()
		
@addToClass(AST.IdNode)	
def llvm(self):
	global s
	s+=str(self.tok)

@addToClass(AST.OpNode)	
def llvm(self):
	global s
	if self.children[0].type == 'Operation':
		self.children[0].llvm()
	if self.children[1].type == 'Operation':
		self.children[1].llvm()
	s+="\n?1? = "
	#Si on a des float, ajouter "f" juste devant
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
		s+="!! " +self.op
		
	if self.children[0].type == 'Integer':
		s+=" i32"+str(self.children[0].tok) +","
		a=self.children[1]
		
	elif self.children[1].type == 'Integer':
		s+=" i32 "+str(self.children[1].tok)+","
		a=self.children[0]
		
	elif self.children[0].type == 'float':
		s+=" float "+str(self.children[0].tok)+","
		a=self.children[1]
		
	elif self.children[1].type == 'float':
		s+=" float"+str(self.children[1].tok)+","
		a=self.children[0]
		
	elif self.children[0].type == 'True' or self.children[0].type == 'False':
		s+=" i1 "+str(self.children[0].tok)+","
		a=self.children[1]
		
	elif self.children[0].type == 'True' or self.children[0].type == 'False':
		s+=" i1 "+str(self.children[1].tok)+","
		a=self.children[1]	
	elif self.children[0].type == 'Identifier':
		s+=" OO %"+str(self.children[0].tok)+","
		a=self.children[1]		
	else:
		s+=" OO" + self.children[0].type+","
		a=self.children[1]
		
	if a.type == 'Operation':
		s+="?2?"
	elif a.type == 'Identifier':
		s+="%"
		a.llvm()
	elif a.type == 'Integer' or a.type == 'float' or a.type == 'True' or a.type == 'False':
		s+= str(a.tok)
	else:
		s+= self.children[i].type
		
	s+="\n"
		
@addToClass(AST.ForNode)#incomplete
def llvm(self):
	global s
	rangeNode= self.children[0]
	if rangeNode.type == 'In range':
		rangeNode.llvm()
		s+="\nfor_body_"+str(self.lineNb)+" : "
		self.children[1].llvm()
		s+="\n?1? = add i32 1, %"+str(rangeNode.children[0].tok)+"\nstore i32 %"+str(rangeNode.children[0].tok)+", OO ?2? \nbr label %for_"+str(self.lineNb)+"\nfor_end_"+str(self.lineNb)+" : "
		
	else: # for iterator in list: not implemented yet
		s+="\n br label %"+"for_" +str(self.lineNb)+" : \n  for_" +str(self.lineNb)+" : "
	
@addToClass(AST.InRangeNode)
def llvm(self):
	global s
	nbr = str(self.parent.lineNb)
	
	if self.children[1].type == 'Operation':
		self.children[1].llvm()
		s+="\nstore i32 %"+str(self.children[0].tok)+", OO ?2?"
	elif self.children[1].type == 'Integer' or self.children[1].type == 'float' or self.children[1].type == 'True' or self.children[1].type == 'False':
		s+="\nstore i32 %"+str(self.children[0].tok)+","
		self.children[1].llvm()
	elif self.children[1].type == 'Identifier':
		s+="\nstore i32 %"+str(self.children[0].tok)+", %"
		self.children[1].llvm()
			
	s+="\nbr label %for_"+nbr+" : "
	s+="\nfor_"+nbr+" : "
	
	if self.children[2].type == 'Operation':
		self.children[2].llvm()
		s+="\n?1? = icmp sle i32 %" +str(self.children[0].tok)+", OO ?2?"
	elif self.children[2].type == 'Integer' or self.children[2].type == 'float' or self.children[2].type == 'True' or self.children[2].type == 'False':
		s+="\n?1? = icmp sle i32 %" +str(self.children[0].tok)+", "
		self.children[2].llvm()
	elif self.children[2].type == 'Identifier':
		s+="\n?1? = icmp sle i32 %" +str(self.children[0].tok)+", %"
		self.children[2].llvm()
	s+="\nbr i1 ?2?, label %for_body_"+nbr+", label %for_end_"+nbr
	
@addToClass(AST.ReturnNode)
def llvm(self):
	global s
	
	a = self.children[0]
	if a.type == 'Operation':
		a.llvm()
		s+="ret OO ?2?"
	elif a.type == 'Identifier':
		s+="ret 00 %"
		a.llvm()
	elif a.type == 'Integer' or a.type == 'float' or a.type == 'True' or a.type == 'False':
		s+="ret " 
		a.llvm
	else:
		s+="ret " 
		s+= a.type
	a.llvm()

@addToClass(AST.ConditionnalNode)
def llvm(self):
	global s
	nbr = self.children[0].lineNb
	s+="\n br label %"+"if_begin_" +str(nbr)
	s+="\n  if_begin_" +str(nbr)+" : "
	self.children[0].llvm()#les deux lignes + le corps du if
	if len(self.children)>1:#if + else/else if
		for i in range(1, len(self.children)):
			self.children[i].llvm()#les deux lignes + le corps du else if


@addToClass(AST.IfNode)
@addToClass(AST.ElseifNode)
def llvm(self):
	global s
	#s+="?2? = icmp +operator+ OO + ??1, ??2" )#fcmp si float, icmp si i32
	a = self.children[0]
	if a.type=='Operation':
		a.llvm()
		s+="\n br i1 ?2?, label %if_" +str(self.lineNb)+", label %"+"end_if_" +str(self.lineNb)
	elif a.type == 'Integer' or a.type == 'float' or a.type == 'True' or a.type == 'False':
		s+="\n br"+a.llvm()+", label %if_" +str(self.lineNb)+", label %"+"end_if_" +str(self.lineNb)
	elif a.type=='Identifier':
		s+="\n br i1 %"+a+llvm()+", label %if_" +str(self.lineNb)+", label %"+"end_if_" +str(self.lineNb)
	s+="\n  if_" +str(self.lineNb)+" : "
	self.children[1].llvm()
	if len(self.parent.children)>self.childNum+1:
		if self.parent.children[self.childNum+1].type == 'Else' :
			s+="\n br label %"
			s+="end_else_" +str(self.lineNb)
	s+="\n  end_if_" +str(self.lineNb)+" : "


@addToClass(AST.ElseNode)
def llvm(self):
	global s
	self.children[0].llvm()
	s+="\n  end_else_" +str(self.parent.children[self.childNum-1].lineNb)+" : "

@addToClass(AST.AssignNode)
def llvm(self):
	global s
	a = self.children[1]
	if a.type == 'Operation':
		a.llvm()
		s+="store OO %" +str(self.children[0].tok)+", OO ?2?"
	
	else:
		s+="store OO " +str(self.children[0].tok)+", "

		if a.type == 'Identifier':
			s+="OO %"
			a.llvm()
		elif a.type == 'Integer' or a.type == 'float' or a.type == 'True' or a.type == 'False':
			a.llvm()
		else:
			s+= self.children[1].type,
	

@addToClass(AST.WhileNode)
def llvm(self):
	global s
	s+= '\n br label %while_'+str(self.lineNb)
	s+="\n  while_" +str(self.lineNb)+" : "
	self.children[0].llvm()
	#s+="?2? = icmp +operator+ OO + ??1, ??2" )
	s+="\nbr i1 ?2?, label %"
	s+="while_body_" +str(self.lineNb)
	s+=", label %"
	s+="while_end_" +str(self.lineNb)
	s+="\n  while_body_" +str(self.lineNb)+" : "
	self.children[1].llvm()
	s+="\nbr label %"
	s+="while_" +str(self.lineNb)
	s+="\n  while_end_" +str(self.lineNb)+" : "

'''
@addToClass(AST.OpNode)
def llvm(self):
	global s
	s+="Type node : " %(self.type)) 


class StringNode(Node):
	type = 'String'
	def __init__(self, n, tok):
		Node.__init__(self, n)
		self.tok = tok

'''
###############################################################

if __name__ == "__main__":
	from parsing import parse
	import sys, os
	prog = file(sys.argv[1]).read()
	ast = parse(prog)
	
	entry = thread(ast)
	graph = ast.makegraphicaltree()
	entry.threadTree(graph)
	
	name = os.path.splitext(sys.argv[1])[0]+"-ast-threaded.pdf"
	graph.write_pdf(name)
	print("wrote threaded ast to", name)
	entry.semAnalysis()
	global s
	s = ""
	ast.llvm()
	print s
	
	
