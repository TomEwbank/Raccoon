import AST
from AST import addToClass

##### adding functions for the "couture" of the AST ####

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

##### adding functions for the semantic analysis ####
	
def semAnalysis(self):
	if len(self.next) > 0
		self.next[0].semAnalysis()
		
@addToClass(AST.AssignNode):
def semAnalysis(self):
	Node.scopeStack.addVariable(self.children[0].tok,'unknown')
	self.next.semAnalysis()

@addToClass(AST.TokenNode):
def semAnalysis(self):
	if not Node.scopeStack.hasVariable(self.tok):
		print("error: uninitialized variable ", self.tok)
	self.next.semAnalysis()

@addToClass(AST.HeadNode):
def semAnalysis(self):
	Node.scopeStack.addFunction(self.children[0].tok, len(self.children)-1)
	Node.scopeStack.newScope
	for argument in self.children[1:]:
		Node.scopeStack.addVariable(argument.tok,'unknown')
	self.next.semAnalysis()

@addToClass(AST.FuncDefNode):
def semAnalysis(self):
	Node.scopeStack.pop()
	self.next.semAnalysis()
	
@addToClass(AST.NumIteratorNode):
def semAnalysis(self):
	Node.scopeStack.addVariable(self.tok,'integer')
	self.next.semAnalysis()
	
@addToClass(AST.ListIteratorNode):
def semAnalysis(self):
	Node.scopeStack.addVariable(self.tok,'unknown')
	self.next.semAnalysis()
	
@addToClass(AST.ListIteratorNode):
def semAnalysis(self):
	Node.scopeStack.addVariable(self.tok,'unknown')
	self.next.semAnalysis()
	
@addToClass(AST.ForNode):
def semAnalysis(self):
	Node.scopeStack.removeVariable(self.children[0].children[0].tok)
	self.next.semAnalysis()
	
@addToClass(AST.ReturnNode):
def semAnalysis(self):
	node = self
	while not isinstance(node.parent, FuncDefNode):
		if self.parent == None:
			print("error: return statement not in a function")
			break
		else:
			node = self.parent
	self.next.semAnalysis()
	
@addToClass(AST.BreakNode):
@addToClass(AST.ContinueNode):
def semAnalysis(self):
	node = self
	while not isinstance(node.parent, ForNode) and not isinstance(node.parent, WhileNode):
		if self.parent == None:
			print("error: break/continue statement not in a loop")
			break
		else:
			node = self.parent
	self.next.semAnalysis()
		
	
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
	
	