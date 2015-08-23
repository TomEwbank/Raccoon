
define i32* @Quicksort(i32* %LIA_arg, i32 %Ilow_arg, i32 %Ihigh_arg){

entry: 
 %LIA = alloca i32* 
store i32* %LIA_arg, i32** %LIA
 %Ilow = alloca i32 
store i32 %Ilow_arg, i32* %Ilow
 %Ihigh = alloca i32 
store i32 %Ihigh_arg, i32* %Ihigh

br label %if_begin_2

if_begin_2:
%0 = load i32* %Ilow
%1 = load i32* %Ihigh
%2 = icmp slt i32 %0, %1

br i1 %2, label %if_2, label %end_if_2

if_2:

%3 = load i32* %Ilow
%4 = load i32** %LIA
%5 = sext i32 %3 to i64
%6 = getelementptr inbounds i32* %4, i64 %5 
%7 = load i32* %6
 %Ipivot = alloca i32 
store i32 %7, i32* %Ipivot

%8 = load i32* %Ilow
 %Ileftwall = alloca i32 
store i32 %8, i32* %Ileftwall

%9 = load i32* %Ilow
%10 = add i32 %9, 1

 %Ii = alloca i32 
store i32 %10, i32* %Ii
br label %for_6

for_6:
%11 = load i32* %Ii
%12 = load i32* %Ihigh
%13 = icmp sle i32 %11, %12
br i1 %13, label %for_body_6, label %for_end_6

for_body_6:

br label %if_begin_7

if_begin_7:
%14 = load i32* %Ii
%15 = load i32** %LIA
%16 = sext i32 %14 to i64
%17 = getelementptr inbounds i32* %15, i64 %16
%18 = load i32* %17
%19 = load i32* %Ipivot
%20 = icmp slt i32 %18, %19

br i1 %20, label %if_7, label %end_if_7

if_7:

%21 = load i32* %Ileftwall
%22 = add i32 %21, 1

store i32 %22, i32* %Ileftwall

%23 = load i32* %Ii
%24 = load i32** %LIA
%25 = sext i32 %23 to i64
%26 = getelementptr inbounds i32* %24, i64 %25 
%27 = load i32* %26
 %Itemp = alloca i32 
store i32 %27, i32* %Itemp

%28 = load i32* %Ileftwall
%29 = load i32** %LIA
%30 = sext i32 %28 to i64
%31 = getelementptr inbounds i32* %29, i64 %30 
%ait0 = load i32* %31
%32 = load i32* %Ii
%33 = load i32** %LIA
%34 = sext i32 %32 to i64
%35 = getelementptr inbounds i32* %33, i64 %34
store i32 %ait0, i32* %35

%ait1 = load i32* %Itemp
%36 = load i32* %Ileftwall
%37 = load i32** %LIA
%38 = sext i32 %36 to i64
%39 = getelementptr inbounds i32* %37, i64 %38
store i32 %ait1, i32* %39
br label %end_if_7

end_if_7:
%40 = load i32* %Ii
%41 = add i32 %40, 1
store i32 %41, i32* %Ii
br label %for_6

for_end_6:

%42 = load i32* %Ilow
%43 = load i32** %LIA
%44 = sext i32 %42 to i64
%45 = getelementptr inbounds i32* %43, i64 %44 
%46 = load i32* %45
store i32 %46, i32* %Itemp

%47 = load i32* %Ileftwall
%48 = load i32** %LIA
%49 = sext i32 %47 to i64
%50 = getelementptr inbounds i32* %48, i64 %49 
%ait2 = load i32* %50
%51 = load i32* %Ilow
%52 = load i32** %LIA
%53 = sext i32 %51 to i64
%54 = getelementptr inbounds i32* %52, i64 %53
store i32 %ait2, i32* %54

%ait3 = load i32* %Itemp
%55 = load i32* %Ileftwall
%56 = load i32** %LIA
%57 = sext i32 %55 to i64
%58 = getelementptr inbounds i32* %56, i64 %57
store i32 %ait3, i32* %58

%59 = load i32* %Ileftwall
store i32 %59, i32* %Ipivot

%arg4= load i32** %LIA
%arg5= load i32* %Ilow
%60 = load i32* %Ipivot
%61 = sub i32 %60, 1

%62 = call i32* @Quicksort(i32* %arg4, i32 %arg5, i32 %61)

store i32* %62, i32** %LIA

%arg6= load i32** %LIA
%63 = load i32* %Ipivot
%64 = add i32 %63, 1

%arg7= load i32* %Ihigh
%65 = call i32* @Quicksort(i32* %arg6, i32 %64, i32 %arg7)

store i32* %65, i32** %LIA
br label %end_if_2

end_if_2:
%66 = load i32** %LIA
ret i32* %66
ret i32* 0
} 
?1? = getelementptr inbounds [7x i32]* @LIa, i32 0, i32 0
 %LIa = alloca i32* 
store i32* ?2?, i32** %LIa

%arg8= load i32** %LIa
?1? = call i32* @Quicksort(i32* %arg8, i32 1 , i32 7 )

 %LInewa = alloca i32* 
store i32* ?2?, i32** %LInewa
@LIa= global[7 x i32] [i32 5,i32 2,i32 3,i32 15,i32 11,i32 8,i32 89]


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

