
define void @Quicksort(i32* %LIAF1_arg, i32 %IlowF1_arg, i32 %IhighF1_arg){

entry: 
 %LIAF1 = alloca i32* 
store i32* %LIAF1_arg, i32** %LIAF1
 %IlowF1 = alloca i32 
store i32 %IlowF1_arg, i32* %IlowF1
 %IhighF1 = alloca i32 
store i32 %IhighF1_arg, i32* %IhighF1

br label %if_begin_4

if_begin_4:
%0 = load i32* %IlowF1
%1 = load i32* %IhighF1
%2 = icmp slt i32 %0, %1

br i1 %2, label %if_4, label %end_if_4

if_4:

%3 = load i32* %IlowF1
%4 = load i32** %LIAF1
%5 = sext i32 %3 to i64
%6 = getelementptr inbounds i32* %4, i64 %5 
%7 = load i32* %6
 %IpivotC10 = alloca i32 
store i32 %7, i32* %IpivotC10

%8 = load i32* %IlowF1
 %IleftwallC10 = alloca i32 
store i32 %8, i32* %IleftwallC10

%9 = load i32* %IlowF1
%10 = add i32 %9, 1

 %IiC10 = alloca i32 
store i32 %10, i32* %IiC10
br label %for_8

for_8:
%11 = load i32* %IiC10
%12 = load i32* %IhighF1
%13 = icmp sle i32 %11, %12
br i1 %13, label %for_body_8, label %for_end_8

for_body_8:

br label %if_begin_9

if_begin_9:
%14 = load i32* %IiC10
%15 = load i32** %LIAF1
%16 = sext i32 %14 to i64
%17 = getelementptr inbounds i32* %15, i64 %16
%18 = load i32* %17
%19 = load i32* %IpivotC10
%20 = icmp slt i32 %18, %19

br i1 %20, label %if_9, label %end_if_9

if_9:

%21 = load i32* %IleftwallC10
%22 = add i32 %21, 1

store i32 %22, i32* %IleftwallC10

%23 = load i32* %IiC10
%24 = load i32** %LIAF1
%25 = sext i32 %23 to i64
%26 = getelementptr inbounds i32* %24, i64 %25 
%27 = load i32* %26
 %Itemp1C12 = alloca i32 
store i32 %27, i32* %Itemp1C12

%28 = load i32* %IleftwallC10
%29 = load i32** %LIAF1
%30 = sext i32 %28 to i64
%31 = getelementptr inbounds i32* %29, i64 %30 
%ait0 = load i32* %31
%32 = load i32* %IiC10
%33 = load i32** %LIAF1
%34 = sext i32 %32 to i64
%35 = getelementptr inbounds i32* %33, i64 %34
store i32 %ait0, i32* %35

%ait1 = load i32* %Itemp1C12
%36 = load i32* %IleftwallC10
%37 = load i32** %LIAF1
%38 = sext i32 %36 to i64
%39 = getelementptr inbounds i32* %37, i64 %38
store i32 %ait1, i32* %39
br label %end_if_9

end_if_9:
%40 = load i32* %IiC10
%41 = add i32 %40, 1
store i32 %41, i32* %IiC10
br label %for_8

for_end_8:

%42 = load i32* %IlowF1
%43 = load i32** %LIAF1
%44 = sext i32 %42 to i64
%45 = getelementptr inbounds i32* %43, i64 %44 
%46 = load i32* %45
 %Itemp2C10 = alloca i32 
store i32 %46, i32* %Itemp2C10

%47 = load i32* %IleftwallC10
%48 = load i32** %LIAF1
%49 = sext i32 %47 to i64
%50 = getelementptr inbounds i32* %48, i64 %49 
%ait2 = load i32* %50
%51 = load i32* %IlowF1
%52 = load i32** %LIAF1
%53 = sext i32 %51 to i64
%54 = getelementptr inbounds i32* %52, i64 %53
store i32 %ait2, i32* %54

%ait3 = load i32* %Itemp2C10
%55 = load i32* %IleftwallC10
%56 = load i32** %LIAF1
%57 = sext i32 %55 to i64
%58 = getelementptr inbounds i32* %56, i64 %57
store i32 %ait3, i32* %58

%59 = load i32* %IleftwallC10
store i32 %59, i32* %IpivotC10

%arg4= load i32** %LIAF1
%arg5= load i32* %IlowF1
%60 = load i32* %IpivotC10
%61 = sub i32 %60, 1

call void @Quicksort(i32* %arg4, i32 %arg5, i32 %61)


%arg6= load i32** %LIAF1
%62 = load i32* %IpivotC10
%63 = add i32 %62, 1

%arg7= load i32* %IhighF1
call void @Quicksort(i32* %arg6, i32 %63, i32 %arg7)

br label %end_if_4

end_if_4:
ret void
} 
define void @main(){

entry: 

%0 = getelementptr inbounds [4x i32]* @LIaF1, i32 0, i32 0
 %LIaF1 = alloca i32* 
store i32* %0, i32** %LIaF1


%1 = getelementptr inbounds [5x i32]* @LIbF1, i32 0, i32 0
 %LIbF1 = alloca i32* 
store i32* %1, i32** %LIbF1


%2 = getelementptr inbounds [7x i32]* @LIcF1, i32 0, i32 0
 %LIcF1 = alloca i32* 
store i32* %2, i32** %LIcF1


 %IdF1 = alloca i32 
store i32 11111 , i32* %IdF1

%3 = load i32** %LIaF1
call void @display_l_LIaF1()

%arg8= load i32** %LIaF1
call void @Quicksort(i32* %arg8, i32 0 , i32 3 )


%4 = load i32** %LIaF1
call void @display_l_LIaF1()

%5 = load i32** %LIbF1
call void @display_l_LIbF1()

%arg9= load i32** %LIbF1
call void @Quicksort(i32* %arg9, i32 0 , i32 4 )


%6 = load i32** %LIbF1
call void @display_l_LIbF1()

%7 = load i32** %LIcF1
call void @display_l_LIcF1()

%arg10= load i32** %LIcF1
call void @Quicksort(i32* %arg10, i32 0 , i32 7 )


%8 = load i32** %LIcF1
call void @display_l_LIcF1()
ret void
} 
define void @display_l_LIaF1() {
entry:
%0= getelementptr inbounds [4 x i32]* @LIaF1, i32 0, i64 0
%1= load i32* %0
call void @display_i(i32 %1)

%2= getelementptr inbounds [4 x i32]* @LIaF1, i32 0, i64 1
%3= load i32* %2
call void @display_i(i32 %3)

%4= getelementptr inbounds [4 x i32]* @LIaF1, i32 0, i64 2
%5= load i32* %4
call void @display_i(i32 %5)

%6= getelementptr inbounds [4 x i32]* @LIaF1, i32 0, i64 3
%7= load i32* %6
call void @display_i(i32 %7)

ret void
}

define void @display_l_LIcF1() {
entry:
%0= getelementptr inbounds [7 x i32]* @LIcF1, i32 0, i64 0
%1= load i32* %0
call void @display_i(i32 %1)

%2= getelementptr inbounds [7 x i32]* @LIcF1, i32 0, i64 1
%3= load i32* %2
call void @display_i(i32 %3)

%4= getelementptr inbounds [7 x i32]* @LIcF1, i32 0, i64 2
%5= load i32* %4
call void @display_i(i32 %5)

%6= getelementptr inbounds [7 x i32]* @LIcF1, i32 0, i64 3
%7= load i32* %6
call void @display_i(i32 %7)

%8= getelementptr inbounds [7 x i32]* @LIcF1, i32 0, i64 4
%9= load i32* %8
call void @display_i(i32 %9)

%10= getelementptr inbounds [7 x i32]* @LIcF1, i32 0, i64 5
%11= load i32* %10
call void @display_i(i32 %11)

%12= getelementptr inbounds [7 x i32]* @LIcF1, i32 0, i64 6
%13= load i32* %12
call void @display_i(i32 %13)

ret void
}

define void @display_l_LIbF1() {
entry:
%0= getelementptr inbounds [5 x i32]* @LIbF1, i32 0, i64 0
%1= load i32* %0
call void @display_i(i32 %1)

%2= getelementptr inbounds [5 x i32]* @LIbF1, i32 0, i64 1
%3= load i32* %2
call void @display_i(i32 %3)

%4= getelementptr inbounds [5 x i32]* @LIbF1, i32 0, i64 2
%5= load i32* %4
call void @display_i(i32 %5)

%6= getelementptr inbounds [5 x i32]* @LIbF1, i32 0, i64 3
%7= load i32* %6
call void @display_i(i32 %7)

%8= getelementptr inbounds [5 x i32]* @LIbF1, i32 0, i64 4
%9= load i32* %8
call void @display_i(i32 %9)

ret void
}

@LIaF1= global[4 x i32] [i32 4,i32 3,i32 2,i32 1]

@LIbF1= global[5 x i32] [i32 1,i32 3,i32 5,i32 1,i32 5]

@LIcF1= global[7 x i32] [i32 4,i32 3,i32 2,i32 1,i32 7,i32 3,i32 4]


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

