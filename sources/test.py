tok = 'List Integer'
stack = [tok]
stack.append('yo')
stack.append('bitches')
stack = 'a' + 'b' + 'c'
print(stack[0:2])
t = stack[2:1]
print(t)


import re

line = "dogsCats are smarter dogs than dogs";

matchObj = re.match( r'dogs', line, re.M|re.I)
if matchObj:
   print "match --> matchObj.group() : ", matchObj.group()
else:
   print "No match!!"

searchObj = re.search( r'dogs', line, re.M|re.I)
if searchObj:
   print "search --> searchObj.group() : ", searchObj.group()
else:
   print "Nothing found!!"