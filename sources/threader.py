import AST
from AST import * #addToClass

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

@addToClass(AST.Node)	
def semAnalysis(self):
	self.next[0].semAnalysis()

@addToClass(AST.ProgramNode)	
def semAnalysis(self):
	print("Semantic analysis terminated with %d errors" %(self.nbSemErrors))
		
@addToClass(AST.AssignNode)
def semAnalysis(self):
	if isinstance(self.children[0], ListElementNode): 
		AST.Node.scopeStack.addVariable(self.children[0].children[0].tok,'unknown')
	else:
		AST.Node.scopeStack.addVariable(self.children[0].tok,'unknown')
	
	self.next[0].semAnalysis()

@addToClass(AST.TokenNode)
def semAnalysis(self):
	if not AST.Node.scopeStack.hasVariable(self.tok):
		print("error: uninitialized variable '%s'" %(self.tok))
		AST.Node.nbSemErrors += 1
	self.next[0].semAnalysis()

@addToClass(AST.HeadNode)
def semAnalysis(self):
	AST.Node.scopeStack.addFunction(self.children[0].tok, len(self.children)-1)
	AST.Node.scopeStack.newScope()
	for argument in self.children[1:]:
		AST.Node.scopeStack.addVariable(argument.tok,'unknown')
	self.next[0].semAnalysis()
	
@addToClass(FuncCallNameNode)
def semAnalysis(self):
	if not AST.Node.scopeStack.hasFunction(self.tok):
		print("error: undefined function '%s'" %(self.tok))
		AST.Node.nbSemErrors += 1
	self.next[0].semAnalysis()

@addToClass(AST.FuncDefNode)
def semAnalysis(self):
	AST.Node.scopeStack.pop()
	self.next[0].semAnalysis()
	
@addToClass(AST.NumIteratorNode)
def semAnalysis(self):
	AST.Node.scopeStack.addVariable(self.tok,'integer')
	self.next[0].semAnalysis()
	
@addToClass(AST.ListIteratorNode)
def semAnalysis(self):
	AST.Node.scopeStack.addVariable(self.tok,'unknown')
	self.next[0].semAnalysis()
	
@addToClass(AST.ListIteratorNode)
def semAnalysis(self):
	AST.Node.scopeStack.addVariable(self.tok,'unknown')
	self.next[0].semAnalysis()
	
@addToClass(AST.ForNode)
def semAnalysis(self):
	AST.Node.scopeStack.removeVariable(self.children[0].children[0].tok)
	self.next[0].semAnalysis()



@addToClass(AST.ReturnNode)
def semAnalysis(self):
	node = self
	while not isinstance(node.parent, FuncDefNode):
		if node.parent == None:
			print("error: return statement not in a function")
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
		if node.parent == None:
			print("error: break/continue statement not in a loop")
			AST.Node.nbSemErrors += 1
			break
		else:
			node = node.parent
	self.next[0].semAnalysis()
		
	
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
	