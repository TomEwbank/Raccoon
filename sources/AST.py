#############################################################################################
#  AST.py,																					#
#																							#
# Module which permits to construct, manipulate and represent abstract syntax trees.		#
#																							#
# This module uses Pydot and Graphviz to represent the tree either in an ASCII-art format,	#
# either in a more readable pdf graph.														#
#																							#
# This module is derived from the module of Matthew AMIGUET and has been adapted to be		#
# used specifically for the development of a compiler for the Raccoon language.				#
#																							#
# May 2015, CATUSANU Paul, EWBANK Tom and VAN DE GOOR Elodie.								#
#############################################################################################

import pydot

class FuncInformarion:
	'''Data structure holding the types of the arguments of a function'''
	
	def __init__(self, typeList, returnType):
		self.argList = typeList
		self.argNumber = len(typeList)
		self.retType = returnType
	
	def getArgNumber(self):
		return self.argNumber
	
	def getReturnType(self):
		return self.retType
		
	def compare(self, types):
		if self.argList == types:
			return True
		else: 
			return False
			

class Scope:
	'''Class which goal is to keep track of variables 
	   initialization, function definitions, and types of 
	   expressions inside a particular scope of a Raccoon 
	   program.'''

	def __init__(self):
		self.typeStack = []
		self.varHash = {}
		self.constHash = {}
		self.funcHash = {}
	
	def addVariable(self, varName, type):
		self.varHash[varName] = type
	
	def hasVariable(self, varName):
		return self.varHash.has_key(varName)
	
	def addConst(self, varName, type):
		self.constHash[varName] = type
	
	def hasConst(self, varName):
		return self.constHash.has_key(varName)
	
	def addFunction(self, funcName, infos):
		self.funcHash[funcName] = infos
	
	def hasFunction(self, funcName):
		return self.funcHash.has_key(funcName)
		
	def removeVariable(self, varName):
		self.varHash.pop(varName, 0)
		
	def getArguments(self, funcName):
		return self.funcHash.get(funcName)
		
	def getVarType(self, varName):
		return self.varHash.get(varName)
	
	def pushType(self, type):
		self.typeStack.append(type)
		
	def mergeTypes(self, op=None):
		'''Compare the last 2 types that has been pushed on
		   the stack, and merge them into one if they are compatible'''
		  
		if len(self.typeStack) < 2:
			return -1
		
		type1 = self.typeStack.pop()
		type2 = self.typeStack.pop()
		print("merge %s and %s" %(type1,type2))
		
		if type1[0:4] == 'List' or type2[0:4] == 'List' or \
		   type1 != type2 or type1 == 'Forbidden' :
			# Raccoon can't deal with arithmetic/combinatory operation on lists,
			# and it also doesn't support casting
			self.typeStack.append('Forbidden')
			return False
		else:
			if op is None or \
			   op == '+' or op == '-' or op == '*' or op == '/' or op == '%':
				self.typeStack.append(type1)
			else:
				self.typeStack.append('Boolean')
			return True

	def getMergedType(self):
		'''Return the type at the top of the stack,
		   which is supposed to be the type of the last
		   encountered expression'''
		print("pop type")
		if len(self.typeStack) > 0:
			return self.typeStack.pop()
		else:
			return 'error'
	

class ScopeStack:
	'''Class which goal is to manage the different scopes
	   that can be encountered in a Raccoon program'''
	   
	def __init__(self):
		self.stack = [Scope()]
		self.currentScope = 0
		self.scopeNumber = 1
		
	def newScope(self):
		self.currentScope += 1
		self.scopeNumber += 1
		self.stack.append(Scope())
	
	def pop(self):
		self.stack.pop()
		self.currentScope -= 1
		self.scopeNumber -= 1
	
	def addVariable(self, varName, type):
		self.stack[self.currentScope].addVariable(varName, type)
		
	def removeVariable(self, varName):
		self.stack[self.currentScope].removeVariable(varName)
	
	def hasVariable(self, varName):
		return self.stack[self.currentScope].hasVariable(varName)
	
	def addConst(self, varName, type):
		self.stack[self.currentScope].addConst(varName, type)
		
	def hasConst(self, varName):
		return self.stack[self.currentScope].hasConst(varName)
		
	def addFunction(self, funcName, infos):
		self.stack[self.currentScope].addFunction(funcName, infos)
	
	def hasFunction(self, funcName):
		for scope in self.stack:
			if scope.hasFunction(funcName):
				return True
							
		return False
		
	def getArguments(self, funcName):
		for scope in self.stack:
			infos = scope.getArguments(funcName)
			if not (infos is None): 
				return infos
							
		return None
	
	def getVarType(self, varName):
		return self.stack[self.currentScope].getVarType(varName)
	
	def pushType(self, type):
		self.stack[self.currentScope].pushType(type)
		
	def mergeTypes(self, op=None):
		return self.stack[self.currentScope].mergeTypes(op)
	
	def getMergedType(self):
		return self.stack[self.currentScope].getMergedType()

class CondScopeStack(ScopeStack):
	def __init__(self):
		self.stack = []
		self.currentScope = -1
		self.scopeNumber = 0
		
	def hasCondScope(self):
		if self.scopeNumber == 0:
			return False
		else:
			return True
	
	def hasVariable(self, varName):
		for scope in self.stack:
			if scope.hasVariable(varName):
				return True
							
		return False
		
	def hasConst(self, varName):
		for scope in self.stack:
			if scope.hasConst(varName):
				return True
							
		return False
	
	def hasFunction(self, funcName):
		for scope in self.stack:
			if scope.hasFunction(funcName):
				return True
							
		return False
	
	def getVarType(self, varName):
		for scope in self.stack:
			type = scope.getVarType(varName)
			if not (type is None):
				return type
		
		return None

class CondScopeStackStack:
	
	def __init__(self):
		self.stack = [CondScopeStack()]
		self.currentStack = 0
		self.stackNumber = 1
	
	def newCondScopeStack(self):
		self.stack.append(CondScopeStack())
		self.currentStack += 1
		self.stackNumber += 1
	
	def popCondScopeStack(self):
		self.stack.pop()
		self.currentStack -= 1
		self.stackNumber -= 1
		
	def newCondScope(self):
		self.stack[self.currentStack].newScope()
		
	def popCondScope(self):
		self.stack[self.currentStack].pop()
		
	def hasCondScope(self):
		return self.stack[self.currentStack].hasCondScope()
		
	def addVariable(self, varName, type):
		self.stack[self.currentStack].addVariable(varName, type)
		
	def removeVariable(self, varName):
		self.stack[self.currentStack].removeVariable(varName)
	
	def hasVariable(self, varName):
		return self.stack[self.currentStack].hasVariable(varName)
	
	def addConst(self, varName, type):
		self.stack[self.currentStack].addConst(varName, type)
		
	def hasConst(self, varName):
		return self.stack[self.currentStack].hasConst(varName)
		
	def addFunction(self, funcName, infos):
		self.stack[self.currentStack].addFunction(funcName, infos)
	
	def hasFunction(self, funcName):
		return self.stack[self.currentStack].hasFunction(funcName)

	def getArguments(self, funcName):
		return self.stack[self.currentStack].getArguments(funcName)
	
	def getVarType(self, varName):
		return self.stack[self.currentStack].getVarType(varName)
	
	def pushType(self, type):
		self.stack[self.currentStack].pushType(type)
		
	def mergeTypes(self, op=None):
		return self.stack[self.currentStack].mergeTypes(op)
	
	def getMergedType(self):
		return self.stack[self.currentStack].getMergedType()


class CheckStack:
	
	def __init__(self):
		self.scopeStack = ScopeStack()
		self.condScopeStackStack = CondScopeStackStack()
	
	def newFunScope(self):
		self.scopeStack.newScope()
		self.condScopeStackStack.newCondScopeStack()
	
	def closeFunScope(self):
		self.scopeStack.pop()
		self.condScopeStackStack.popCondScopeStack()
		
	def newCondScope(self):
		self.condScopeStackStack.newCondScope()
	
	def closeCondScope(self):
		self.condScopeStackStack.popCondScope()
	
	def addVariable(self, varName, type):
		if self.condScopeStackStack.hasCondScope():
			self.condScopeStackStack.addVariable(varName, type)
		else:
			self.scopeStack.addVariable(varName, type)
		
	def removeVariable(self, varName):
		if self.condScopeStackStack.hasCondScope():
			self.condScopeStackStack.removeVariable(varName)
		else:
			self.scopeStack.removeVariable(varName)
	
	def hasVariable(self, varName):
		if self.scopeStack.hasVariable(varName) or self.condScopeStackStack.hasVariable(varName):
			return True
		else:
			return False
	
	def addConst(self, varName, type):
		if self.condScopeStackStack.hasCondScope():
			self.condScopeStackStack.addConst(varName, type)
		else:
			self.scopeStack.addConst(varName, type)
		
	def hasConst(self, varName):
		if self.scopeStack.hasConst(varName) or self.condScopeStackStack.hasConst(varName):
			return True
		else:
			return False
		
	def addFunction(self, funcName, infos):
		if self.condScopeStackStack.hasCondScope():
			self.condScopeStackStack.addFunction(funcName, infos)
		else:
			self.scopeStack.addFunction(funcName, infos)
	
	def hasFunction(self, funcName):
		if self.scopeStack.hasFunction(funcName) or self.condScopeStackStack.hasFunction(funcName):
			return True
		else:
			return False
		
	def getArguments(self, funcName):
		infos = self.condScopeStackStack.getArguments(funcName)
		if infos is None:
			infos = self.scopeStack.getArguments(funcName)
		return infos
	
	def getVarType(self, varName):
		type = self.condScopeStackStack.getVarType(varName)
		if type is None:
			type = self.scopeStack.getVarType(varName)
		return type
	
	def pushType(self, type):
		if self.condScopeStackStack.hasCondScope():
			self.condScopeStackStack.pushType(type)
		else:
			self.scopeStack.pushType(type)
		
	def mergeTypes(self, op=None):
		if self.condScopeStackStack.hasCondScope():
			return self.condScopeStackStack.mergeTypes(op)
		else:
			return self.scopeStack.mergeTypes(op)
	
	def getMergedType(self):
		if self.condScopeStackStack.hasCondScope():
			return self.condScopeStackStack.getMergedType()
		else:
			return self.scopeStack.getMergedType()


#### Basic node class ####
		
class Node:
	count = 0
	type = 'Node (unspecified)'
	shape = 'ellipse'

	nbSynErrors = 0
	nbSemErrors = 0
	checkStack = CheckStack()

	
	def __init__(self,n,children=None):
		self.ID = str(Node.count)
		Node.count+=1
		self.lineNb = n
		self.parent = None
		self.childNum = 0
		if not children: self.children = []
		elif hasattr(children,'__len__'):
			self.children = children
			i = 0
			for child in children:
				child.parent = self
				child.childNum = i
				i += 1
		else:
			self.children = [children]
			children.parent = self
		self.next = []

	def addNext(self,next):
		self.next.append(next)

	def asciitree(self, prefix=''):
		result = "%s%s\n" % (prefix, repr(self))
		prefix += '|  '
		for c in self.children:
			if not isinstance(c,Node):
				result += "%s*** Error: Child of type %r: %r\n" % (prefix,type(c),c)
				continue
			result += c.asciitree(prefix)
		return result
	
	def __str__(self):
		return self.asciitree()
	
	def __repr__(self):
		return self.type
	
	def makegraphicaltree(self, dot=None, edgeLabels=True):
			if not dot: dot = pydot.Dot()
			dot.add_node(pydot.Node(self.ID,label=repr(self), shape=self.shape))
			label = edgeLabels and len(self.children)-1
			for i, c in enumerate(self.children):
				c.makegraphicaltree(dot, edgeLabels)
				edge = pydot.Edge(self.ID,c.ID)
				if label:
					edge.set_label(str(i))
				dot.add_edge(edge)
				#Workaround for a bug in pydot 1.0.2 on Windows:
				#dot.set_graphviz_executables({'dot': r'C:\Program Files\Graphviz2.16\bin\dot.exe'})
			return dot
		
	def threadTree(self, graph, seen = None, col=0):
			colors = ('red', 'green', 'blue', 'yellow', 'magenta', 'cyan')
			if not seen: seen = []
			if self in seen: return
			seen.append(self)
			new = not graph.get_node(self.ID)
			if new:
				graphnode = pydot.Node(self.ID,label=repr(self), shape=self.shape)
				graphnode.set_style('dotted')
				graph.add_node(graphnode)
			label = len(self.next)-1
			for i,c in enumerate(self.next):
				if not c: return
				col = (col + 1) % len(colors)
				color = colors[col]                
				c.threadTree(graph, seen, col)
				edge = pydot.Edge(self.ID,c.ID)
				edge.set_color(color)
				edge.set_arrowsize('.5')
				# The edges corresponding to the "coutures" are not taken into account
				# for the layout of the graph. This permits to keep the tree in his
				# "standard" representation, but may also provoke surprises with the
				# representation of the coutures...
				# By commenting this line, the layout will be quite better, but the
				# tree will be much more difficult to recognize.
				edge.set_constraint('false') 
				if label:
					edge.set_taillabel(str(i))
					edge.set_labelfontcolor(color)
				graph.add_edge(edge)
			return graph    


#### Node types classes ####
			
class ProgramNode(Node):
	type = 'Program'

class TokenNode(Node):
	type = 'token'
	def __init__(self, n, tok):
		Node.__init__(self, n)
		self.tok = tok
		
	def __repr__(self):
		return repr(self.tok)
		
	def getLlvmTok(self):
		return self.tok
	
class OpNode(Node):
	type = 'Operation'
	def __init__(self, n, op, children):
		Node.__init__(self,n,children)
		self.op = op
		try:
			self.nbargs = len(children)
		except AttributeError:
			self.nbargs = 1
		
	def __repr__(self):
		return "%s" % (self.op)

class IdNode(TokenNode):
	type = 'Identifier'
	
	def getLlvmTok(self):
		if self.id_type == 'Integer':
			type = 'I'
		elif self.id_type == 'Double':
			type = 'D'
		elif self.id_type == 'Boolean':
			type = 'B'
		elif self.id_type == 'List Integer':
			type = 'LI'
		elif self.id_type == 'List Double':
			type = 'LD'
		elif self.id_type == 'List Boolean':
			type = 'LB'
		
		return type+self.tok
	
class AssignNode(Node):
	type = 'Assignment'
	
class ConstNode(Node):
	type = 'Constant'

class FuncCallNode(Node):
	type = 'Function call'
	
class ReturnNode(Node):
	type = 'Return'
	
class FuncDefNode(Node):
	type = 'Function Definition'
	
class BodyNode(Node):
	type = 'Body'
	
class HeadNode(Node):
	type = 'Head'
	
class WhileNode(Node):
	type = 'While'
		
class ForNode(Node):
	type = 'For'

class InNode(Node):
	type = 'In'
	
class InRangeNode(Node):
	type = 'In range'

class ConditionnalNode(Node):
	type = 'Conditionnal'
	
class IfNode(Node):
	type = 'If'
	
class ElseifNode(Node):
	type = 'Elseif'
	
class ElseNode(Node):
	type = 'Else'
	
class BreakNode(Node):
	type = 'Break'
	
class ContinueNode(Node):
	type = 'Continue'
	
class TrueNode(Node):
	type = 'True'
	
class FalseNode(Node):
	type = 'False'
	
class ListElementNode(Node):
	type = 'List element'
	# first child will be the ID, second the index (or expression to calculate it)

class ListNode(Node):
	type = 'List'
	
# class StringNode(Node):
	# type = 'String'
	# def __init__(self, n, tok):
		# Node.__init__(self, n)
		# self.tok = tok
	
class AssignVarNode(TokenNode):
	type = 'Assignment variable'
	
	def __repr__(self):
		return repr('assignVar ' + self.tok)
	
	def getLlvmTok(self):
		if self.id_type == 'Integer':
			type = 'I'
		elif self.id_type == 'Double':
			type = 'D'
		elif self.id_type == 'Boolean':
			type = 'B'
		elif self.id_type == 'List Integer':
			type = 'LI'
		elif self.id_type == 'List Double':
			type = 'LD'
		elif self.id_type == 'List Boolean':
			type = 'LB'
		
		return type+self.tok
		
class FuncDefNameNode(TokenNode):
	type = 'Function name'
	def __init__(self, n, tok, t):
		Node.__init__(self, n)
		self.tok = tok
		self.var_type = t

class FuncDefArgNode(TokenNode):
	type = 'Function argument'
	def __init__(self, n, tok, t):
		Node.__init__(self, n)
		self.tok = tok
		self.var_type = t
		self.id_type = t
		
	def __repr__(self):
		return repr(self.var_type + self.tok)
		
	def getLlvmTok(self):
		if self.id_type == 'Integer':
			type = 'I'
		elif self.id_type == 'Double':
			type = 'D'
		elif self.id_type == 'Boolean':
			type = 'B'
		elif self.id_type == 'List Integer':
			type = 'LI'
		elif self.id_type == 'List Double':
			type = 'LD'
		elif self.id_type == 'List Boolean':
			type = 'LB'
		
		return type+self.tok
	
class NumIteratorNode(TokenNode):
	type = 'Numeric iterator'
	
	def getLlvmTok(self):
		return 'I'+self.tok
		
class ListIteratorNode(TokenNode):
	type = 'List iterator'

class IntNode(TokenNode):
	type = 'Integer'

class DoubleNode(TokenNode):
	type = 'Double'
	
class FuncCallNameNode(TokenNode):
	type = 'Function call name'

class DisplayNode(Node):
	type = 'Display'
	
class MinusNode(Node):
	type = '-'

class EntryNode(Node):
	type = 'ENTRY'
	def __init__(self):
		Node.__init__(self, None)
		
class ErrorNode(Node):
	type = 'ERROR'
	def __init__(self):
		Node.__init__(self, None)


#### Decorator ####
		
def addToClass(cls):
	'''Decorator which permits to add the decorated function as a method
	to a class.
	
	This permits to regroup all the methods that have a common goal in the 
	same placed.
	
	Warning: After the utilisation of this decorator, the decorated function 
	remains in the current namespace. If it bother, you can use del to delete it.
	'''
	def decorator(func):
		setattr(cls,func.__name__,func)
		return func
	return decorator