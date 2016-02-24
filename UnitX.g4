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
 * 【UnitX's grammar】
 * This grammar can be a parser of UnitX by using ANTLR4.
 * And, ANTLR4 is a parser generator by Java.
 * So, you need the Java lang. And also, you can use it like below.
 * 
 *     java -jar antlr-4.5.1-complete.jar UnitX.g4 
 * 
 * Anyway, see "http://www.antlr.org/" for the details! if you wanna change this grammar.
 */
grammar UnitX;

/*
 * Parser from Here.
 *
 * A starting point of Parser RULE is 'program'.
 * memo: If someone or future I could add RULES of import statement or name space, add the RULES to a 'program' RULE.
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
    : '(' formalParameterList? ')'
    ;

formalParameterList
    : formalParameter (',' formalParameter)* 
    ;

formalParameter
    :  Identifier ('=' expression)?
    ;

statement
	: block
	| 'loop' '(' forControl ')' statement
	| 'if' parExpression statement ('else' statement)?
	| 'print' expression
	| 'return' expression
	| 'break'
	| 'continue'
	| borderPrinter
	| '@'? expression
	;

borderPrinter
	: '---' '-'*
	;

block
    : '{' blockStatement* '}'
    ;

blockStatement
    : statement
    ;

expressionList
    :   expression (',' expression)*
    ;

parExpression
	: '(' expression ')'
	;

forControl
	: Identifier ',' endFor
	;

endFor
	: IntegerLiteral
	| collection
	;

collection
	: '[' expression? (',' expression)* ']'
	;

expression
	: primary
	| expression ('*'|'/') expression
	| expression ('+'|'-') expression
	| expression ('++' | '--')
	| expression '(' expressionList ')'
    | expression ('='|'+='|'-='|'*='|'/='|'%=') expression
	| ('++'|'--') expression
	;

unit
	: '{' unitSingleOrPairOperator '}'
	;

unitSingleOrPairOperator
	: unitOperator? '/' unitOperator?
	| unitOperator
	;

unitOperator
	: Identifier
	| Identifier '->' Identifier
	| '->' Identifier
	;

primary
	: Identifier unit?
	| literal unit?
    | '(' expression ')' unit?
	;

literal
    : IntegerLiteral
    | FloatingPointLiteral
    | StringLiteral
    | BooleanLiteral
    | ImageLiteral
    | 'null'
    ;


/*
 * LEXER from here.
 */

// Keywords
DEF           	: 'def';
LOOP           	: 'loop';
PRINT         	: 'print';
IF          	: 'if';
RETURN          : 'return';
BREAK           : 'break';
CONTINUE      	: 'continue';
LPAREN          : '(';
RPAREN          : ')';
LBRACE          : '{';
RBRACE          : '}';
LBRACK          : '[';
RBRACK          : ']';
SEMI            : ';';
COMMA           : ',';
DOT             : '.';

// Operators
TREE_BORDER		: '---';
ASSIGN          : '=';
GT              : '>';
LT              : '<';
BANG            : '!';
TILDE           : '~';
QUESTION        : '?';
COLON           : ':';
EQUAL           : '==';
LE              : '<=';
GE              : '>=';
ALLOW			: '->';
NOTEQUAL        : '!=';
AND             : '&&';
OR              : '||';
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

AT				: '@';
//NEWLINE			: '\n';


// Integer Literals

ImageLiteral
    : ( FloatingPointLiteral |  ) [jJ]
    ;

IntegerLiteral
    :   DecimalIntegerLiteral
    |   HexIntegerLiteral
    |   OctalIntegerLiteral
    |   BinaryIntegerLiteral
    ;

fragment
DecimalIntegerLiteral
    :   DecimalNumeral IntegerTypeSuffix?
    ;

fragment
HexIntegerLiteral
    :   HexNumeral IntegerTypeSuffix?
    ;

fragment
OctalIntegerLiteral
    :   OctalNumeral IntegerTypeSuffix?
    ;

fragment
BinaryIntegerLiteral
    :   BinaryNumeral IntegerTypeSuffix?
    ;

fragment
IntegerTypeSuffix
    :   [lL]
    ;

fragment
DecimalNumeral
    :   '0'
    |   NonZeroDigit (Digits? | Underscores Digits)
    ;

fragment
Digits
    :   Digit (DigitOrUnderscore* Digit)?
    ;

fragment
Digit
    :   '0'
    |   NonZeroDigit
    ;

fragment
NonZeroDigit
    :   [1-9]
    ;

fragment
DigitOrUnderscore
    :   Digit
    |   '_'
    ;

fragment
Underscores
    :   '_'+
    ;

fragment
HexNumeral
    :   '0' [xX] HexDigits
    ;

fragment
HexDigits
    :   HexDigit (HexDigitOrUnderscore* HexDigit)?
    ;

fragment
HexDigit
    :   [0-9a-fA-F]
    ;

fragment
HexDigitOrUnderscore
    :   HexDigit
    |   '_'
    ;

fragment
OctalNumeral
    :   '0' Underscores? OctalDigits
    ;

fragment
OctalDigits
    :   OctalDigit (OctalDigitOrUnderscore* OctalDigit)?
    ;

fragment
OctalDigit
    :   [0-7]
    ;

fragment
OctalDigitOrUnderscore
    :   OctalDigit
    |   '_'
    ;

fragment
BinaryNumeral
    :   '0' [bB] BinaryDigits
    ;

fragment
BinaryDigits
    :   BinaryDigit (BinaryDigitOrUnderscore* BinaryDigit)?
    ;

fragment
BinaryDigit
    :   [01]
    ;

fragment
BinaryDigitOrUnderscore
    :   BinaryDigit
    |   '_'
    ;

// Floating-Point Literals

FloatingPointLiteral
    :   DecimalFloatingPointLiteral
    |   HexadecimalFloatingPointLiteral
    ;

fragment
DecimalFloatingPointLiteral
    :   Digits '.' Digits? ExponentPart? FloatTypeSuffix?
    |   '.' Digits ExponentPart? FloatTypeSuffix?
    |   Digits ExponentPart FloatTypeSuffix?
    |   Digits FloatTypeSuffix
    ;

fragment
ExponentPart
    :   ExponentIndicator SignedInteger
    ;

fragment
ExponentIndicator
    :   [eE]
    ;

fragment
SignedInteger
    :   Sign? Digits
    ;

fragment
Sign
    :   [+-]
    ;

fragment
FloatTypeSuffix
    :   [fFdD]
    ;

fragment
HexadecimalFloatingPointLiteral
    :   HexSignificand BinaryExponent FloatTypeSuffix?
    ;

fragment
HexSignificand
    :   HexNumeral '.'?
    |   '0' [xX] HexDigits? '.' HexDigits
    ;

fragment
BinaryExponent
    :   BinaryExponentIndicator SignedInteger
    ;

fragment
BinaryExponentIndicator
    :   [pP]
    ;

// Boolean Literals

BooleanLiteral
    :   'true'
    |   'false'
    ;

// String Literals

StringLiteral
    :   '"' StringCharacters? '"'
    |   '\'' StringCharacters? '\''
    ;

fragment
StringCharacters
    :   StringCharacter+
    ;

fragment
StringCharacter
    :   ~["\\]
    |   EscapeSequence
    ;

// Escape Sequences for Character and String Literals

fragment
EscapeSequence
    :   '\\' [btnfr"'\\]
    |   OctalEscape
    |   UnicodeEscape
    ;

fragment
OctalEscape
    :   '\\' OctalDigit
    |   '\\' OctalDigit OctalDigit
    |   '\\' ZeroToThree OctalDigit OctalDigit
    ;

fragment
UnicodeEscape
    :   '\\' 'u' HexDigit HexDigit HexDigit HexDigit
    ;

fragment
ZeroToThree
    :   [0-3]
    ;

// The Null Literal

NullLiteral
    :   'null'
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
	:  ['\n']+ -> skip
    ;

WS  :  [ \t\r\u000C]+ -> skip
    ;

COMMENT
    :   '/*'
		('\n'|.)*? 
		'*/' -> skip
    ;

LINE_COMMENT
    :   '#' ~[\r\n]* -> skip
    ;
