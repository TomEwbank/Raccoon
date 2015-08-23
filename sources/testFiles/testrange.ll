
define void @main(){

entry: 

 %In = alloca i32 
store i32 15 , i32* %In

%0 = load i32* %In
%1 = sdiv i32 %0, 2

 %Ia = alloca i32 
store i32 %1, i32* %Ia

 %Ii = alloca i32 
store i32 0 , i32* %Ii
br label %for_4

for_4:
%2 = load i32* %In
%3 = mul i32 %2, 2

%4 = load i32* %Ia
%5 = add i32 %3, 1

%6 = sub i32 %4, %5

%7 = load i32* %Ii
%8 = icmp sge i32 %6, %7
br i1 %8, label %for_body_4, label %for_end_4

for_body_4:

%9 = load i32* %Ii
call void @display_i(i32 %9)
%10 = load i32* %Ii
%11 = add i32 %10, 1
store i32 %11, i32* %Ii
br label %for_4

for_end_4:
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

