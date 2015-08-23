
define void @main(){

entry: 

 %In = alloca i32 
store i32 15 , i32* %In

 %Ia = alloca i32 
store i32 2 , i32* %Ia

 %Db = alloca double 
store double 8.45 , double* %Db

%0 = load double* %Db
%1 = fdiv double %0, 2.02

 %Dc = alloca double 
store double %1, double* %Dc

%2 = load double* %Db
call void @display_f(double %2)

 %Ii = alloca i32 
store i32 0 , i32* %Ii
br label %for_7

for_7:
%3 = load i32* %In
%4 = sdiv i32 %3, 2

%5 = load i32* %Ii
%6 = icmp sge i32 %4, %5
br i1 %6, label %for_body_7, label %for_end_7

for_body_7:

%7 = load i32* %Ii
call void @display_i(i32 %7)
%8 = load i32* %Ii
%9 = add i32 %8, 1
store i32 %9, i32* %Ii
br label %for_7

for_end_7:
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

