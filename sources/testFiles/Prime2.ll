
define i1 @Bprime(i32 %Inbr_arg){

entry: 
 %Inbr = alloca i32 
store i32 %Inbr_arg, i32* %Inbr

 %Bret = alloca i1 
store i1 true, i1* %Bret

 %Ii = alloca i32 
store i32 2 , i32* %Ii
br label %for_4

for_4:
%0 = load i32* %Inbr
%1 = sub i32 %0, 1

%2 = load i32* %Ii
%3 = icmp sge i32 %1, %2
br i1 %3, label %for_body_4, label %for_end_4

for_body_4:

br label %if_begin_5

if_begin_5:
%4 = load i32* %Inbr
%5 = load i32* %Ii
%6 = srem i32 %4, %5

%7 = icmp eq i32 %6, 0

br i1 %7, label %if_5, label %end_if_5

if_5:

store i1 false, i1* %Bret
br label %end_if_5

end_if_5:
%8 = load i32* %Ii
%9 = add i32 %8, 1
store i32 %9, i32* %Ii
br label %for_4

for_end_4:
%10 = load i1* %Bret
ret i1 %10
ret i1 0
} 
define void @main(){

entry: 

%0 = call i1 @Bprime( i32 6 )

 %Ba = alloca i1 
store i1 %0, i1* %Ba

%1 = load i1* %Ba
call void @display_b(i1 %1)

%2 = call i1 @Bprime( i32 7 )

 %Bb = alloca i1 
store i1 %2, i1* %Bb

%3 = load i1* %Bb
call void @display_b(i1 %3)

%4 = call i1 @Bprime( i32 123 )

 %Bc = alloca i1 
store i1 %4, i1* %Bc

%5 = load i1* %Bc
call void @display_b(i1 %5)
ret void
} 

@.strf = private unnamed_addr constant [4 x i8] c"%f\0A\00"
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

@.str = private unnamed_addr constant [4 x i8] c"%d\0A\00"	
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

