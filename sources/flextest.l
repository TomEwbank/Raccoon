%{

#include "stack.h"

STACK indent;
int init_indent = 1;

%}

/* regular definitions */

letter		[A-Za-z]
digit       [0-9]
id        	{letter}({letter}|{digit})*
integer  	{digit}+
double      {digit}+\.{digit}*

%%

^\n     	{}
\n[ ]*		{if (init_indent)
			 {
				initStack(&indent, 100);
				init_indent = 0;
			 }

			 if (yyleng == 1)
		     {
				if (indent.size > 0)
				{
					pop(&indent);
					if (peek(&indent) > yyleng && indent.size != 0)
						yyless(0);
					printf("DEDENT \n");
				}
				printf("END_STATEMENT \n");
				}
		     else	
		     {
				if (peek(&indent) < yyleng || indent.size == 0)
				{
					push(&indent, yyleng);
					printf("INDENT \n");
				}
				else if (peek(&indent) > yyleng && indent.size != 0)
				{
					pop(&indent);
					if (peek(&indent) > yyleng && indent.size != 0)
						yyless(0);
					printf("DEDENT \n");
				}
				else
				{
					printf("END_STATEMENT \n");
				}
		     }}
 
<<EOF>>		{if (init_indent)
			 {
				initStack(&indent, 100);
				init_indent = 0;
			 }
			 if (indent.size > 0)
             {
				pop(&indent);
                printf("DEDENT \n");
             }
			 freeStack(&indent);
             yyterminate();}
[ ]*		
becomes 	printf("T_ASSIGN \n");
is 			printf("T_CONST \n");
or			printf("T_OR \n");
and			printf("T_AND \n");
True		printf("T_TRUE \n");
False		printf("T_FALSE \n");
function	printf("T_FUN \n");
return		printf("T_RET \n");
if			printf("T_IF \n");
"else if"	printf("T_EIF \n");
else		printf("T_ELSE \n");
while		printf("T_WHILE \n");
break		printf("T_BREAK \n");
continue	printf("T_CONT \n");
for			printf("T_FOR \n");
in 			printf("T_IN \n");
range		printf("T_RANGE \n");
"=?"        printf("T_CEQ \n");
"!="        printf("T_CNE \n");
"<"         printf("T_CLT \n");
"<="        printf("T_CLE \n");
">"         printf("T_CGT \n");
">="        printf("T_CGE \n");
"("         printf("T_LPAREN \n");
")"         printf("T_RPAREN \n");
":"         printf("T_COLON \n");
","         printf("T_COMMA \n");
"+"         printf("T_PLUS \n");
"-"         printf("T_MINUS \n");
"*"         printf("T_MUL \n");
"/"         printf("T_DIV \n");
mod			printf("T_MOD \n");
{id}  		printf("T_IDENTIFIER \n");
{double}    printf("T_DOUBLE \n");
{integer}   printf("T_INTEGER \n");
.           printf("Unknown token!\n"); yyterminate();

%%			 
