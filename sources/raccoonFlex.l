%{
#define YYSTYPE double /* Define the main semantic type */
#include <string.h> /* for strdup */
#include "raccoonParser.tab.h" /* for token definitions and yylval */
#include "stack.h"

STACK indent;
int init_indent = 1;

%}

%option yylineno /* Ask flex to put line number in yylineno */

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
					return(DEDENT);
				}
				return(END_STATEMENT);
				}
		     else	
		     {
				if (peek(&indent) < yyleng || indent.size == 0)
				{
					push(&indent, yyleng);
					return(INDENT);
				}
				else if (peek(&indent) > yyleng && indent.size != 0)
				{
					pop(&indent);
					if (peek(&indent) > yyleng && indent.size != 0)
						yyless(0);
					return(DEDENT);
				}
				else
				{
					return(END_STATEMENT);
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
                return(DEDENT);
             }
			 freeStack(&indent);
             yyterminate();}

[ ]*		
becomes 	return(T_ASSIGN);
is 			return(T_CONST);
or			return(T_OR);
and			return(T_AND);
True		return(T_TRUE);
False		return(T_FALSE);
function	return(T_FUN);
return		return(T_RET);
if			return(T_IF);
"else if"	return(T_EIF);
else		return(T_ELSE);
while		return(T_WHILE);
break		return(T_BREAK);
continue	return(T_CONT);
for			return(T_FOR);
in 			return(T_IN);
range		return(T_RANGE);
"=?"        return(T_CEQ);
"!="        return(T_CNE);
"<"         return(T_CLT);
"<="        return(T_CLE);
">"         return(T_CGT);
">="        return(T_CGE);
"("         return(T_LPAREN);
")"         return(T_RPAREN);
":"         return(T_COLON);
","         return(T_COMMA);
"+"         return(T_PLUS);
"-"         return(T_MINUS);
"*"         return(T_MUL);
"/"         return(T_DIV);
mod			return(T_MOD);
{id}  		{yylval.id = (char *) strdup(yytext); 
			 return(T_IDENTIFIER);}
{double}    yylval.dval = atof(yytext); return(T_DOUBLE);
{integer}   yylval.ival = atoi(yytext); return(T_INTEGER);
.           printf("Unknown token!\n"); yyterminate();

%%			 
