
	
a = ["prout", 8, 2, 6, 14]
b = ["prout", 8, 2, 6, 14]

for i in a:
	y = 84
	if i == 2:
		break

print(y)

while i == 3:
	i+=1
	says = 85

print(says)
if a == b:
	print("yeah")
else:
	print("damn")
	
c = {"coucou" : "bitch", "haha":"hihi"}

print(c.get("coucou"))



# tok = 'List Integer'
# stack = [tok]
# stack.append('yo')
# stack.append('bitches')
# stack = 'a' + 'b' + 'c'
# print(stack[0:2])
# t = stack[2:1]
# print(t)


# def string_processing(s):
	# result = s[1:len(s)-1]
	# i = 0
	# while i < len(result)-1:
		# if ord(result[i]) == 92 and ord(result[i+1]) == 34:
			# print("oh")
			# result = result[0:i] + result[i+1:]
		# else:
			# i += 1
	# return result

# print("\"youyou\"")	
# print(string_processing("\"he says \\\"youyou\\\"\""))

# i = ord("\"")
# j = ord("\\")
# print(i)
# print(j)

# import re

# def remcom(s):
	# result = ""
	# rest = s
	# while len(rest) > 0:
		# try:
			# i = rest.index(chr(47)) # get the index of a "/" character
		# except:
			# result += rest
			# break
			
		# if ord(rest[i+1]) == 42: # if the character that follows is "*" -> block comment
			
			# inBlockComment = True
			# j = 2
			# level = 1
			# l = len(rest)
			
			# # Store the new lines encountered in a block comment 
			# # to be able to replace a block comments with 
			# # the right amount of empty lines
			# newLines = "" 
			
			# while inBlockComment:
				# if i+j+1 >= l: break
				# elif ord(rest[i+j]) == 47 and \
				   # ord(rest[i+j+1]) == 42: 
					# # "/*" encountered
					# level += 1
					# j += 2
				# elif ord(rest[i+j]) == 42 and \
				     # ord(rest[i+j+1]) == 47: 
					# # "*/" encountered
					# level -= 1
					# if level == 0: inBlockComment = False
					# j +=2
				# elif ord(rest[i+j]) == 10:
					# # newline encountered 
					# newLines += rest[i+j]
					# j += 1
				# else: j += 1
				
			# if inBlockComment:
				# raise NameError('Block comment reaching EOF without closing, \n check for unclosed nested comment')
			
			# result = result + rest[0:i] + newLines
			# rest = rest[i+j:]
		
		# elif ord(rest[i+1]) == 47: # if the character that follows is "/" -> line comment
			# j = 2
			# while ord(rest[i+j]) != 10:
				# j += 1
			# result = result + rest[0:i]
			# rest = rest[i+j:]
			
		# else :
			# result = result + rest[0:i+1]
			# rest = rest[i+1:]
	
	# return result

# file = open("uncom.rac", "w")	
# file.write(remcom(open("testBon.rac").read()))