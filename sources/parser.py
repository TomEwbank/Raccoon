import ply.yacc as yacc
#import Lexer
import AST
import os

from lexical import tokens

precedence = (
	('left', 'ADD_OP', 'SUB_OP') ,
	('left', 'MUL_OP', 'DIV_OP', 'MOD_OP') ,
)


def p_program(p):
	'''program : stmt
               | stmt program'''
	if len(p) == 2:
		p[0] = AST.ProgramNode([p[1]])
	if len(p) == 3:
		p[0] = AST.ProgramNode([p[1]] + p[2].children)
		
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
		   	      | func_call
			  	  | return_stmt
			  	  | loop_stmt''' # return, break, and continue are not context free, leave to  semantic analysis? 
	p[0] = p[1]
				  
def p_(p):
	'''return_stmt : RETURN
                   | RETURN expr
                   | RETURN boolean'''			   
	if len(p) == 2:
		p[0] = AST.ReturnNode([])
	if len(p) == 3:
		p[0] = AST.ReturnNode([p[2]])

def p_loop_stmt(p):
	'''loop_stmt : BREAK 
	| CONTINUE'''
	p[0] = AST.TokenNode(p[1])
				  
def p_assign(p):
	'''assignment : IDENTIFIER ASSIGN expr
				  | IDENTIFIER ASSIGN boolean
			      | ARRAY_CELL ASSIGN expr
			      | ARRAY_CELL ASSIGN boolean'''
	p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])

def p_const(p):
	'''const_decl : IDENTIFIER CONST expr'''
	p[0] = AST.ConstNode([AST.TokenNode(p[1]), p[3]])

def p_func_call(p):
	'''func_call : IDENTIFIER LPAREN call_args RPAREN
                 | IDENTIFIER LPAREN RPAREN'''
	if len(p) == 5:
		p[0] = AST.FuncCallNode([AST.TokenNode(p[1])] + p[3].children)
	if len(p) == 4:
		p[0] = AST.FuncCallNode([AST.TokenNode(p[1])])
		
def p_call_args(p):
	'''call_args : arg 
                 | arg COMMA call_args'''				 
	if len(p) == 2:
		p[0] = p[1]
	if len(p) == 4:
		p[0] = AST.Node([p[1]] + p[3].children)

def p_arg(p):
	'''arg : expr
           | boolean'''
	p[0] = p[1]

def p_expr_id(p):
	'''expr : IDENTIFIER
			| ARRAY_CELL'''
	p[0] = AST.TokenNode(p[1])
	
def p_expr(p):
	'''expr : func_call
			| arithmetic
			| LPAREN expr RPAREN'''
	if len(p) == 2:
		p[0] = p[1]
	if len(p) == 4:
		p[0] = p[2]

def p_expr_num(p):
	'''expr : INTEGER 
			| DOUBLE'''
	p[0] = AST.TokenNode(p[1])

def p_bool(p):
	'''boolean : TRUE 
	| FALSE'''
	p[0] = AST.TokenNode(p[1])

def p_arithmetic(p):
	'''arithmetic : expr ADD_OP expr
                  | expr SUB_OP expr
	           	  | expr MUL_OP expr
				  | expr DIV_OP expr
			      | expr MOD_OP expr'''
	p[0] = AST.OpNode(p[2], [p[1], p[2]])
	


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
	'''func_def : head END_STATEMENT body END'''
	p[0] = AST.FuncDefNode([p[1], p[3]])

def p_head(p):
	'''head : FUNCTION IDENTIFIER LPAREN p_func_def_args RPAREN COLON
			| FUNCTION IDENTIFIER LPAREN RPAREN COLON'''
	if len(p) == 6:
		p[0] = AST.HeadNode([AST.TokenNode(p[2])] + p[4].children)
	if  len(p) == 5: 
		p[0] = AST.HeadNode([AST.TokenNode(p[2])])

def p_func_def_args(p):
	'''p_func_def_args : IDENTIFIER 
                       | IDENTIFIER COMMA p_func_def_args'''
	if len(p) == 2:
		p[0] = AST.TokenNode(p[1])
	if len(p) == 4:
		p[0] = AST.Node([AST.TokenNode(p[1])] + p[3].children)

def p_body(p):
	'''body : stmt
            | stmt body'''
	if len(p) == 2:
		p[0] = p[1]
	if len(p) == 3:
		p[0] = AST.BodyNode([p[1]] + p[2].children)

def p_while(p):
	'''while_stmt : WHILE cond_list COLON END_STATEMENT body END''' # What if no body? same issue with func_def, if,... 
	p[0] = AST.WhileNode([p[2], p[5]])
	
def p_cond_list(p):
	'''cond_list : condition
                 | condition comb_op cond_list'''
	if len(p) == 2:
		p[0] = p[1]
	if len(p) ==  4:
		p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_cond_list_paren(p):
	'''cond_list : LPAREN cond_list RPAREN'''
	p[0] = p[2]
	
def p_cond(p):
	'''condition : expr comp_op expr
			     | boolean'''
	if len(p) == 4:
		p[0] = AST.OpNode(p[2], [p[1], p[3]])
	if len(p) == 2:
		p[0] = p[1]

def p_for(p):
	'''for_stmt : FOR IDENTIFIER IN RANGE LPAREN INTEGER COMMA INTEGER RPAREN COLON END_STATEMENT body END
                | FOR IDENTIFIER IN IDENTIFIER COLON END_STATEMENT body END'''
	if len(p) == 14:
		iter = AST.TokenNode(p[2])
		lowLim = AST.TokenNode(p[6])
		highLim = AST.TokenNode(p[8])
		p[0] = AST.ForNode([AST.InRangeNode([iter, lowLim, highLim]), p[12]])
	if len(p) == 9:
		p[0] = AST.ForNode([AST.InNode([AST.TokenNode(p[2]), AST.TokenNode(p[4])]), p[7]])
		

def p_if(p):
	'''if_stmt : IF cond_list COLON END_STATEMENT body END
			   | IF cond_list COLON END_STATEMENT body END elseif_list
			   | IF cond_list COLON END_STATEMENT body END elseif_list ELSE COLON END_STATEMENT body END
               | IF cond_list COLON END_STATEMENT body END ELSE COLON END_STATEMENT body END'''
	if len(p) == 7:
		p[0] = AST.ConditionnalNode([AST.IfNode([p[2], p[5]])])
	if len(p) == 8:
		p[0] = AST.ConditionnalNode([AST.IfNode([p[2], p[5]])] + p[7].children)
	if len(p) == 12:
		p[0] = AST.ConditionnalNode([AST.IfNode([p[2], p[5]])] + p[7].children + [AST.ElseNode([p[10]])])
	if len(p) == 11:
		p[0] = AST.ConditionnalNode([AST.IfNode([p[2], p[5]]), AST.ElseNode([p[10]])])

def p_elseif(p):
	'''elseif_list : ELSEIF cond_list COLON END_STATEMENT body END
                   | ELSEIF cond_list COLON END_STATEMENT body END elseif_list'''
	if len(p) == 7:
		p[0] = AST.Node([AST.ElseifNode([p[2], p[5]])])
	if len(p) == 8:
		p[0] = AST.Node([AST.ElseifNode([p[2], p[5]])] + p[7].children)

def p_error(p):
	
	if p:
		print("Syntax error in line")	
		yacc.errok()
	else:
		print("Syntax error: NEWLINE missing at last statement")

		

yacc.yacc(outputdir='generated')

if __name__ == "__main__":

	import sys
	try:
		prog = file(sys.argv[1]).read()
		result = yacc.parse(prog)
		print(result)
		import os
		graph = result.makegraphicaltree()
		name = os.path.splitext(sys.argv[1])[0]+"-ast.pdf"
		graph.write_pdf(name)
		print("wrote ast to" , name)
	except (AttributeError, TypeError) as e:
		print("Unable to build an AST because of the syntax errors")
