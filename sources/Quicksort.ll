;En cours

define fastcc i32 *@Quicksort(i32* %A,i32 %low, i32 %high){

entry:
  %1 = icmp ugt i32 %high, %low       ;if(high>low)
  br i1 %1, label %body, label %end
  
body:
  %pivot = alloca i32                 ;pivot := A[low]
%1ptrlow = load i32* %low
%1ptr = getelementptr inbounds i32* %A, i32 %1ptrlow
%pivot = load i32* %1ptr
  %leftwall = alloca i32              ;leftwall := low
  store i32 %low, i32* %leftwall
  %i = alloca i32                     ;i = low+1
  %2=add i32 1, %low
  store i32 %2, i32* %i
  
for:
  %3 = icmp ule i32 %i, %high         ;for i [low+1 -> high]
  br i1 %3, label %for_body label %for_end

for_body:
%3ptri = load i32* %i
%3ptr = getelementptr inbounds i32* %A, i32 %3ptri
%3Ai = load i32* %3ptr
  %4 = icmp ult i32 %3Ai , %pivot     ;if A[i]<pivot
  br i1 %4, label %if_body, label %if_end

if_body:
  %5 = add i32 1, %leftwall           ;leftwall++
  store i32 %5, i32* %leftwall
  
  %temp = alloca i32                  ;temp:=A[i]
  %6ptri = load i32* %i             
  %6ptr = getelementptr inbounds i32* %A, i32 %6ptri
  %temp = load i32* %6ptr

  X                                   ;A[i]:=A[leftwall]
 
  %8ptrleftwall = load i32* %leftwall ;A[leftwall]:=temp
  %8ptr = getelementptr inbounds i32* %A, i32 %8ptrleftwall
  store i32 %temp, 32* %8ptr

if_end:
  %9 = add i32 1, %i                  ;i:=i+1
  store i32 %i, i32* %i
  br label %for

for_end
  %9ptrlow = load i32* %low             ;temp := A[low]
  %9ptr = getelementptr inbounds i32* %A, i32 %9ptrlow
  %temp = load i32* %9ptr

  X                                   ;A[low]:=A[leftwall]
  
  %10ptrleftwall = load i32* %leftwall;A[leftwall]:=temp
  %10ptr = getelementptr inbounds i32* %A, i32 %10ptrleftwall
  store i32 %temp, 32* %10ptr
  
  store i32 %leftwall, i32* %pivot    ;pivot:=leftwall

end
  ret i32* %A
  
}
