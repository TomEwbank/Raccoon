
define i1 @Bprime(i32 %Inbr_arg){

entry: 
 %Inbr = alloca i32 
store i32 %Inbr_arg, i32* %Inbr

 %Ii = alloca i32 
store i32 2 , i32* %Ii
br label %for_2

for_2:
%0 = load i32* %Inbr
%1 = sub i32 %0, 1

%2 = load i32* %Ii
%3 = icmp sge i32 %1, %2
br i1 %3, label %for_body_2, label %for_end_2

for_body_2:

br label %if_begin_3

if_begin_3:
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
ret i1 0
} 


define void @main(){

entry: 
%0 = call i1 @Bprime( i32 7 )
 %Ba = alloca i1 
store i1 %0, i1* %Ba

%1 = load i1* %Ba
call void @display_b(i1 %1)
ret void
} 



@.strf = private unnamed_addr constant [4 x i8] c"\0A%f\00"
define void @display_f(float %n)  {
entry:
  %n.addr = alloca float
  store float %n, float* %n.addr
  %0 = load float* %n.addr
  %1 = fpext float %0 to double
  %2 = getelementptr inbounds [4 x i8]* @.strf, i32 0, i32 0
  %call = call i32 (i8*, ...)* @printf(i8* %2, double %1)
  ret void
}

@.str = private unnamed_addr constant [4 x i8] c"\0A%d\00"	
define void @display_i(i32 %n) {
entry:
  %n.addr = alloca i32
  store i32 %n, i32* %n.addr
  %0 = load i32* %n.addr
  %1 = getelementptr inbounds [4 x i8]* @.str, i32 0, i32 0
  %2 = call i32 (i8*, ...)* @printf(i8* %1, i32 %0)
  ret void
}
define void @display_b(i1 %n) {
entry:
  %n.addr = alloca i1
  store i1 %n, i1* %n.addr
  %0 = load i1* %n.addr
  %1 = getelementptr inbounds [4 x i8]* @.str, i32 0, i32 0
  %2 = call i32 (i8*, ...)* @printf(i8* %1, i1 %0)
  ret void
}


declare i32 @printf(i8*, ...)

