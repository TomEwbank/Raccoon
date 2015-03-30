# coding: latin-1
import ply.lex as lex
import sys

tokens = [
	'IDENTIFIER',
	'INTEGER',
	'DOUBLE',
	'PLUS' ,
	'MINUS',
	'MUL',
	'DIV',
	'LPAREN',
	'RPAREN',
	'CEQ',
	'CNE',
	'CLT',
	'CLE',
	'CGT',
	'CGE',
	'COMMA',
	'COLON',
	'NEWLINE',
]

reserved = {
	'function' :  'FUN',
	'if' :  'IF',
	'else' : 'ELSE',
	'while' : 'WHILE',
	'continue' : 'CONT',
	'break' : 'BREAK',
	'range' : 'RANGE',
	'for' : 'FOR',
	'in' : 'IN',
	'return' : 'RET',
	'else if' : 'EIF',
	'mod':'MOD',
	'or':'OR',
	'and':'AND',
	'becomes':'ASSIGN',
	'is':'CONST',
	'False':'FALSE',
	'True':'TRUE',
}

#tokens += reserved.values()
tokens += list(reserved.values())

#def t_IDENTIFIER(t):
#	r'[a-zA-Z_][a-zA-Z0-9_]*'
#	if t.value.upper() in tokens:
#		t.type = t.value.upper()
#	return t
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t

t_PLUS= r'\+'
t_MINUS= r'-'
t_MUL= r'\*'
t_DIV= r'/'
t_LPAREN= r'\('
t_RPAREN= r'\)'
t_CEQ=r'=\?'
t_CNE=r'!='
t_CLT=r'<'
t_CLE=r'<='
t_CGT=r'>'
t_CGE=r'>='
t_COMMA= r','
t_COLON= r':'



def t_DOUBLE(t):
	r'-?[0-9]+\.[0-9]*'
	t.value = float(t.value)
	return t


def t_INTEGER(t):
	r'-?\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print("Integer value too large %d", t.value)
		t.value = 0
	return t

def t_SIMPLE_COMMENTS(t):
	r'//.*'


def t_BLOCK_COMMENTS(t):
	r'/\*(\n|.)*?(\*/)'
	t.value=t.value.count('\n')*'\n'
	t_NEWLINE(t)

def t_NEWLINE(t) :
	r'\n+'
	#t.lexer.lineno += len(t.value)
	t.lexer.lineno += t.value.count("\n")

	# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

def t_error(t) :
	print("Illegal character '%s'" %t.value[0])
	t.lexer.skip(1)

lex.lex( )


if __name__ == "__main__":

	prog = open(sys.argv[1]).read()

	lex.input(prog)
	while 1 :
		tok = lex.token()
		if not tok: break
		print("line %d: %s(%s)" %(tok.lineno, tok.type, tok.value))

