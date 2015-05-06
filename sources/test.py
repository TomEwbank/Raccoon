# tok = 'List Integer'
# stack = [tok]
# stack.append('yo')
# stack.append('bitches')
# stack = 'a' + 'b' + 'c'
# print(stack[0:2])
# t = stack[2:1]
# print(t)


def string_processing(s):
	result = s[1:len(s)-1]
	i = 0
	while i < len(result)-1:
		if ord(result[i]) == 92 and ord(result[i+1]) == 34:
			print("oh")
			result = result[0:i] + result[i+1:]
		else:
			i += 1
	return result

print("\"youyou\"")	
print(string_processing("\"he says \\\"youyou\\\"\""))

i = ord("\"")
j = ord("\\")
print(i)
print(j)