define i1 @Bprime(i32 %Inbr_arg)  {
entry:
  %test = alloca double
  store double 0x3463212346, double* %test
  %Inbr = alloca i32 
  store i32 %Inbr_arg, i32* %Inbr
  %Ii = alloca i32 
  store i32 2, i32* %Ii
  br label %for_2
for_2: 
  %0 = load i32* %Inbr
  %1 = sub i32 %0, 1                                        
  %2 = load i32* %Ii
  %3 = icmp sge i32 %1, %2
  br i1 %3, label %for_body_2, label %for_end_2
for_body_2:                                         
  %4 = load i32* %Inbr
  %5 = load i32* %Ii
  %6 = srem i32 %4, %5
  %7 = icmp eq i32 %6, 0
  br i1 %7, label %if_3, label %end_if_3
if_3:                                         
  ret i1 false
end_if_3:                                         
  %8 = load i32* %Ii
  %9 = add i32 %8, 1
  store i32 %9, i32* %Ii
  br label %for_2
for_end_2:                                        
  ret i1 true
}
define void @main() {
entry:
  %0 = call i1 @Bprime(i32 7)
  %Ba = alloca i1 
  store i1 %0, i1* %Ba
  ret void
}