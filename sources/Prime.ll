;//return true if the number nbr is prime. Return false otherwise

;	for i in range (2,n):
;		if nbr mod i =? 0:
;			return false
;		end
;	end
;	return true


define fastcc i32 *@Prime(i32 %nbr){

entry:
  %n = alloca i32                         ; n := nbr-1
  %1=sub i32 1, %nbr
  store i32 %1, i32* %n
  
for:
  %i = i32 2                              ;for i [2 -> n]
  %2 = icmp ule i32 %i, %n   
  br i1 %2, label %for_body label %for_end
  
for_body: ;si i<=n, if_body  sinon for_end


if_body::	if nbr mod i =? 0: if_body sinon if_end
    ret i32* %A   return false

if_end:
  %4c = add i32 1, %i                     ; i:=i+1
  store i32 %i, i32* %4c
  br label %for


for_end







end
  ret i32* %A   return true
