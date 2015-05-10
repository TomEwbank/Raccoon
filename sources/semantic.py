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

#### Functions for the "couture" of the AST ####

@addToClass(AST.Node)
def thread(self, lastNode):
	for  c  in self.children:
		lastNode = c.thread(lastNode)
	lastNode.addNext(self)
	return self
	
def thread(tree):
	entry = AST.EntryNode()
	tree.thread(entry)
	return entry

#### Functions for the semantic analysis ####

@addToClass(AST.Node)	
def semAnalysis(self):
	self.next[0].semAnalysis()

@addToClass(AST.ProgramNode)	
def semAnalysis(self):
	print("Semantic analysis terminated with %d errors" %(self.nbSemErrors))
		
@addToClass(AST.AssignNode)
@addToClass(AST.ConstNode)
def semAnalysis(self):
	stack = AST.Node.scopeStack
	type = stack.getMergedType()
	if isinstance(self.children[0], ListElementNode):
		token = self.children[0].children[0].tok
		trueType = stack.getVarType(token)
		
		if stack.hasVariable(token) and trueType[0:4] == 'List' and type != trueType[5:] and type != 'unknown':
			print("error l.%d: Trying to assign type %s to a list element of type %s" %(self.lineNb,type, trueType[5:]))
			AST.Node.nbSemErrors += 1
		
		if stack.hasConst(token):
			print("error l.%d: Trying to assign a new value to the constant '%s'" %(self.lineNb,token))
			AST.Node.nbSemErrors += 1
			
	else:
		token = self.children[0].tok
		if stack.hasConst(token):
			print("error l.%d: Trying to assign a new value to the constant '%s'" %(self.lineNb,token))
			AST.Node.nbSemErrors += 1
		else:
			stack.addVariable(token, type)
			if isinstance(self, ConstNode):
				stack.addConst(token, type)
	
	self.next[0].semAnalysis()
	
@addToClass(AST.OpNode)
def semAnalysis(self):
	if not AST.Node.scopeStack.mergeTypes():
		print("error l.%d: operation members have incompatible types" %(self.lineNb))
		AST.Node.nbSemErrors += 1
	self.next[0].semAnalysis()
	
@addToClass(AST.IntNode)
def semAnalysis(self):
	AST.Node.scopeStack.pushType('Integer')
	self.next[0].semAnalysis()
	
@addToClass(AST.FloatNode)
def semAnalysis(self):
	AST.Node.scopeStack.pushType('Float')
	self.next[0].semAnalysis()
	
@addToClass(AST.TrueNode)
@addToClass(AST.FalseNode)
def semAnalysis(self):
	AST.Node.scopeStack.pushType('Boolean')
	self.next[0].semAnalysis()
	
@addToClass(AST.StringNode)
def semAnalysis(self):
	AST.Node.scopeStack.pushType('String')
	self.next[0].semAnalysis()
	
@addToClass(AST.ListNode)
def semAnalysis(self):
	for i in range(1, len(self.children)): 
		AST.Node.scopeStack.mergeTypes()

	listType = AST.Node.scopeStack.getMergedType()
	
	if listType == 'Forbidden':
		print("error l.%d: all list elements must be the same type" %(self.lineNb))
		AST.Node.nbSemErrors += 1
		
	AST.Node.scopeStack.pushType('List '+listType)
	self.next[0].semAnalysis()

@addToClass(AST.IdNode)
def semAnalysis(self):
	if not AST.Node.scopeStack.hasVariable(self.tok):
		print("error l.%d: uninitialized variable '%s'" %(self.lineNb,self.tok))
		AST.Node.nbSemErrors += 1
		AST.Node.scopeStack.pushType('unknown') # permits to still continue the analysis 
	else:
		type = AST.Node.scopeStack.getVarType(self.tok)
		if isinstance(self.parent, ListElementNode) and \
		   self is self.parent.children[0]:
				# means the type will be 'List some_type' or 
				# 'unknown' (because list passed as an argument) 
				# and we just want to push the 'some_type' on the typeStack
				if type == 'unknown':
					AST.Node.scopeStack.pushType(type)
				else:
					AST.Node.scopeStack.pushType(type[5:]) 
			
		else:
			AST.Node.scopeStack.pushType(type)
	
	self.next[0].semAnalysis()
	
@addToClass(AST.ListElementNode)
def semAnalysis(self):
	stack = AST.Node.scopeStack
	token = self.children[0].tok
	
	#check if the index is an integer
	type = stack.getMergedType()
	if type != 'Integer' and \
	   type != 'unknown' :
		print("error l.%d: wrong type for index" %(self.lineNb))
		AST.Node.nbSemErrors += 1
	
	# If we realize that the id of the list exists in the scope,
	# but has the type 'unknown', it means it was passed as arguments
	# and now we now that it is a list so we can update the type to 
	# 'List unknown' for further semantic checking
	if stack.hasVariable(token) and stack.getVarType(token) == 'unknown':
		stack.addVariable(token, 'List unknown')
	elif stack.hasVariable(token) and stack.getVarType(token)[0:4] != 'List':
		print("error l.%d: '%s' is not a list" %(self.lineNb,token))
		AST.Node.nbSemErrors += 1
	
	self.next[0].semAnalysis()


@addToClass(AST.WhileNode)
@addToClass(AST.IfNode)
@addToClass(AST.ElseifNode)
def semAnalysis(self):
	type = AST.Node.scopeStack.getMergedType()
	if type != 'Float' and \
	   type != 'Integer' and \
	   type != 'Boolean' and \
	   type != 'unknown' :
		print("error l.%d: wrong type for condition" %(self.lineNb))
		AST.Node.nbSemErrors += 1
	
	self.next[0].semAnalysis()
	

@addToClass(AST.HeadNode)
def semAnalysis(self):
	if AST.Node.scopeStack.hasFunction(self.children[0].tok):
		#polymorphism not allowed
		print("error l.%d: function '%s' already defined" %(self.lineNb,self.children[0].tok))
		AST.Node.nbSemErrors += 1
	else:
		AST.Node.scopeStack.addFunction(self.children[0].tok, len(self.children)-1)
	
	# analyse scope of the function even if it was already defined
	AST.Node.scopeStack.newScope()
	for argument in self.children[1:]:
		AST.Node.scopeStack.addVariable(argument.tok,'unknown')
	
	self.next[0].semAnalysis()
	
@addToClass(FuncCallNode)
def semAnalysis(self):
	if not AST.Node.scopeStack.hasFunction(self.children[0].tok):
		print("error l.%d: undefined function '%s'" %(self.lineNb,self.children[0].tok))
		AST.Node.nbSemErrors += 1
	else:
		if len(self.children)-1 != AST.Node.scopeStack.getArgNumber(self.children[0].tok): 
			print("error l.%d: wrong number of arguments for function '%s'" %(self.lineNb,self.children[0].tok))
			AST.Node.nbSemErrors += 1
			
	self.next[0].semAnalysis()

@addToClass(AST.FuncDefNode)
def semAnalysis(self):
	AST.Node.scopeStack.pop()
	self.next[0].semAnalysis()
	
@addToClass(AST.NumIteratorNode)
def semAnalysis(self):
	if AST.Node.scopeStack.hasVariable(self.tok):
		self.prev_type = AST.Node.scopeStack.getVarType(self.tok)
	AST.Node.scopeStack.addVariable(self.tok,'Integer')
	self.next[0].semAnalysis()
	
@addToClass(AST.ListIteratorNode)
def semAnalysis(self):
	if AST.Node.scopeStack.hasVariable(self.tok):
		self.prev_type = AST.Node.scopeStack.getVarType(self.tok)
	AST.Node.scopeStack.addVariable(self.tok,'unknown')
	self.next[0].semAnalysis()
	
@addToClass(AST.ForNode)
def semAnalysis(self):
	type = self.children[0].children[0].prev_type
	token = self.children[0].children[0].tok
	if type == 'None':
		AST.Node.scopeStack.removeVariable(token)
	else:
		AST.Node.scopeStack.addVariable(token,type)
	self.next[0].semAnalysis()
	
@addToClass(AST.InRangeNode)
def semAnalysis(self):
	type1 = AST.Node.scopeStack.getMergedType()
	type2 = AST.Node.scopeStack.getMergedType()
	if type1 != 'Integer' and type1 != 'unknown':
		print("error l.%d: range first type should be integer" %(self.lineNb))
		AST.Node.nbSemErrors += 1
	if type2 != 'Integer' and type2 != 'unknown':
		print("error l.%d: range second type should be integer" %(self.lineNb))
		AST.Node.nbSemErrors += 1
	self.next[0].semAnalysis()
	
@addToClass(AST.InNode)
def semAnalysis(self):
	type = AST.Node.scopeStack.getMergedType()
	if type[0:4] != 'List' and type != 'unknown':
		print("error l.%d: '%s' is not a list" %(self.lineNb,self.children[1].tok))
		AST.Node.nbSemErrors += 1
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

		if AST.Node.nbSynErrors > 0 or lexical.nbLexErrors > 0:
			print("Lexical analysis terminated with %d errors" %(lexical.nbLexErrors))
			print("Syntactic analysis terminated with %d errors" %(AST.Node.nbSynErrors))
		else:
			entry = thread(ast)
			
			if len(sys.argv) == 3 and sys.argv[2] == "-ast" :
				graph = ast.makegraphicaltree()
				entry.threadTree(graph)
				name = os.path.splitext(sys.argv[1])[0]+"-ast-threaded.pdf"
				graph.write_pdf(name)
				print("wrote threaded ast to '%s'" %name)
			
			entry.semAnalysis()
	except NameError as e:
		print("error:")
		print(e)