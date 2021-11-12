# Name: Ryan Menow
# Date: 12/06/2020
# Course: CSCI 330 - Programming Languages
# Professor: William Killian
# Assignment: MU Calculator
# Description: Implement a calculator using Python!
#              This includes implementing the lexical analyszer, expression parser and evalutor.

import ply.lex as lex
import ply.yacc as yacc
from calclex import tokens
import sys

#=====================Lexical Analyser==============================

# List of tokens
tokens = [
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDES',
    'POWER',
    'LPAREN',
    'RPAREN',
    'NUMBER',
    'PI',
    'E',
]

# Rules for tokens
t_PLUS    = r'\+'
t_MINUS   = r'\-'
t_TIMES   = r'\*'
t_DIVIDES = r'\/'
t_POWER   = r'\^'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# Ignore whitespace
t_ignore = r' '

# Define what NUMBER is
def t_NUMBER(t):
    r'\d+(\.\d*)?'
    t.value = float(t.value)
    return t

# Define what PI is
def t_PI(t):
    r'[p][i]'
    t.value = 3.14159265358979
    return t

# Define what E is
def t_E(t):
    r'[e]'
    t.value = 2.71828182845904
    return t

# Error for illegal characters
def t_error(t):
    print("You have an illegal character(s)!")
    t.lexer.skip(1)

# Creates lexer
lexer = lex.lex()

#=====================Expression Parser & Evaluator=============================

# Sets precedence for operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDES'),
    ('right', 'POWER'),
)

# Displays solution to calculation
def p_calc(p):
    '''
    calc : Exp
         | empty
    '''
    print(run(p[1]))

# Calculates the given expression(s)
def run(p):
    # If p is a tuple compute the appropriate calculation
    if type(p) == tuple:
        # Calculation for addition
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        # Calculation for subtraction
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        # Calculation for multiplication
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        # Calculation for division
        elif p[0] == '/':
            return run(p[1]) / run(p[2])
        # Calculation for exponation
        elif p[0] == '^':
            return run(p[1]) ** run(p[2])
    # If p is not a tuple, then return p
    else:
        return p

# Handles Expression grammars and sets up AST using tuples
def p_exp(p):
    '''
    Exp : Exp PLUS Exp
        | Exp MINUS Exp
        | Exp TIMES Exp
        | Exp DIVIDES Exp
        | Exp POWER Exp
    '''
    p[0] = (p[2], p[1], p[3])

def p_exp_term(p):
    '''
    Exp : Term
    '''
    p[0] = p[1]

# Handles Term grammars
def p_term_paren(p):
    '''
    Term : LPAREN Exp RPAREN
    '''
    p[0] = p[2]

def p_term_num(p):
    '''
    Term : Num
    '''
    p[0] = p[1]

# Handles Num grammars
def p_num(p):
    '''
    Num : NUMBER
        | PI
        | E
    '''
    p[0] = p[1]

# Handles empty input
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

# Handles Syntax error
def p_error(p):
    print("There is a syntax error in your input!")

# Creates parser
parser = yacc.yacc()

# Allows user to give input to the parser
while True:
    try:
        s = input('>>> ')
    except EOFError:
        break
    parser.parse(s)