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
  %3
}
