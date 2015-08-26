
define i32 @coeffBin(i32 %In_arg, i32 %Im_arg){

entry: 
 %In = alloca i32 
store i32 %In_arg, i32* %In
 %Im = alloca i32 
store i32 %Im_arg, i32* %Im

 %Inum = alloca i32 
store i32 1 , i32* %Inum

%0 = load i32* %Im
%1 = add i32 %0, 1

 %Ii = alloca i32 
store i32 %1, i32* %Ii
br label %for_3

for_3:
%2 = load i32* %Ii
%3 = load i32* %In
%4 = icmp sle i32 %2, %3
br i1 %4, label %for_body_3, label %for_end_3

for_body_3:

%5 = load i32* %Inum
%6 = load i32* %Ii
%7 = mul i32 %5, %6

store i32 %7, i32* %Inum
%8 = load i32* %Ii
%9 = add i32 %8, 1
store i32 %9, i32* %Ii
br label %for_3

for_end_3:

 %Ideno = alloca i32 
store i32 1 , i32* %Ideno

store i32 1 , i32* %Ii
br label %for_7

for_7:
%10 = load i32* %In
%11 = load i32* %Im
%12 = sub i32 %10, %11

%13 = load i32* %Ii
%14 = icmp sge i32 %12, %13
br i1 %14, label %for_body_7, label %for_end_7

for_body_7:

%15 = load i32* %Ideno
%16 = load i32* %Ii
%17 = mul i32 %15, %16

store i32 %17, i32* %Ideno
%18 = load i32* %Ii
%19 = add i32 %18, 1
store i32 %19, i32* %Ii
br label %for_7

for_end_7:

%20 = load i32* %Inum
%21 = load i32* %Ideno
%22 = sdiv i32 %20, %21

ret i32 %22
ret i32 0
} 
define void @main(){

entry: 

%0 = getelementptr inbounds [3x i32]* @LIliste, i32 0, i32 0
 %LIliste = alloca i32* 
store i32* %0, i32** %LIliste


%1 = load i32** %LIliste
call void @display_l_LIliste()
ret void
} 
define void @display_l_LIliste() {
entry:
%0= getelementptr inbounds [3 x i32]* @LIliste, i32 0, i64 0
%1= load i32* %0
call void @display_i(i32 %1)

%2= getelementptr inbounds [3 x i32]* @LIliste, i32 0, i64 1
%3= load i32* %2
call void @display_i(i32 %3)

%4= getelementptr inbounds [3 x i32]* @LIliste, i32 0, i64 2
%5= load i32* %4
call void @display_i(i32 %5)

ret void
}

@LIliste= global[3 x i32] [i32 1,i32 5,i32 8]


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

