#############################################################################################
#  semantic.py,																				#
#																							#
# Semantic analyser for the Raccoon language.												#
#																							#
# This module adds functions to the nodes of the AST. The first part of these functions		#
# permits the "couture" of the AST, allowing a particular traversing of the tree,			#
# which will then be useful to the second part of these functions which performs the		#
# actual semantic analysis.																	#
#																							#
# May 2015, CATUSANU Paul, EWBANK Tom and VAN DE GOOR Elodie.								#
#############################################################################################

import AST
from AST import * 
from lexical import NestComError

#### Functions for the "couture" of the AST ####

@addToClass(AST.Node)
def thread(self, lastNode):
	for c in self.children:
		lastNode = c.thread(lastNode)
	lastNode.addNext(self)
	return self
	
def thread(tree):
	entry = AST.EntryNode()
	tree.thread(entry)
	return entry

#### Functions for the semantic analysis ####

def condCheck(node):
	'''Routine that needs to be executed for many of the nodes,
	   it detects if we are in a condition and in that case, 
	   it checks if the type is correct and opens a new scope'''
	if isinstance(node.parent, IfNode) or \
	   isinstance(node.parent, ElseifNode) or \
	   isinstance(node.parent, WhileNode):
		type = AST.Node.checkStack.getMergedType()
		print(type)
		if type != 'Boolean' and type != 'Integer' and type != 'Double':
			print("error l.%d: wrong type for condition" %(node.lineNb))
			AST.Node.nbSemErrors += 1
		AST.Node.checkStack.newCondScope()


@addToClass(AST.Node)	
def semAnalysis(self):
	self.next[0].semAnalysis()

@addToClass(AST.ProgramNode)	
def semAnalysis(self):
	print("Semantic analysis terminated with %d errors" %(self.nbSemErrors))
		
@addToClass(AST.AssignNode)
@addToClass(AST.ConstNode)
def semAnalysis(self):
	stack = AST.Node.checkStack
	type = stack.getMergedType()
	if type == 'Forbidden':
		print("error l.%d: unable to make the assignment because of type error(s) or uninitialized variable(s)" %(self.lineNb))
		AST.Node.nbSemErrors += 1
	elif isinstance(self.children[0], ListElementNode):
		token = self.children[0].children[0].tok
		trueType = stack.getVarType(token)
		
		if stack.hasConst(token):
			print("error l.%d: Trying to assign a new value to the constant '%s'" %(self.lineNb,token))
			AST.Node.nbSemErrors += 1
		elif trueType is not None and trueType[0:4] == 'List' and type != trueType[5:]:
			print("error l.%d: Trying to assign type %s to a list element of type %s" %(self.lineNb,type, trueType[5:]))
			AST.Node.nbSemErrors += 1
 
	else:
		token = self.children[0].tok
		trueType = stack.getVarType(token)
		
		if stack.hasConst(token):
			print("error l.%d: Trying to assign a new value to the constant '%s'" %(self.lineNb,token))
			AST.Node.nbSemErrors += 1
		elif trueType is not None and trueType != type:
			print("error l.%d: Trying to assign type %s to a variable of type %s" %(self.lineNb,type, trueType))
			AST.Node.nbSemErrors += 1
		else:
			stack.addVariable(token, type)
			self.children[0].var_type = type
			if isinstance(self, ConstNode):
				stack.addConst(token, type)
	
	self.next[0].semAnalysis()
	
@addToClass(AST.OpNode)
def semAnalysis(self):
	if not AST.Node.checkStack.mergeTypes(self.op):
		print("error l.%d: operation members have incompatible or erroneous types" %(self.lineNb))
		AST.Node.nbSemErrors += 1
		
	if isinstance(self.parent, BodyNode) or isinstance(self.parent, ProgramNode):
		# It means the statement is a simple operation that doesn't have any effect or purpose,
		# so we need to pop out of the stack the resulting merged type to make the rest of the analysis work
		AST.Node.checkStack.getMergedType()
	
	condCheck(self)
	
	self.next[0].semAnalysis()
	
@addToClass(AST.IntNode)
def semAnalysis(self):
	if not(isinstance(self.parent, BodyNode) or isinstance(self.parent, ProgramNode)):
		AST.Node.checkStack.pushType('Integer')
		print("pushed int %s" %(self.tok))
	
	condCheck(self)
	
	self.next[0].semAnalysis()
	
@addToClass(AST.DoubleNode)
def semAnalysis(self):
	if not(isinstance(self.parent, BodyNode) or isinstance(self.parent, ProgramNode)):
		AST.Node.checkStack.pushType('Double')
		print("pushed dou %s" %(self.tok))
		
	condCheck(self)
		
	self.next[0].semAnalysis()
	
@addToClass(AST.TrueNode)
@addToClass(AST.FalseNode)
def semAnalysis(self):
	if not(isinstance(self.parent, BodyNode) or isinstance(self.parent, ProgramNode)):
		AST.Node.checkStack.pushType('Boolean')
		print("pushed bool %s" %(self.type))
		
	condCheck(self)
		
	self.next[0].semAnalysis()
	
# @addToClass(AST.StringNode)
# def semAnalysis(self):
	# if not(isinstance(self.parent, BodyNode) or isinstance(self.parent, ProgramNode)):
		# AST.Node.checkStack.pushType('String')
	# self.next[0].semAnalysis()
	
@addToClass(AST.ListNode)
def semAnalysis(self):
	for i in range(1, len(self.children)): 
		AST.Node.checkStack.mergeTypes()

	listType = AST.Node.checkStack.getMergedType()
	self.var_type = listType
	
	if listType == 'Forbidden':
		print("error l.%d: all list elements must be the same type and not lists" %(self.lineNb))
		AST.Node.nbSemErrors += 1
		AST.Node.checkStack.pushType(listType)
		print("pushed %s" %(listType))
	else:
		AST.Node.checkStack.pushType('List '+listType)
		print("pushed List %s" %(listType))
		
	
	self.next[0].semAnalysis()

@addToClass(AST.IdNode)
def semAnalysis(self):
	if not(isinstance(self.parent, BodyNode) or isinstance(self.parent, ProgramNode)):
		type = AST.Node.checkStack.getVarType(self.tok)
		if type is None:
			print("error l.%d: uninitialized variable '%s'" %(self.lineNb,self.tok))
			AST.Node.nbSemErrors += 1
			AST.Node.checkStack.pushType('Forbidden') # permits to still continue the analysis 
			print("pushed forbid %s" %(self.tok))
		else:
			if isinstance(self.parent, ListElementNode) and \
			   self is self.parent.children[0] and type[0:4] == 'List':
				# means the type will be 'List some_type'  
				# and we just want to push the 'some_type' on the typeStack
				AST.Node.checkStack.pushType(type[5:])
				self.var_type = type[5:]
				print("pushed %s %s" %(type[5:],self.tok))
				
			else:
				AST.Node.checkStack.pushType(type)
				self.var_type = type
				print("pushed %s %s" %(type,self.tok))
	
	condCheck(self)
	
	self.next[0].semAnalysis()
	
@addToClass(AST.ListElementNode)
def semAnalysis(self):
	stack = AST.Node.checkStack
	token = self.children[0].tok
	
	#check if the index is an integer
	type = stack.getMergedType()
	if type != 'Integer':
		print("error l.%d: wrong type for index, an integer is needed" %(self.lineNb))
		AST.Node.nbSemErrors += 1
	
	type = stack.getVarType(token)
	if stack.hasVariable(token) and type[0:4] != 'List':
		print("error l.%d: '%s' is not a list" %(self.lineNb,token))
		AST.Node.nbSemErrors += 1
	else:
		self.var_type = type
		
	condCheck(self)
	
	self.next[0].semAnalysis()


@addToClass(AST.WhileNode)
@addToClass(AST.IfNode)
@addToClass(AST.ElseifNode)
def semAnalysis(self):
	AST.Node.checkStack.closeCondScope()
	
	if isinstance(self, ElseifNode):
		i = 0
		for node in self.parent.children:
			if node is self:
				break
			i += 1
		if i < len(self.parent.children) and isinstance(self.parent.children[i+1], ElseNode):
			AST.Node.checkStack.newCondScope()
	
	self.next[0].semAnalysis()

@addToClass(AST.ElseNode)
@addToClass(AST.ForNode)
def semAnalysis(self):
	AST.Node.checkStack.closeCondScope()
	self.next[0].semAnalysis()

@addToClass(AST.HeadNode)
def semAnalysis(self):
	if AST.Node.checkStack.hasFunction(self.children[0].tok):
		#polymorphism not allowed
		print("error l.%d: function '%s' already defined" %(self.lineNb,self.children[0].tok))
		AST.Node.nbSemErrors += 1
	else:
		typeList = []
		for argument in self.children[1:]:
			typeList.append(argument.var_type)
		AST.Node.checkStack.addFunction(self.children[0].tok, FuncArguments(typeList))
	
	AST.Node.checkStack.newFunScope() # analyse scope of the function even if it was already defined
	for argument in self.children[1:]:
		AST.Node.checkStack.addVariable(argument.tok,argument.var_type)
	
	self.next[0].semAnalysis()
	
@addToClass(FuncCallNode)
def semAnalysis(self):
	args = AST.Node.checkStack.getArguments(self.children[0].tok)
	if args is None:
		print("error l.%d: undefined function '%s'" %(self.lineNb,self.children[0].tok))
		AST.Node.nbSemErrors += 1
	else:
		if len(self.children)-1 != args.getArgNumber(): 
			print("error l.%d: wrong number of arguments for function '%s'" %(self.lineNb,self.children[0].tok))
			AST.Node.nbSemErrors += 1
		else:
			# Check if the type of the arguments is correct
			typeList = []
			for argument in reversed(self.children[1:]):
				if isinstance(argument, IdNode) or isinstance(argument, ListElementNode):
					typeList.append(argument.var_type)
				elif isinstance(argument, IntNode):
					typeList.append('Integer')
				elif isinstance(argument, DoubleNode):
					typeList.append('Double')
				# elif isinstance(argument, StringNode):
					# typeList.append('String')
				elif isinstance(argument, TrueNode) or isinstance(argument, FalseNode):
					typeList.append('Boolean')
				else:
					typeList.append(AST.Node.checkStack.getMergedType)
			
			typeList.reverse()
			if not(args.compare(typeList)):
				print("error l.%d: wrong types of arguments for function '%s'" %(self.lineNb,self.children[0].tok))
				AST.Node.nbSemErrors += 1
			
	self.next[0].semAnalysis()

@addToClass(AST.FuncDefNode)
def semAnalysis(self):
	AST.Node.checkStack.closeFunScope()
	self.next[0].semAnalysis()
	
@addToClass(AST.NumIteratorNode)
def semAnalysis(self):
	type = AST.Node.checkStack.getVarType(self.tok)
	if type is None:
		AST.Node.checkStack.addVariable(self.tok,'Integer')
	elif type != 'Integer':
		print("error l.%d: variable '%s' is already defined and not of a valid numeric iterator type (Int)" %(self.lineNb,self.tok))
		AST.Node.nbSemErrors += 1
	elif AST.Node.checkStack.hasConst(self.tok):
		print("error l.%d: variable '%s' is already defined as a constant and can't be used as a numeric iterator" %(self.lineNb,self.tok))
		AST.Node.nbSemErrors += 1
	else:
		self.var_type = 'Integer'
	
	self.next[0].semAnalysis()
	
@addToClass(AST.ListIteratorNode)
def semAnalysis(self):
	if AST.Node.checkStack.hasConst(self.tok):
		print("error l.%d: variable '%s' is already defined as a constant and can't be used as an iterator" %(self.lineNb,self.tok))
		AST.Node.nbSemErrors += 1
		
	self.next[0].semAnalysis()
	
@addToClass(AST.InRangeNode)
def semAnalysis(self):
	type2 = AST.Node.checkStack.getMergedType()
	type1 = AST.Node.checkStack.getMergedType()
	if type1 != 'Integer' and type1 != 'Forbidden':
		print("error l.%d: first type of range should be integer" %(self.lineNb))
		AST.Node.nbSemErrors += 1
	if type2 != 'Integer' and type2 != 'Forbidden':
		print("error l.%d: second type of range should be integer" %(self.lineNb))
		AST.Node.nbSemErrors += 1
	
	AST.Node.checkStack.newCondScope()
	
	self.next[0].semAnalysis()
	
@addToClass(AST.InNode)
def semAnalysis(self):
	iterTok = self.children[0].tok
	listTok = self.children[1].tok
	iterType = AST.Node.checkStack.getVarType(iterTok)
	listType = AST.Node.checkStack.getMergedType()
	if listType is None:
		print("error l.%d: variable '%s' is undefined" %(self.lineNb,listTok))
		AST.Node.nbSemErrors += 1
	elif listType[0:4] != 'List':
		print("error l.%d: '%s' is not a list" %(self.lineNb,listTok))
		AST.Node.nbSemErrors += 1
	elif iterType is None:
		AST.Node.checkStack.addVariable(iterTok,listType[5:])
		self.children[0].var_type = listType[5:]
		if AST.Node.checkStack.hasConst(listTok):
			AST.Node.checkStack.addConst(iterTok,iterType)
	elif iterType != listType[5:]:
		print("error l.%d: variable '%s' is already defined and not of the valid list iterator type (%s)" %(self.lineNb,iterTok,listType[5:]))
		AST.Node.nbSemErrors += 1
	
	AST.Node.checkStack.newCondScope()
	
	self.next[0].semAnalysis()

@addToClass(AST.ReturnNode)
def semAnalysis(self):
	node = self
	while not isinstance(node.parent, FuncDefNode):
		if node.parent == None: #we reached the root of the tree without finding function node
			print("error l.%d: return statement not in a function" %(self.lineNb))
			AST.Node.nbSemErrors += 1
			break
		else:
			node = node.parent

	self.next[0].semAnalysis()
	
@addToClass(AST.BreakNode)
@addToClass(AST.ContinueNode)
def semAnalysis(self):
	node = self
	while not isinstance(node.parent, ForNode) and not isinstance(node.parent, WhileNode):
		if node.parent == None: #we reached the root of the tree without finding loop node
			print("error l.%d: break/continue statement not in a loop" %(self.lineNb))
			AST.Node.nbSemErrors += 1
			break
		else:
			node = node.parent
	self.next[0].semAnalysis()
		

###############################################################
		
if __name__ == "__main__":
	try:
		from parsing import parse
		import sys, os
		import lexical

		prog = file(sys.argv[1]).read()
		ast = parse(prog)
		
		print("Lexical analysis terminated with %d errors" %(lexical.nbLexErrors))
		print("Syntactic analysis terminated with %d errors" %(AST.Node.nbSynErrors))
			
		if not(AST.Node.nbSynErrors > 0 or lexical.nbLexErrors > 0):
			entry = thread(ast)
			
			if len(sys.argv) == 3 and sys.argv[2] == "-ast" :
				graph = ast.makegraphicaltree()
				entry.threadTree(graph)
				name = os.path.splitext(sys.argv[1])[0]+"-ast-threaded.pdf"
				graph.write_pdf(name)
				print("wrote threaded ast to '%s'" %name)
			
			entry.semAnalysis()
	except NestComError, e:
		print("ERROR:")
		print(e.msg)