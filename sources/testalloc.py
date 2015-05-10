import re

def add_alloc(s):
	'''This function take an llvm code as argument (in the form of a string)
	   and add to it the missing "alloc" statements. The modified llvm is
	   returned as a string'''
	   
	result = ""
	rest = s
	encountered_var = {}
	while len(rest) > 0:
		try:
			i = rest.index('%') # search for a variable
		except:
			result = result + rest
			break
		
		result = result + rest[0:i+1]
		
		if rest[i-6:i] != "label ": # no need for an "alloc" statement if the variable is preceded by "label"
			
			allocNeeded = True
			
			# Find the variable name that follows the "%" character
			matchObj = re.match(r'[a-zA-Z_][a-zA-Z_0-9]*', rest[i+1:], re.I)
			if matchObj == None:
				allocNeeded = False
			else :
				j = len(matchObj.group())
				varName = rest[i:i+j+1]
				
				# only one "alloc" is need by variable, so check that we didn't encountered it before
				if not encountered_var.has_key(varName):
					encountered_var[varName] = 1
					print(varName)
					
					k = len(result)-1
					char = result[k]
					# going back to the previous line to insert the alloc statement
					while char != '\n':
						k -= 1
						char = result[k]
						# if "define" encountered in the line, variable is an argument and don't need an "alloc"
						if k+6 <= len(result) and result[k:k+6] == "define":
							allocNeeded = False
							break							
				else: allocNeeded = False
			
			if allocNeeded:
				if varName[1] == 'I':
					alloca = " = alloca i32 "
				elif varName[1] == 'F': 
					alloca = " = alloca float "
				elif varName[1] == 'B':
					alloca = " = alloca i1 "
				elif varName[1] == 'L':
					alloca = " = alloca list "
				else:
					print("llvm error: unkown type")
					alloca = " = alloca undef "
					
				result = result[0:k+1] + "  " + varName + alloca + result[k:]

		rest = rest[i+1:]
		
	return result
	
if __name__ == "__main__":
		import sys, os

		prog = file(sys.argv[1]).read()

		# orig_stdout = sys.stdout
		# f = file('result', 'w')
		# sys.stdout = f

		r = add_alloc(prog)

		# sys.stdout = orig_stdout
		# f.close()
		print(r)
		file = open("llvmtest.ll", 'w')
		file.write(r)
		file.close()
		