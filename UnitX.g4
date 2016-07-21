/*
 * The MIT License (MIT)
 * Copyright (c) 2015-2016 Tasuku TAKAHASHI 
 * All rights reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

/*
 * 【A grammar of UnitX】
 * This grammar can be a parser of UnitX by using ANTLR4.
 * ANTLR4 is a parser generator made using Java by Prof. Terence Parr and the reasearch team.
 * So you absolutely need the Java language. Follow an example such as below.
 * 
 *     java -jar antlr-4.5.1-complete.jar UnitX.g4 
 * 
 * See "http://www.antlr.org/" on detail! if you'd like to know about the generator. 
 * Enjoy!!!!
 */
grammar UnitX;

/*
 * A grammar will start from here.
 *
 * A starting point of Parser RULE is 'program'.
 * Memo (to my future self): if someone or I could add RULES of import statement or name space, Add the RULES to a 'typeDeclaration' RULE.
 */
program
	: typeDeclaration* EOF 
	;

typeDeclaration
	: statement
	| functionDeclaration
	;

functionDeclaration
	: 'def' Identifier formalParameters block
	;

formalParameters
    : formalParameterList?
    | '(' formalParameterList? ')'
    ;

formalParameterList
    : formalParameter (',' formalParameter)* 
    ;

formalParameter
    : Identifier ('=' expression)?
    ;

block
    : '{' blockStatement*  '}'
    ;

blockStatement
    : statement
    ;

statement
	: block
	| repStatement
	| ifStatement
	| expressionStatement SEMICOLON?
	| 'return' expression? SEMICOLON?
	| 'break' SEMICOLON?
	| 'continue' SEMICOLON?
	| printStatement SEMICOLON?
	| assertStatement SEMICOLON?
	| dumpStatement SEMICOLON?
	| borderStatement SEMICOLON?
	;

repStatement
    : 'rep' repControl statement 
    | 'rep' '(' repControl ')' statement 
	;

ifStatement
    : 'if' parExpression statement ('else' statement)?
	;

expressionStatement
	: expression
	;

printStatement
	: 'print' expression? (',' expression)*
	;

assertStatement
	: 'assert' expression?
	;

dumpStatement
	: '>' '>' expression? (',' expression)*
	;

borderStatement
	: '---'
	| '----'
	| '-----'
	| '------'
	| '-------'
	| '--------'
	| '---------'
	| '----------'
	;

expressionList
    : expression (',' expression)*
    ;

parExpression
	: expression
	| '(' expression ')'
	;

repControl
	: Identifier ',' endRep
	;

endRep
	: expression
	;

expression
	: primary
	| expression '(' expressionList? ')'
	| expression ('*'|'/'|'%') expression
	| expression ('+'|'-') expression
	| expression ('<='|'>='|'>'|'<') expression // Not yet
	| expression ('=='|'!='|'is') expression
    | expression
		( '='
		| '+='
		| '-='
		| '*='
		| '/='
		| '%='
		) expression
	| expression // Not yet
		( '&&'
		| '||'
		| 'and'
		| 'or'
		) expression
	| ('++'|'--') expression
	| ('!'|'not') expression //Not yet
	| 'not' expression //Not yet
	;

/*
	| '&'
	| '^'
	| '|'
	| '&='
	| '|='
	| '^='
*/


unit
	: '{' unitSingleOrPairOperator '}'
	;

unitSingleOrPairOperator
	: '@'? unitOperator
	| '@'? unitOperator '/' unitOperator
	;

unitOperator
	: Identifier
	| Identifier '->' Identifier
	;

primary
	: Identifier unit?
	| literal unit?
	| '(' expression ')' unit?
	| '[' expression? (',' expression)* ']' unit?
	;

literal
	: number
    | string
    | boolean
    | none
    ;


string
	: STRING_LITERAL
	| BYTES_LITERAL
	;

number
	: integer
	| FLOAT_NUMBER
	| IMAG_NUMBER
	;


/*
newlines
	: newlines NEWLINE
	| NEWLINE
	;
*/

/// integer        ::=  decimalinteger | octinteger | hexinteger | bininteger
integer
	 : DECIMAL_INTEGER
	 | OCT_INTEGER
	 | HEX_INTEGER
	 | BIN_INTEGER
	 ;

// Boolean Literals
boolean
    :   'true'
    |   'false'
    ;

// The Null Literal
none
	:   'NULL'
	;

/*
 * LEXER from here.
 */

// Keywords
DEF             : 'def';
REP             : 'rep';
PRINT           : 'print';
IF              : 'if';
RETURN          : 'return';
BREAK           : 'break';
CONTINUE        : 'continue';
LPAREN          : '(';
RPAREN          : ')';
LBRACE          : '{';
RBRACE          : '}';
LBRACK          : '[';
RBRACK          : ']';
SEMICOLON       : ';';
COMMA           : ',';
DOT             : '.';

// Operators
THREE_BORDER    : '---';
FOUR_BORDER     : '----';
FIVE_BORDER     : '-----';
SIX_BORDER      : '------';
SEVEN_BORDER    : '-------';
EIGHT_BORDER    : '--------';
NINE_BORDER     : '---------';
TEN_BORDER      : '----------';
ASSIGN          : '=';
GT              : '>';
LT              : '<';
BANG            : '!';
BANG_X          : 'not';
TILDE           : '~';
QUESTION        : '?';
COLON           : ':';
EQUAL           : '==';
EQUAL_X         : 'is';
LE              : '<=';
GE              : '>=';
ALLOW           : '->';
NOTEQUAL        : '!=';
AND             : '&&';
OR              : '||';
AND_X           : 'and';
OR_X            : 'or';
INC             : '++';
DEC             : '--';
ADD             : '+';
SUB             : '-';
MUL             : '*';
DIV             : '/';
BITAND          : '&';
BITOR           : '|';
CARET           : '^';
MOD             : '%';

ADD_ASSIGN      : '+=';
SUB_ASSIGN      : '-=';
MUL_ASSIGN      : '*=';
DIV_ASSIGN      : '/=';
AND_ASSIGN      : '&=';
OR_ASSIGN       : '|=';
XOR_ASSIGN      : '^=';
MOD_ASSIGN      : '%=';

AT              : '@';
//NEWLINE      : '\n';



/// stringliteral   ::=  [stringprefix](shortstring | longstring)
/// stringprefix    ::=  "r" | "R"
STRING_LITERAL
	: ( SHORT_STRING | LONG_STRING )
	;
// without [uU]? [rR]? now

/// bytesliteral   ::=  bytesprefix(shortbytes | longbytes)
/// bytesprefix    ::=  "b" | "B" | "br" | "Br" | "bR" | "BR"
BYTES_LITERAL
	: ( SHORT_BYTES | LONG_BYTES )
	;
// without [bB] [rR]? now

/// decimalinteger ::=  nonzerodigit digit* | "0"+
DECIMAL_INTEGER
	: NON_ZERO_DIGIT DIGIT*
	| '0'+
	;

/// octinteger     ::=  "0" ("o" | "O") octdigit+
OCT_INTEGER
	: '0' [oO] OCT_DIGIT+
	;

/// hexinteger     ::=  "0" ("x" | "X") hexdigit+
HEX_INTEGER
	: '0' [xX] HEX_DIGIT+
	;

/// bininteger     ::=  "0" ("b" | "B") bindigit+
BIN_INTEGER
	: '0' [bB] BIN_DIGIT+
	;

/// floatnumber   ::=  pointfloat | exponentfloat
FLOAT_NUMBER
	: POINT_FLOAT
	| EXPONENT_FLOAT
	;

/// imagnumber ::=  (floatnumber | intpart) ("j" | "J")
IMAG_NUMBER
	: ( FLOAT_NUMBER | INT_PART ) [jJ]
	;


/*
 * fragment
 */

fragment
SHORT_STRING
	: '\'' ( STRING_ESCAPE_SEQ | ~[\\\r\n'] )* '\''
	| '"' ( STRING_ESCAPE_SEQ | ~[\\\r\n"] )* '"'
	;
fragment
LONG_STRING
	: '\'\'\'' LONG_STRING_ITEM*? '\'\'\''
	| '"""' LONG_STRING_ITEM*? '"""'
	;

fragment
LONG_STRING_ITEM
	: LONG_STRING_CHAR
	| STRING_ESCAPE_SEQ
	;

fragment
LONG_STRING_CHAR
	: ~'\\'
	;

fragment
STRING_ESCAPE_SEQ
	: '\\' .
	;

fragment
NON_ZERO_DIGIT
	: [1-9]
	;

fragment
DIGIT
	: [0-9]
	;

fragment
OCT_DIGIT
	: [0-7]
	;

fragment
HEX_DIGIT
	: [0-9a-fA-F]
	;

fragment
BIN_DIGIT
	: [01]
	;

fragment
POINT_FLOAT
	: INT_PART? FRACTION
	| INT_PART '.'
	;

fragment
EXPONENT_FLOAT
	: ( INT_PART | POINT_FLOAT ) EXPONENT
	;

fragment
INT_PART
	: DIGIT+
	;

fragment
FRACTION
	: '.' DIGIT+
	;

fragment
EXPONENT
	: [eE] [+-]? DIGIT+
	;

fragment
SHORT_BYTES
	: '\'' ( SHORT_BYTES_CHAR_NO_SINGLE_QUOTE | BYTES_ESCAPE_SEQ )* '\''
	| '"' ( SHORT_BYTES_CHAR_NO_DOUBLE_QUOTE | BYTES_ESCAPE_SEQ )* '"'
	;

fragment
LONG_BYTES
	: '\'\'\'' LONG_BYTES_ITEM*? '\'\'\''
	| '"""' LONG_BYTES_ITEM*? '"""'
	;

fragment
LONG_BYTES_ITEM
	: LONG_BYTES_CHAR
	| BYTES_ESCAPE_SEQ
	;

/// shortbyteschar ::=  <any ASCII character except "\" or newline or the quote>
fragment
SHORT_BYTES_CHAR_NO_SINGLE_QUOTE
	: [\u0000-\u0009]
	| [\u000B-\u000C]
	| [\u000E-\u0026]
	| [\u0028-\u005B]
	| [\u005D-\u007F]
	; 
fragment
SHORT_BYTES_CHAR_NO_DOUBLE_QUOTE
	: [\u0000-\u0009]
	| [\u000B-\u000C]
	| [\u000E-\u0021]
	| [\u0023-\u005B]
	| [\u005D-\u007F]
	; 
/// longbyteschar  ::=  <any ASCII character except "\">
fragment
LONG_BYTES_CHAR
	: [\u0000-\u005B]
	| [\u005D-\u007F]
	;
/// bytesescapeseq ::=  "\" <any ASCII character>
fragment
BYTES_ESCAPE_SEQ
	: '\\' [\u0000-\u007F]
	;



// Identifiers (must appear after all keywords in the grammar)
Identifier
	:   UnitXLetter UnitXLetterOrDigit*
    ;

fragment
UnitXLetter
    :   [a-zA-Z$_] // these are the "java letters" below 0xFF
    |   // covers all characters above 0xFF which are not a surrogate
        ~[\u0000-\u00FF\uD800-\uDBFF]
    |   // covers UTF-16 surrogate pairs encodings for U+10000 to U+10FFFF
        [\uD800-\uDBFF] [\uDC00-\uDFFF]
    ;

fragment
UnitXLetterOrDigit
    :   [a-zA-Z0-9$_] // these are the "java letters or digits" below 0xFF
    |   // covers all characters above 0xFF which are not a surrogate
        ~[\u0000-\u00FF\uD800-\uDBFF]
    |   // covers UTF-16 surrogate pairs encodings for U+10000 to U+10FFFF
        [\uD800-\uDBFF] [\uDC00-\uDFFF]
    ;


// Whitespace and comments
NEWLINE
	: '\n' -> skip
	;

WS  : [ \t\r\u000C]+ -> skip
    ;

COMMENT
    :   '/*'
		('\n'|.)*? 
		'*/' -> skip
    ;

LINE_COMMENT
    : '#' ~[\r\n]* -> skip
	;

C_LINE_COMMENT
	: '//' ~[\r\n]* -> skip
    ;
