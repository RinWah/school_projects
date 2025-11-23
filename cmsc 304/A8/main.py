from enum import Enum, auto #import enum class that allows python enum properties, built in
from dataclasses import dataclass #idk what this is tbh

class TokenType(Enum): #make enum stuff, but idk why all of them are auto
    LEFT_PARENTHESIS = auto()
    RIGHT_PARENTHESIS = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    WHILE_KEYWORD = auto()
    RETURN_KEYWORD = auto()
    EQUAL = auto()
    COMMA = auto()
    EOL = auto()
    VARTYPE = auto()
    IDENTIFIER = auto()
    BINOP = auto()
    NUMBER = auto()

@dataclass
class Lex: #is this like saying hey all my tokens are going to be token type and all my lexemes are going to be str? also what are
# lexemes again? words? 
    token: TokenType
    lexeme: str
