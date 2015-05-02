define fastcc i32 *@Quicksort(i32* %A,i32 %low, i32 %high){

entry:
  %0 = icmp ugt i32 %high, %low           ; if(high>low)
  br i1 %0, label %body, label %end
  
  
body:
  %pivot = alloca i32                     ; pivot := A[low]
  %1 = load i32* %low
  %2 = getelementptr inbounds i32* %A, i32 %1
  %pivot = load i32* %2
  
  %leftwall = alloca i32                  ; leftwall := low
  store i32 %low, i32* %leftwall
  
  %i = alloca i32                         ; i = low+1
  %3 = add i32 1, %low
  store i32 %3, i32* %i
  
  
for:
  %4 = icmp ule i32 %i, %high            ; for i [low+1 -> high]
  br i1 %4, label %for_body label %for_end


for_body:
  %5 = load i32* %i                   ; if A[i]<pivot
  %6 = getelementptr inbounds i32* %A, i32 %5
  %7 = load i32* %6
  %8 = icmp ult i32 %7 , %pivot
  br i1 %8, label %if_body, label %if_end


if_body:
  %9 = add i32 1, %leftwall               ; leftwall++
  store i32 %9, i32* %leftwall

  
  %temp = alloca i32                      ; temp:=A[i]
  %7ptri = load i32* %i             
  %7ptr = getelementptr inbounds i32* %A, i32 %7ptri
  %temp = load i32* %7ptr

  %8ptrleftwall = load i32* %leftwall     ; A[i]:=A[leftwall]  
  %8ptr1 = getelementptr inbounds i32* %A, i32 %8ptrleftwall
  %8valueInLeftwall = load i32* %8ptr1
  %8ptri = load i32* %i          
  %8ptr2 = getelementptr inbounds i32* %A, i32 %8ptri
  store i32 %8valueInLeftwall, i32* %8ptr2
 
  %9ptrleftwall = load i32* %leftwall     ; A[leftwall]:=temp
  %9ptr = getelementptr inbounds i32* %A, i32 %9ptrleftwall
  store i32 %temp, i32* %9ptr


if_end:
  %4c = add i32 1, %i                     ; i:=i+1
  store i32 %i, i32* %4c
  br label %for


for_end
  %10ptrlow = load i32* %low              ; temp := A[low]
  %10ptr = getelementptr inbounds i32* %A, i32 %10ptrlow
  %temp = load i32* %10ptr

  %11ptrleftwall = load i32* %leftwall    ; A[low]:=A[leftwall]  
  %11ptr1 = getelementptr inbounds i32* %A, i32 %11ptrleftwall
  %11valueInLeftwall = load i32* %11ptr1
  %11ptrlow = load i32* %low          
  %11ptr2 = getelementptr inbounds i32* %A, i32 %11ptrlow
  store i32 %11valueInLeftwall, i32* %11ptr2
  
  %12ptrleftwall = load i32* %leftwall    ; A[leftwall]:=temp
  %12ptr = getelementptr inbounds i32* %A, i32 %12ptrleftwall
  store i32 %temp, i32* %12ptr
  
  store i32 %leftwall, i32* %pivot        ;pivot:=leftwall
  
  %1415 = load i32* %pivot                ; A := Quicksort(A,low, pivot - 1)
  %14a = load i32* %low
  %14b = sub i32 %1415, 1
  %A = call fastcc void (i32*, i32, i32)* @swap(i32* %A, i32 %14a , i32 %14b) 
 
  %15a = add i32 %1415, 1                 ; A := Quicksort(A, pivot + 1, high)
  %15b = load i32* %high
  %A = call fastcc void (i32*, i32, i32)* @swap(i32* %A, i32 %15a , i32 %15b) 
  
end
  ret i32* %A
  
}
