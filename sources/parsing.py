import ply.yacc as yacc
from lexical import remove_comments
from lexical import tokens
from lexical import lexer
import AST

precedence = (
    ('left', 'OR', 'AND'),
	('left', 'CEQ', 'CNE', 'CLT', 'CLE', 'CGT', 'CGE'),
	('left', 'ADD_OP', 'SUB_OP') ,
	('left', 'MUL_OP', 'DIV_OP', 'MOD_OP') ,
)

def p_program(p):
	'''program : stmt
			   | stmt program
               | END_STATEMENT stmt program'''
	if len(p) == 2:
		p[0] = AST.ProgramNode([p[1]])
	if len(p) == 3:
		p[0] = AST.ProgramNode([p[1]] + p[2].children)
	if len(p) == 4:
		p[0] = AST.ProgramNode([p[2]] + p[3].children)
		
def p_stmt_type(p):
	'''stmt : simple_stmt
			| compound_stmt'''
	p[0] = p[1]

def p_simple_stmt(p):
	'''simple_stmt : small_stmt END_STATEMENT'''
	p[0] = p[1]

def p_small_stmt(p):
	'''small_stmt : assignment 
				  | const_decl 
				  | expr
			  	  | return_stmt
			  	  | loop_stmt''' # return, break, and continue are not context free, leave to  semantic analysis? 
	p[0] = p[1]
				  
def p_(p):
	'''return_stmt : RETURN
                   | RETURN expr'''			   
	if len(p) == 2:
		p[0] = AST.ReturnNode()
	if len(p) == 3:
		p[0] = AST.ReturnNode([p[2]])

def p_break(p):
	'''loop_stmt : BREAK'''
	p[0] = AST.BreakNode()
	
def p_continue(p):
	'''loop_stmt : CONTINUE'''
	p[0] = AST.ContinueNode()
				  
def p_assign(p):
	'''assignment : IDENTIFIER ASSIGN expr
				  | IDENTIFIER ASSIGN LSBRACKET list_args RSBRACKET
				  | IDENTIFIER LSBRACKET expr RSBRACKET ASSIGN expr'''
	if len(p) == 4:
		p[0] = AST.AssignNode([AST.AssignVarNode(p[1])] + [p[3]])
	if len(p) == 6:
		p[0] = AST.AssignNode([AST.AssignVarNode(p[1]), AST.ListNode(p[4].children)])
	if len(p) == 7:
		p[0] = AST.AssignNode([AST.ListElementNode([AST.AssignVarNode(p[1]), p[3]]), p[6]])
	
def p_const(p):
	'''const_decl : IDENTIFIER CONST expr'''
	p[0] = AST.ConstNode([AST.TokenNode(p[1]), p[3]])

	
def p_func_call(p):
	'''func_call : IDENTIFIER LPAREN list_args RPAREN
                 | IDENTIFIER LPAREN RPAREN'''
	if len(p) == 5:
		p[0] = AST.FuncCallNode([AST.FuncCallNameNode(p[1])] + p[3].children)
	if len(p) == 4:
		p[0] = AST.FuncCallNode([AST.FuncCallNameNode(p[1])])
		
def p_list_args(p):
	'''list_args : expr 
                 | expr COMMA list_args'''				 
	if len(p) == 2:
		p[0] = AST.Node([p[1]])
	if len(p) == 4:
		p[0] = AST.Node([p[1]] + p[3].children)

		
def p_expr_id(p):
	'''expr : IDENTIFIER
	        | IDENTIFIER LSBRACKET expr RSBRACKET'''
	if len(p) == 2:
		p[0] = AST.TokenNode(p[1])
	if len(p) == 5:
		p[0] = AST.ListElementNode([AST.TokenNode(p[1]), p[3]])

def p_expr_string(p):
	'''expr : STRING'''
	p[0] = AST.StringNode(p[1])
		
def p_expr(p):
	'''expr : LPAREN expr RPAREN
			| func_call'''
	if len(p) == 2:
		p[0] = p[1]
	if len(p) == 4:
		p[0] = p[2]

def p_expr_num(p):
	'''expr : INTEGER 
			| DOUBLE'''
	p[0] = AST.NumNode(p[1])

def p_expr_bool(p):
	'''expr : boolean'''
	p[0] = p[1]
	
def p_true(p):
	'''boolean : TRUE'''
	p[0] = AST.TrueNode()

def p_false(p):
	'''boolean : FALSE'''
	p[0] = AST.FalseNode()
	
def p_op(p):
	'''expr : expr ADD_OP expr
            | expr SUB_OP expr
	        | expr MUL_OP expr
			| expr DIV_OP expr
			| expr MOD_OP expr
			| expr comb_op expr
			| expr comp_op expr'''
	p[0] = AST.OpNode(p[2], [p[1], p[3]])
	
def p_comb_op(p):
	'''comb_op : OR 
	           | AND'''
	p[0] = p[1]

def p_comp_op(p):
	'''comp_op : CEQ 
			   | CNE 
			   | CLT 
			   | CLE 
			   | CGT 
			   | CGE'''
	p[0] = p[1]	

def p_compound_stmt(p):
	'''compound_stmt : func_def 
	                 | if_stmt 
	                 | while_stmt 
	                 | for_stmt'''
	p[0] = p[1]	

def p_func_def(p):
	'''func_def : FUNCTION head END_STATEMENT INDENT body DEDENT'''
	p[0] = AST.FuncDefNode([p[2], p[5]])

def p_head(p):
	'''head : IDENTIFIER LPAREN func_def_args RPAREN COLON
			| IDENTIFIER LPAREN RPAREN COLON'''
	if len(p) == 6:
		p[0] = AST.HeadNode([AST.FuncDefNameNode(p[1])] + p[3].children)
	if  len(p) == 5: 
		p[0] = AST.HeadNode([AST.FuncDefNameNode(p[1])])

def p_func_def_args(p):
	'''func_def_args : IDENTIFIER 
                     | IDENTIFIER COMMA func_def_args'''
	if len(p) == 2:
		p[0] = AST.Node([AST.FuncDefArgNode(p[1])])
	if len(p) == 4:
		p[0] = AST.Node([AST.FuncDefArgNode(p[1])] + p[3].children)

def p_body(p):
	'''body : stmt
            | stmt body'''
	if len(p) == 2:
		p[0] = AST.BodyNode([p[1]])
	if len(p) == 3:
		p[0] = AST.BodyNode([p[1]] + p[2].children)

def p_while(p):
	'''while_stmt : WHILE expr COLON END_STATEMENT INDENT body DEDENT''' # What if no body? same issue with func_def, if,... 
	p[0] = AST.WhileNode([p[2], p[6]])
	

def p_for(p):
	'''for_stmt : FOR IDENTIFIER IN RANGE LPAREN expr COMMA expr RPAREN COLON END_STATEMENT INDENT body DEDENT
                | FOR IDENTIFIER IN IDENTIFIER COLON END_STATEMENT INDENT body DEDENT'''
	if len(p) == 15:
		iter = AST.NumIteratorNode(p[2])
		lowLim = p[6]
		highLim = p[8]
		p[0] = AST.ForNode([AST.InRangeNode([iter, lowLim, highLim]), p[13]])
	if len(p) == 10:
		p[0] = AST.ForNode([AST.InNode([AST.ListIteratorNode(p[2]), AST.TokenNode(p[4])]), p[8]])
		

def p_if(p):
	'''if_stmt : IF expr COLON END_STATEMENT INDENT body DEDENT
			   | IF expr COLON END_STATEMENT INDENT body DEDENT elseif_list
			   | IF expr COLON END_STATEMENT INDENT body DEDENT elseif_list ELSE COLON END_STATEMENT INDENT body DEDENT
               | IF expr COLON END_STATEMENT INDENT body DEDENT ELSE COLON END_STATEMENT INDENT body DEDENT'''
	if len(p) == 8:
		p[0] = AST.ConditionnalNode([AST.IfNode([p[2], p[6]])])
	if len(p) == 9:
		p[0] = AST.ConditionnalNode([AST.IfNode([p[2], p[6]])] + p[8].children)
	if len(p) == 15:
		p[0] = AST.ConditionnalNode([AST.IfNode([p[2], p[6]])] + p[8].children + [AST.ElseNode([p[13]])])
	if len(p) == 14:
		p[0] = AST.ConditionnalNode([AST.IfNode([p[2], p[6]]), AST.ElseNode([p[12]])])

def p_elseif(p):
	'''elseif_list : ELSEIF expr COLON END_STATEMENT INDENT body DEDENT
                   | ELSEIF expr COLON END_STATEMENT INDENT body DEDENT elseif_list'''
	if len(p) == 8:
		p[0] = AST.Node([AST.ElseifNode([p[2], p[6]])])
	if len(p) == 9:
		p[0] = AST.Node([AST.ElseifNode([p[2], p[6]])] + p[9].children)

# def p_error(p):
	
	# if p:
		# print("Syntax error in line %d" % p.lineno)	
		# yacc.errok()
	# else:
		# print("Syntax error: NEWLINE missing at last statement")

def p_error(p):
    global flag_for_error
    flag_for_error = 1

    if p is not None:
		print("Syntax error in line %d" % p.lineno)
		yacc.errok()
    else:
        print("Unexpected end of input")
		

yacc.yacc(outputdir='generated')


def parse(program):
	prog = remove_comments(program)
	return yacc.yacc().parse(prog, lexer)

############################
	
if __name__ == "__main__":

	import sys
	prog = remove_comments(open(sys.argv[1]).read())
	result = yacc.yacc().parse(prog, lexer)
	#print(result)
	import os
	try:
		graph = result.makegraphicaltree()
		name = os.path.splitext(sys.argv[1])[0]+"-ast.pdf"
		graph.write_pdf(name)
		print("wrote ast to" , name)
	except (AttributeError, TypeError) as e:
		print("Unable to build an AST because of the syntax errors")
