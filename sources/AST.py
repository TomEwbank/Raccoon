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

class Scope:
	'''Class which goal is to keep track of variables 
	   initialization, function definitions, and types of 
	   expressions inside a particular scope of a Raccoon 
	   program.'''

	def __init__(self):
		self.typeStack = []
		self.varHash = {}
		self.funcHash = {}
	
	def addVariable(self, varName, type):
		self.varHash[varName] = type
	
	def hasVariable(self, varName):
		return self.varHash.has_key(varName)
	
	def addFunction(self, funcName, nbArgs):
		self.funcHash[funcName] = nbArgs
	
	def hasFunction(self, funcName):
		return self.funcHash.has_key(funcName)
		
	def removeVariable(self, varName):
		self.varHash.pop(varName, 0)
		
	def getArgNumber(self, funcName):
		return self.funcHash[funcName]
		
	def getVarType(self, varName):
		return self.varHash[varName]
	
	def pushType(self, type):
		self.typeStack.append(type)
		
	def mergeTypes(self):
		'''Compare the last 2 types that has been pushed on
		   the stack, and merge them into one if they are compatible'''
		  
		if len(self.typeStack) < 2:
			return -1
		
		type1 = self.typeStack.pop()
		type2 = self.typeStack.pop()
		
		if type1 == 'String' or type1 == 'List' or \
		   type2 == 'String' or type2 == 'List':
			# Raccoon can't deal with arithmetic/combinatory operation on lists and strings
			self.typeStack.append('Forbidden')
			return False
		elif type1 == type2 or type1 == 'unknown':
			self.typeStack.append(type2)
			return True
		elif type2 == 'unknown':
			self.typeStack.append(type1)
			return True
		else: 
			# The merging of 2 different numeric types leads to the type Double
			# (Booleans are considered as numeric types: True = 1, False = 0)
			self.typeStack.append('Double')
			return True
	
	def getMergedType(self):
		'''Return the type at the top of the stack,
		   which is supposed to be the type of the last
		   encountered expression'''
		   
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
	
	def addFunction(self, funcName, nbArgs):
		self.stack[self.currentScope].addFunction(funcName, nbArgs)
	
	def hasFunction(self, funcName):
		for scope in self.stack:
			if scope.hasFunction(funcName):
				return True
							
		return False
		
	def getArgNumber(self, funcName):
		for scope in self.stack:
			if scope.hasFunction(funcName):
				return scope.getArgNumber(funcName)
							
		return -1
	
	def getVarType(self, varName):
		return self.stack[self.currentScope].getVarType(varName)
	
	def pushType(self, type):
		self.stack[self.currentScope].pushType(type)
		
	def mergeTypes(self):
		return self.stack[self.currentScope].mergeTypes()
	
	def getMergedType(self):
		return self.stack[self.currentScope].getMergedType()

#### Basic node class ####
		
class Node:
	count = 0
	type = 'Node (unspecified)'
	shape = 'ellipse'

	nbSynErrors = 0
	nbSemErrors = 0
	scopeStack = ScopeStack()
	
	def __init__(self,n,children=None):
		self.ID = str(Node.count)
		Node.count+=1
		self.lineNb = n
		self.parent = None
		if not children: self.children = []
		elif hasattr(children,'__len__'):
			self.children = children
			for child in children:
				child.parent = self
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
	
class StringNode(Node):
	type = 'String'
	def __init__(self, n, tok):
		Node.__init__(self, n)
		self.tok = tok
	
class AssignVarNode(TokenNode):
	type = 'Assignment variable'
		
class FuncDefNameNode(TokenNode):
	type = 'Function name'

class FuncDefArgNode(TokenNode):
	type = 'Function argument'
		
class NumIteratorNode(TokenNode):
	type = 'Numeric iterator'
		
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