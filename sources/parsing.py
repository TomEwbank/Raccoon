#############################################################################################
#  parsing.py,																				#
#																							#
# Parser for the Raccoon language, using PLY.												#
#																							#
# May 2015, CATUSANU Paul, EWBANK Tom and VAN DE GOOR Elodie.								#
#############################################################################################

import ply.yacc as yacc
from lexical import remove_comments
from lexical import tokens
from lexical import lexer
from lexical import NestComError
import AST

precedence = (
    ('left', 'OR', 'AND'),
	('left', 'CEQ', 'CNE', 'CLT', 'CLE', 'CGT', 'CGE'),
	('left', 'ADD_OP', 'SUB_OP') ,
	('left', 'MUL_OP', 'DIV_OP', 'MOD_OP'),
	('right','MINUS'),
)

def p_program(p):
	'''program : func_def
			   | func_def program'''
	if len(p) == 2:
		p[0] = AST.ProgramNode(p.lineno(1), [p[1]])
	if len(p) == 3:
		p[0] = AST.ProgramNode(p.lineno(1), [p[1]] + p[2].children)
		
def p_program2(p):
	'''program : END_STATEMENT program'''
	p[0] = p[2]
		
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
				  | display
			  	  | loop_stmt'''
	p[0] = p[1]

def p_return(p):
	'''return_stmt : RETURN
                   | RETURN expr'''			   
	if len(p) == 2:
		p[0] = AST.ReturnNode(p.lineno(1))
	if len(p) == 3:
		p[0] = AST.ReturnNode(p.lineno(1), [p[2]])

def p_break(p):
	'''loop_stmt : BREAK'''
	p[0] = AST.BreakNode(p.lineno(1))
	
def p_continue(p):
	'''loop_stmt : CONTINUE'''
	p[0] = AST.ContinueNode(p.lineno(1))
	
def p_display(p):
	'''display : DISPLAY LPAREN IDENTIFIER RPAREN'''
	p[0] = AST.DisplayNode(p.lineno(1), [AST.IdNode(p.lineno(1), p[3])])
				  

def p_assign(p):
	'''assignment : IDENTIFIER ASSIGN expr
				  | IDENTIFIER ASSIGN LSBRACKET list_args RSBRACKET
				  | IDENTIFIER LSBRACKET expr RSBRACKET ASSIGN expr'''
	if len(p) == 4:
		p[0] = AST.AssignNode(p.lineno(2), [AST.AssignVarNode(p.lineno(1), p[1])] + [p[3]])
	if len(p) == 6:
		p[0] = AST.AssignNode(p.lineno(2), [AST.AssignVarNode(p.lineno(1), p[1]), AST.ListNode(p.lineno(1), p[4].children)])
	if len(p) == 7:
		p[0] = AST.AssignNode(p.lineno(5), [AST.ListElementNode(p.lineno(1), [AST.AssignVarNode(p.lineno(1), p[1]), p[3]]), p[6]])

def p_const(p):
	'''const_decl : IDENTIFIER CONST expr
				  | IDENTIFIER CONST LSBRACKET list_args RSBRACKET'''
	if len(p) == 4:
		p[0] = AST.ConstNode(p.lineno(2), [AST.AssignVarNode(p.lineno(1), p[1]), p[3]])
	if len(p) == 6:
		p[0] = AST.ConstNode(p.lineno(2), [AST.AssignVarNode(p.lineno(1), p[1]), AST.ListNode(p.lineno(1), p[4].children)])

	
def p_func_call(p):
	'''func_call : IDENTIFIER LPAREN list_args RPAREN
                 | IDENTIFIER LPAREN RPAREN'''
	if len(p) == 5:
		p[0] = AST.FuncCallNode(p.lineno(1), [AST.FuncCallNameNode(p.lineno(1), p[1])] + p[3].children)
	if len(p) == 4:
		p[0] = AST.FuncCallNode(p.lineno(1), [AST.FuncCallNameNode(p.lineno(1), p[1])])
		
def p_list_args(p):
	'''list_args : expr 
                 | expr COMMA list_args'''				 
	if len(p) == 2:
		p[0] = AST.Node(p.lineno(1), [p[1]])
	if len(p) == 4:
		p[0] = AST.Node(p.lineno(1), [p[1]] + p[3].children)

		
def p_expr_id(p):
	'''expr : IDENTIFIER
	        | IDENTIFIER LSBRACKET expr RSBRACKET'''
	if len(p) == 2:
		p[0] = AST.IdNode(p.lineno(1), p[1])
	if len(p) == 5:
		p[0] = AST.ListElementNode(p.lineno(1), [AST.IdNode(p.lineno(1), p[1]), p[3]])

# def p_expr_string(p):
	# '''expr : STRING'''
	# p[0] = AST.StringNode(p.lineno(1), p[1])
		
def p_expr(p):
	'''expr : LPAREN expr RPAREN
			| func_call'''
	if len(p) == 2:
		p[0] = p[1]
	if len(p) == 4:
		p[0] = p[2]

def p_expr_int(p):
	'''expr : INTEGER'''
	p[0] = AST.IntNode(p.lineno(1), p[1])

def p_expr_double(p):
	'''expr : DOUBLE'''
	p[0] = AST.DoubleNode(p.lineno(1), p[1])
	
def p_expr_bool(p):
	'''expr : boolean'''
	p[0] = p[1]
	
def p_true(p):
	'''boolean : TRUE'''
	p[0] = AST.TrueNode(p.lineno(1))

def p_false(p):
	'''boolean : FALSE'''
	p[0] = AST.FalseNode(p.lineno(1))
	
def p_op(p):
	'''expr : expr ADD_OP expr
			| expr SUB_OP expr
			| expr MUL_OP expr
			| expr DIV_OP expr
			| expr MOD_OP expr
			| expr OR expr
			| expr AND expr
			| expr CEQ expr
			| expr CNE expr
			| expr CLT expr
			| expr CLE expr
			| expr CGT expr
			| expr CGE expr'''
	p[0] = AST.OpNode(p.lineno(2), p[2], [p[1], p[3]])
	
def p_expr_signed(p):
	'''expr : SUB_OP expr %prec MINUS'''
	p[0] =  AST.MinusNode(p.lineno(1), [p[2]])

def p_compound_stmt(p):
	'''compound_stmt : func_def 
	                 | if_stmt 
	                 | while_stmt 
	                 | for_stmt'''
	p[0] = p[1]	

def p_func_def(p):
	'''func_def : FUNCTION head END_STATEMENT INDENT body DEDENT'''
	p[0] = AST.FuncDefNode(p.lineno(1), [p[2], p[5]])

def p_head_void(p):
	'''head : IDENTIFIER LPAREN func_def_args RPAREN COLON
			| IDENTIFIER LPAREN RPAREN COLON'''
	if len(p) == 6:
		p[0] = AST.HeadNode(p.lineno(1), [AST.FuncDefNameNode(p.lineno(1), p[1], 'Void')] + p[3].children)
	if  len(p) == 5: 
		p[0] = AST.HeadNode(p.lineno(1), [AST.FuncDefNameNode(p.lineno(1), p[1], 'Void')])
		
def p_head_int(p):
	'''head : IDENTIFIER LPAREN func_def_args RPAREN RETURN T_INT COLON
			| IDENTIFIER LPAREN RPAREN RETURN T_INT COLON'''
	if len(p) == 8:
		p[0] = AST.HeadNode(p.lineno(1), [AST.FuncDefNameNode(p.lineno(1), p[1], 'Integer')] + p[3].children)
	if  len(p) == 7: 
		p[0] = AST.HeadNode(p.lineno(1), [AST.FuncDefNameNode(p.lineno(1), p[1], 'Integer')])
		
def p_head_double(p):
	'''head : IDENTIFIER LPAREN func_def_args RPAREN RETURN T_DOUBLE COLON
			| IDENTIFIER LPAREN RPAREN RETURN T_DOUBLE COLON'''
	if len(p) == 8:
		p[0] = AST.HeadNode(p.lineno(1), [AST.FuncDefNameNode(p.lineno(1), p[1], 'Double')] + p[3].children)
	if  len(p) == 7: 
		p[0] = AST.HeadNode(p.lineno(1), [AST.FuncDefNameNode(p.lineno(1), p[1], 'Double')])

def p_head_bool(p):
	'''head : IDENTIFIER LPAREN func_def_args RPAREN RETURN T_BOOL COLON
			| IDENTIFIER LPAREN RPAREN RETURN T_BOOL COLON'''
	if len(p) == 8:
		p[0] = AST.HeadNode(p.lineno(1), [AST.FuncDefNameNode(p.lineno(1), p[1], 'Boolean')] + p[3].children)
	if  len(p) == 7: 
		p[0] = AST.HeadNode(p.lineno(1), [AST.FuncDefNameNode(p.lineno(1), p[1], 'Boolean')])

def p_func_def_args(p):
	'''func_def_args : argument 
                     | argument COMMA func_def_args'''
	if len(p) == 2:
		p[0] = AST.Node(p.lineno(1), [p[1]])
	if len(p) == 4:
		p[0] = AST.Node(p.lineno(1), [p[1]] + p[3].children)

def p_func_def_arg_int(p):
	'''argument : T_INT IDENTIFIER'''
	p[0] = AST.FuncDefArgNode(p.lineno(1), p[2], 'Integer')
	
def p_func_def_arg_double(p):
	'''argument : T_DOUBLE IDENTIFIER'''
	p[0] = AST.FuncDefArgNode(p.lineno(1), p[2], 'Double')
	
def p_func_def_arg_bool(p):
	'''argument : T_BOOL IDENTIFIER'''
	p[0] = AST.FuncDefArgNode(p.lineno(1), p[2], 'Boolean')
	
def p_func_def_arg_list_int(p):
	'''argument : T_LIST_INT IDENTIFIER'''
	p[0] = AST.FuncDefArgNode(p.lineno(1), p[2], 'List Integer')

def p_func_def_arg_list_double(p):
	'''argument : T_LIST_DOUBLE IDENTIFIER'''
	p[0] = AST.FuncDefArgNode(p.lineno(1), p[2], 'List Double')

def p_func_def_arg_list_bool(p):
	'''argument : T_LIST_BOOL IDENTIFIER'''
	p[0] = AST.FuncDefArgNode(p.lineno(1), p[2], 'List Boolean')
	
# def p_func_def_arg_list_string(p):
	# '''argument : T_LIST_STRING IDENTIFIER'''
	# p[0] = AST.FuncDefArgNode(p.lineno(1), p[2], 'List String')

# def p_func_def_arg_string(p):
	# '''argument : T_STRING IDENTIFIER'''
	# p[0] = AST.FuncDefArgNode(p.lineno(1), p[2], 'String')

def p_body(p):
	'''body : stmt
            | stmt body'''
	if len(p) == 2:
		p[0] = AST.BodyNode(p.lineno(1), [p[1]])
	if len(p) == 3:
		p[0] = AST.BodyNode(p.lineno(1), [p[1]] + p[2].children)

def p_while(p):
	'''while_stmt : WHILE expr COLON END_STATEMENT INDENT body DEDENT'''
	p[0] = AST.WhileNode(p.lineno(1), [p[2], p[6]])
	

def p_for(p):
	'''for_stmt : FOR IDENTIFIER IN RANGE LPAREN expr COMMA expr RPAREN COLON END_STATEMENT INDENT body DEDENT
                | FOR IDENTIFIER IN IDENTIFIER COLON END_STATEMENT INDENT body DEDENT'''
	if len(p) == 15:
		iter = AST.NumIteratorNode(p.lineno(1), p[2])
		lowLim = p[6]
		highLim = p[8]
		p[0] = AST.ForNode(p.lineno(1), [AST.InRangeNode(p.lineno(1), [iter, lowLim, highLim]), p[13]])
	if len(p) == 10:
		p[0] = AST.ForNode(p.lineno(1), [AST.InNode(p.lineno(1), [AST.ListIteratorNode(p.lineno(1), p[2]), AST.IdNode(p.lineno(1), p[4])]), p[8]])
		

def p_if(p):
	'''if_stmt : IF expr COLON END_STATEMENT INDENT body DEDENT
               | IF expr COLON END_STATEMENT INDENT body DEDENT ELSE COLON END_STATEMENT INDENT body DEDENT'''
	if len(p) == 8:
		p[0] = AST.ConditionnalNode(p.lineno(1), [AST.IfNode(p.lineno(1), [p[2], p[6]])])
	if len(p) == 14:
		p[0] = AST.ConditionnalNode(p.lineno(1), [AST.IfNode(p.lineno(1), [p[2], p[6]]), AST.ElseNode(p.lineno(8), [p[12]])])

def p_error(p):
	# this is a panic mode error handling, not very handy but really easy to implement
    AST.Node.nbSynErrors += 1

    if p is not None:
		print("Syntax error in line %d" % p.lineno)
		while True:
			tok = yacc.token()  # Get the next token
			if not tok or tok.type == 'END_STATEMENT': 
				break
		yacc.restart()
    else:
        print("Syntax error at end of file")


def parse(program):
	prog = remove_comments(program+"\n")
	return yacc.yacc().parse(prog, lexer)

#####################################################
	
if __name__ == "__main__":
	try:
		import sys
		prog = open(sys.argv[1]).read() + "\n"
		prog = remove_comments(prog)
		result = yacc.yacc().parse(prog, lexer)
		
		import os
		import lexical
		
		if AST.Node.nbSynErrors == 0 and lexical.nbLexErrors == 0 and \
		   len(sys.argv) == 3 and sys.argv[2] == "-ast":
			try:
				graph = result.makegraphicaltree()
				name = os.path.splitext(sys.argv[1])[0]+"-ast.pdf"
				graph.write_pdf(name)
				print("wrote ast to '%s'" %name)
			except (AttributeError, TypeError) as e:
				print("Unable to print the AST")
		
		print("Lexical analysis terminated with %d errors" %(lexical.nbLexErrors))
		print("Syntactic analysis terminated with %d errors" %(AST.Node.nbSynErrors))
	except NestComError, e:
		print("error:")
		print(e.msg)