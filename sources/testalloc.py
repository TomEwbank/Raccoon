import re

def add_alloc(s):
	result = ""
	rest = s
	while len(rest) > 0:
		try:
			i = rest.index('%')
		except:
			result += rest
			break
			
		if rest[i-5:i] != "label":
			matchObj = re.match(r'[a-zA-Z_][a-zA-Z_0-9]*', rest[i+1:], re.I)
			j = len(matchObj.group())
			print(j)
			varName = rest[i:i+j+1]
			
			k = i
			char = rest[k]
			while char != '\n':
				k -= 1
				char = rest[k]
			
			result = result + rest[0:k+1] + varName + " = alloca undef " + rest[k:i+1]
		else:
			result = result + rest[0:i+1]
			
		rest = rest[i+1:]
		
	return result
	
str = "xxxxxxxxxx\nxxxxxxxxx\nxxxxx %bouBi85fs, xxx\nxxxxxxx\nxxxx %i) xxxx\nxxxxxxxxxx"
str = add_alloc(str)
print(str)