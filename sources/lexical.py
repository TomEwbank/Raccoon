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

nbLexErrors = 0 #global counter for the number of lexical errors

class NestComError(Exception):
   def __init__(self, txt):
      self.msg = txt

#### Utility functions ####

def remove_comments(text):
	from cStringIO import StringIO
	result = StringIO()
	rest = text
	while len(rest) > 1:
		try:
			i = rest.index(chr(47)) # get the index of a "/" character
		except:
			break
		
		if ord(rest[i+1]) == 42: # if the character that follows is "*" -> block comment
			
			inBlockComment = True
			j = 2
			level = 1
			l = len(rest)
			
			# Store the new lines encountered in a block comment 
			# to be able to replace a block comments with 
			# the right amount of empty lines
			newLines = StringIO() 
			
			while inBlockComment:
				if i+j+1 >= l: break
				elif ord(rest[i+j]) == 47 and \
				   ord(rest[i+j+1]) == 42: 
					# "/*" encountered
					level += 1
					j += 2
				elif ord(rest[i+j]) == 42 and \
				     ord(rest[i+j+1]) == 47: 
					# "*/" encountered
					level -= 1
					if level == 0: inBlockComment = False
					j +=2
				elif ord(rest[i+j]) == 10:
					# newline encountered 
					newLines.write(rest[i+j])
					j += 1
				else: j += 1
				
			if inBlockComment:
				raise NestComError("Block comment reached EOF without closing, \n check for unclosed nested comment")
			
			result.write(rest[0:i])
			result.write(newLines.getvalue())
			rest = rest[i+j:]
		
		elif ord(rest[i+1]) == 47: # if the character that follows is "/" -> line comment
			j = 2
			while ord(rest[i+j]) != 10:
				j += 1
			result.write(rest[0:i])
			rest = rest[i+j:]
			
		else :
			result.write(rest[0:i+1])
			rest = rest[i+1:]
	
	result.write(rest)
	
	return result.getvalue()

#def string_processing(s):
	# result = s[1:len(s)-1]
	# i = 0
	# while i < len(result)-1:
		# if ord(result[i]) == 92 and ord(result[i+1]) == 34:
			# result = result[0:i] + result[i+1:]
		# else:
			# i += 1
	# return result
	

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
	# 'STRING',
	
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
	'Integer' : 'T_INT',
	'Double' : 'T_DOUBLE',
	'Boolean' : 'T_BOOL',
	'List_Integer' : 'T_LIST_INT',
	'List_Double' : 'T_LIST_DOUBLE',
	'List_Boolean' : 'T_LIST_BOOL',
	# 'List_String' : 'T_LIST_STRING',
	# 'String' : 'T_STRING',

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

t_LSBRACKET=r'\['
t_RSBRACKET=r'\]'

def t_indent_error(t):
	r'[\n\t ]*\n[\t]*[ ]+'
	l = t.value.count('\n')
	t.lexer.lineno += l
	print("Warning l.%d: use of spaces after tab(s) leads to erronous indent" %(t.lexer.lineno))

def t_END_STATEMENT(t):
	r'[\n\t ]*\n[\t]*'
	l = t.value.count('\n')
	t.lexer.lineno += l
	return t
	
# def t_STRING(t):
	# r'".*"'
	# t.value = t.value[1:len(t.value)-1]
	# return t

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
	print("Lexical error l.%d: Illegal character '%s'" %(t.lexer.lineno, t.value[0]))
	global nbLexErrors
	nbLexErrors += 1
	t.lexer.skip(1)

t_ignore = ' '

# create the first stage
lexer = lex.lex()


#### SECOND LEXING STAGE ####

class IndentLexer(object):
	'''A second lexing stage that generates the appropriate
	   tokens representing the indentation'''
	
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
		change = self.calc_indent(n, token)
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

	def calc_indent(self, nbTabs, token):
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
				print("Lexical error l.%d: wrong indentation level" %(token.lineno))
				global nbLexErrors
				nbLexErrors += 1
			i -= 1
		return i

# create the second stage
lexer = IndentLexer(lexer)


#########################################################

if __name__ == "__main__":
	try:
		prog = open(sys.argv[1]).read() + "\n" 
		lexer.input(remove_comments(prog))
		while 1 :
			tok = lexer.token()
			if not tok: 
				break
			else:
				print("line %d: %s(%s)" %(tok.lineno, tok.type, tok.value))
	except NestComError as e:
		print("error:")
		print(e)
			

