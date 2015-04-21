# coding: latin-1

''' AST.py, version 0.2

Petit module utilitaire pour la construction, la manipulation et la 
repr�sentation d'arbres syntaxiques abstraits.

S�rement plein de bugs et autres surprises. � prendre comme un 
"work in progress"...
Notamment, l'utilisation de pydot pour repr�senter un arbre syntaxique cousu
est une utilisation un peu "limite" de graphviz. �a marche, mais le layout n'est
pas toujours optimal...

2008-2009, Matthieu Amiguet, HE-Arc      !!!!!!MODIFIED VERSION!!!!!
'''

import pydot


class Scope:
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
		if len(self.typeStack) < 2:
			return -1
		
		type1 = self.typeStack.pop()
		type2 = self.typeStack.pop()
		
		if type1 == type2 or type1 == 'unknown':
			self.typeStack.append(type2)
			return True
		elif type2 == 'unknown':
			self.typeStack.append(type1)
			return True
		elif (type1 == 'Double' or type1 == 'Integer' or type1 == 'Boolean') and \
		     (type2 == 'Double' or type2 == 'Integer' or type2 == 'Boolean'):
			self.typeStack.append('Double')
			return True
		else:
			self.typeStack.append('Forbidden')
			return False
	
	def getMergeType(self):
		if len(self.typeStack) > 0:
			return self.typeStack.pop()
		else:
			return 'error'
	

class ScopeStack:
	def __init__(self):
		self.stack = [Scope()]
		self.currentScope = 0
		self.scopeNumber = 1
		
	def newScope(self):
		self.currentScope += 1
		self.scopeNumber += 1
		self.stack.append(Scope())
		# print("new scope")
	
	def pop(self):
		self.stack.pop()
		self.currentScope -= 1
		self.scopeNumber -= 1
		# print("pop scope")
	
	def addVariable(self, varName, type):
		# print(self.currentScope)
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
	
	def getMergeType(self):
		return self.stack[self.currentScope].getMergeType()
	
		
class Node:
	count = 0
	type = 'Node (unspecified)'
	shape = 'ellipse'
	
	scopeStack = ScopeStack()
	nbSemErrors = 0
	
	def __init__(self,children=None):
		self.ID = str(Node.count)
		Node.count+=1
		self.parent = None
		if not children: self.children = []
		elif hasattr(children,'__len__'):
			self.children = children
			for child in children:
				child.parent = self
		else:
			self.children = [children]
			for child in children:
				child.parent = self
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
				# Les arr�tes correspondant aux coutures ne sont pas prises en compte
				# pour le layout du graphe. Ceci permet de garder l'arbre dans sa repr�sentation
				# "standard", mais peut provoquer des surprises pour le trajet parfois un peu
				# tarabiscot� des coutures...
				# En commantant cette ligne, le layout sera bien meilleur, mais l'arbre nettement
				# moins reconnaissable.
				edge.set_constraint('false') 
				if label:
					edge.set_taillabel(str(i))
					edge.set_labelfontcolor(color)
				graph.add_edge(edge)
			return graph    
		
class ProgramNode(Node):
	type = 'Program'

class TokenNode(Node):
	type = 'token'
	def __init__(self, tok):
		Node.__init__(self)
		self.tok = tok
		
	def __repr__(self):
		return repr(self.tok)
	
class OpNode(Node):
	def __init__(self, op, children):
		Node.__init__(self,children)
		self.op = op
		try:
			self.nbargs = len(children)
		except AttributeError:
			self.nbargs = 1
		
	def __repr__(self):
		return "%s" % (self.op)

		
############ ajout	

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
	# def __init__(self, tok, retValue, nline = 0):
		# Node.__init__(self, None, nline)
		# self.tok = tok
		# self.retValue = retValue
		
		# Node.__init__(self, [cond, block], nline)
	
class FuncDefNode(Node):
	type = 'Function Definition'
	
class BodyNode(Node):
	type = 'Body'
	
class HeadNode(Node):
	type = 'Head'
	
class WhileNode(Node):
	type = 'While'
	# def __init__(self, cond, body, nline = 0):
		# self.cond = cond
		# self.body = body
		
		# Node.__init__(self, [cond, body], nline)

		
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
	def __init__(self, tok):
		Node.__init__(self)
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

		
############### fin de l'ajout



	
# class AssignNode(Node):
	# type = '='
	
# class PrintNode(Node):
	# type = 'print'
	
# class WhileNode(Node):
	# type = 'while'
	
class EntryNode(Node):
	type = 'ENTRY'
	def __init__(self):
		Node.__init__(self, None)
	
def addToClass(cls):
	''' D�corateur permettant d'ajouter la fonction d�cor�e en tant que m�thode
	� une classe.
	
	Permet d'impl�menter une forme �l�mentaire de programmation orient�e
	aspects en regroupant les m�thodes de diff�rentes classes impl�mentant
	une m�me fonctionnalit� en un seul endroit.
	
	Attention, apr�s utilisation de ce d�corateur, la fonction d�cor�e reste dans
	le namespace courant. Si cela d�range, on peut utiliser del pour la d�truire.
	Je ne sais pas s'il existe un moyen d'�viter ce ph�nom�ne.
	'''
	def decorator(func):
		setattr(cls,func.__name__,func)
		return func
	return decorator