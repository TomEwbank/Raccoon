;En cours

define fastcc i32 *@Quicksort(i32* %A,i32 %low, i32 %high){

entry:
  %1 = icmp ugt i32 %high, %low       ;if(high>low)
  br i1 %1, label %body, label %end
  
body:
  X                                   ;pivot := A[low]
  %leftwall = alloca i32              ;leftwall := low
  store i32 %low, i32* %leftwall
  %i = alloca i32                     ;i = low+1
  %2=add i32 1, %low
  store i32 %2, i32* %i
  
for:
  %3 = icmp ule i32 %i, %high         ;for i [low+1 -> high]
  br i1 %3, label %for_body label %for_end

for_body:
  %4 = icmp ult i32 X A[i] X , %pivot ;if A[i]<pivot
  br i1 %4, label %if_body, label %if_end
  
if_body:
  %5 = add i32 1, %leftwall           ;leftwall++
  store i32 %5, i32* %leftwall
  X                                   ;temp:=A[i]
  X                                   ;A[i]:=A[leftwall]
  X                                   ;A[leftwall]:=temp

if_end:
  %9 = add i32 1, %i                  ;i:=i+1
  store i32 %i, i32* %i
  br label %for

for_end
  X                                   ;temp := A[low]
  X                                   ;A[low]:=A[leftwall]
  X                                   ;A[leftwall]:=temp
  store i32 %leftwall, i32* %pivot    ;pivot:=leftwall

end
  ret i32* %A
  
}
