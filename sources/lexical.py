# coding: latin-1
import ply.lex as lex
import sys

tokens = [
	'ADD_OP' ,
	'SUB_OP',
	'MUL_OP',
	'DIV_OP',
	
	'CEQ',
	'CNE',
	'CLT',
	'CLE',
	'CGT',
	'CGE',
	
	'IDENTIFIER',
	'DOUBLE',
	'INTEGER',
	
	'COMMA',
	'COLON',
	'LPAREN',
	'RPAREN',
	'QUOTE',
	'APOSTROPHE',
	'LSBRACKET',
	'RSBRACKET',
	
	'END_STATEMENT',
	'STRING',
	
	'ELSEIF',
	'MOD_OP',
]

reserved = {

	'or':'OR',
	'and':'AND',
	'return' : 'RETURN',
	
	'break' : 'BREAK',
	'continue' : 'CONTINUE',
	'False':'FALSE',
	'True':'TRUE',
	'if' :  'IF',
	'else' : 'ELSE',
	'while' : 'WHILE',
	'range' : 'RANGE',
	'for' : 'FOR',
	'in' : 'IN',
	'becomes':'ASSIGN',
	'is':'CONST',
<<<<<<< HEAD
=======
	'elseif' : 'ELSEIF',
>>>>>>> 930610a92bbef8c0996cf9842b9c7e8dde1a0a11
	'function' :  'FUNCTION',
	'end' : 'END',

}

tokens += list(reserved.values())


t_ADD_OP= r'\+'
t_SUB_OP= r'-'
t_MUL_OP= r'\*'
t_DIV_OP= r'/'
t_CEQ=r'=\?'
t_CNE=r'!='
t_CLT=r'<'
t_CLE=r'<='
t_CGT=r'>'
t_CGE=r'>='

t_LPAREN= r'\('
t_RPAREN= r'\)'
t_COMMA= r','
t_COLON= r':'

t_QUOTE=r'\"'
t_APOSTROPHE=r'\''
t_LSBRACKET=r'\['
t_RSBRACKET=r'\]'


def t_STRING(t):
	r'".*"'
	return t

def t_ELSEIF(t):
	r'else\ if'
	return t

def t_MOD_OP(t):
	r'[ ]*mod[ ]*'
	return t
	
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    
    return t


def t_DOUBLE(t):
	r'\d+\.\d*'
	t.value = float(t.value)
	return t


def t_INTEGER(t):
	r'\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print("Integer value too large %d", t.value)
		t.value = 0
	return t

def t_END_STATEMENT(t):
	r'(\n[ \t]*)+'
	t.value=t.value.count('\n')*'\n'
	t.lexer.lineno += len(t.value)
	return t
 
def t_SIMPLE_COMMENTS(t):
	r'//.*'

def t_BLOCK_COMMENTS(t):
	r'/\*(\n|.)*?(\*/)'
	t.value=t.value.count('\n')*'\n'
	t_END_STATEMENT(t)




def t_error(t) :
	print("Illegal character '%s'" %t.value[0])
	t.lexer.skip(1)


t_ignore = ' \t'

lexer = lex.lex()


if __name__ == "__main__":
	prog = open(sys.argv[1]).read()
	lexer.input(prog)
	while 1 :
		tok = lexer.token()
		if not tok: 
			break
		if (tok.type=='END_STATEMENT'):
			print("end statement line %d\n" %(tok.lineno))
		else:
			print("line %d: %s(%s)" %(tok.lineno, tok.type, tok.value))

