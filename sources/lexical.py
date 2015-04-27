#############################################################################################
#  lexical.py,																				#
#																							#
# Lexical analyser for the Raccoon language, using PLY.										#				#
#																							#
# May 2015, CATUSANU Paul, EWBANK Tom and VAN DE GOOR Elodie.								#
#############################################################################################

import ply.lex as lex
import re
import sys
import copy

#### FIRST LEXING STAGE ####

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
	'LSBRACKET',
	'RSBRACKET',
	
	'END_STATEMENT',
	'DEDENT',
	'INDENT',
	'STRING',
	
	'ELSEIF',
	'MOD_OP'
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
	'function' :  'FUNCTION',
	'display' : 'DISPLAY',

}

tokens += list(reserved.values())

# t_TAB = r'\t'

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

t_LSBRACKET=r'\['
t_RSBRACKET=r'\]'

def t_END_STATEMENT(t):
	r'[\n\t]*\n[\t]*'
	l = t.value.count('\n')*'\n'
	t.lexer.lineno += len(l)
	return t
	
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

	
def t_error(t) :
	print("Illegal character '%s'" %t.value[0])
	t.lexer.skip(1)

t_ignore = ' '

# create the first stage
lexer = lex.lex()


#### SECOND LEXING STAGE ####

class IndentLexer(object):
	'''A second lexing stage that interprets TABS
	   Manages Off-Side Rule for indentation'''
	
	def __init__(self, lexer):
		self.indents = [0]  # indentation stack
		self.tokens = []    # token queue
		self.lexer = lexer

	def input(self, *args, **kwds):
		self.lexer.input(*args, **kwds)

	# Iterator interface
	def __iter__(self):
		return self

	def next(self):
		t = self.token()
		if t is None:
			raise StopIteration
		return t

	__next__ = next

	def token(self):
		# empty our buffer first
		if self.tokens:
			return self.tokens.pop(0)

		# grab the next from first stage
		token = self.lexer.token()

		# we only care about indentation stored in END_STATEMENT tokens
		if not token or token.type != 'END_STATEMENT':
			return token
		
		# calculate number of tabs in the indentation
		n = 0;
		end = len(token.value)-1
		while token.value[end-n] == '\t':
			n += 1 
			
		# check for new indent/dedent
		change = self._calc_indent(n)
		if not(change):
			return token
			
		
		# indentation change
		if change == 1:
			token.type = 'INDENT'
			self.tokens.append(copy.copy(token))
			token.type = 'END_STATEMENT'
			return token

		# dedenting one or more times
		assert change < 0
		change += 1
		token.type = 'DEDENT'
		self.tokens.append(copy.copy(token))

		# buffer any additional DEDENTs
		while change:
			self.tokens.append(copy.copy(token))
			change += 1
		
		token.type = 'END_STATEMENT'
		return token

	def _calc_indent(self, nbTabs):
		'''returns a number representing indents added or removed'''
		
		indents = self.indents # stack of space numbers
		if nbTabs > indents[-1]:
			indents.append(nbTabs)
			return 1

		# we are at the same level
		if nbTabs == indents[-1]:
			return 0

		# dedent one or more times
		i = 0
		while nbTabs < indents[-1]:
			indents.pop()
			if nbTabs > indents[-1]:
				raise SyntaxError("wrong indentation level")
			i -= 1
		return i

# create the second stage
lexer = IndentLexer(lexer)

#### comments remover function ####

def remove_comments(text):
	def replacer(match):
		s = match.group(0)
		if s.startswith('/'):
			return ""
		else:
			return s
	pattern = re.compile(
		r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
		re.DOTALL | re.MULTILINE
	)
	return re.sub(pattern, replacer, text)

	
#########################################################

if __name__ == "__main__":
	prog = remove_comments(open(sys.argv[1]).read())
	lexer.input(prog)
	while 1 :
		tok = lexer.token()
		if not tok: 
			break
		else:
			print("line %d: %s(%s)" %(tok.lineno, tok.type, tok.value))
			

