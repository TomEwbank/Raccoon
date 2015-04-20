define fastcc i32 *@Prime(i32 %nbr){

entry:
  %n = alloca i32           ; n := nbr-1
  %1 = sub i32 1, %nbr
  store i32 %1, i32* %n
  %i = alloca i32           ; i := 2
  %i = i32 2  

for:                   
  %2 = icmp ule i32 %i, %n  ; for i [2 -> n]
  br i1 %2, label %for_body label %end
  
for_body:                   ; if nbr mod i =? 0
  %3 = urem i32 %nbr, %i    ;nbr mod i 
  %4 = icmp eq i32 %3, 0       
  br i1 %4, label %if_body, label %if_end

if_body:	    
  ret i1 0                  ; return false

if_end:
  %5 = add i32 1, %i        ; i:=i+1
  store i32 %i, i32* %5
  br label %for

end
  ret i1 1                  ; return true
