from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Iterator


class TokenKind(enum.Enum):
    """Classe já implementada: nomes e números não devem ser alterados."""

    EOF = -1

    IDENTIFIER = 1
    INT_LITERAL = 2
    STRING_LITERAL = 3

    KW_INT = 10
    KW_BOOL = 11
    KW_VOID = 12
    KW_TRUE = 13
    KW_FALSE = 14
    KW_IF = 15
    KW_ELSE = 16
    KW_WHILE = 17
    KW_RETURN = 18
    KW_PRINT = 19

    PLUS = 20
    MINUS = 21
    STAR = 22
    SLASH = 23
    PERCENT = 24
    LESS = 25
    LESS_EQUAL = 26
    GREATER = 27
    GREATER_EQUAL = 28
    EQUAL_EQUAL = 29
    NOT_EQUAL = 30
    LOGICAL_AND = 31
    LOGICAL_OR = 32
    LOGICAL_NOT = 33
    ASSIGN = 34

    LEFT_PAREN = 40
    RIGHT_PAREN = 41
    LEFT_BRACE = 42
    RIGHT_BRACE = 43
    COMMA = 44
    SEMICOLON = 45


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    lexeme: str
    value: int | str | bool | None
    line: int
    column: int

    def __str__(self) -> str:
        return (
            f"<{self.kind.value}, {self.kind.name}, {self.lexeme!r}, "
            f"{self.value!r}, {self.line}, {self.column}>"
        )


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"erro léxico em {self.line}:{self.column}: {self.message}"


class Lexer:
    """Converte texto-fonte MicroC em uma sequência de tokens."""

    def __init__(self, source: str):
        self.source = source

    def tokens(self) -> Iterator[Token]:
        """Produza todos os tokens significativos e um único EOF ao final."""
        tokens = []
        current_lexeme = ""
        line = 1
        column = 1
        
        i = 0
        while i < len(self.source):
            char = self.source[i]
            #print("i: " + str(i) + "repr" + repr(char))
            if char.isspace(): # Ignorar espaços em branco
                if char == '\n':
                    line += 1
                    column = 1
                i += 1
            else:
                if char in ['(', ')', '{', '}', ',', ';', '+', '-', '*', '%']: # Tokens de um caractere
                    if char == '(':
                        tokens.append(Token(TokenKind.LEFT_PAREN, char, None, line, column))
                    elif char == ')':
                        tokens.append(Token(TokenKind.RIGHT_PAREN, char, None, line, column))
                    elif char == '{':
                        tokens.append(Token(TokenKind.LEFT_BRACE, char, None, line, column))
                    elif char == '}':
                        tokens.append(Token(TokenKind.RIGHT_BRACE, char, None, line, column))
                    elif char == ',':
                        tokens.append(Token(TokenKind.COMMA, char, None, line, column))
                    elif char == ';':
                        tokens.append(Token(TokenKind.SEMICOLON, char, None, line, column))
                    elif char == '+':
                        tokens.append(Token(TokenKind.PLUS, char, None, line, column))
                    elif char == '-':
                        tokens.append(Token(TokenKind.MINUS, char, None, line, column))
                    elif char == '*':
                        tokens.append(Token(TokenKind.STAR, char, None, line, column))
                    elif char == '%':
                        tokens.append(Token(TokenKind.PERCENT, char, None, line, column))
                    i += 1
                elif char.isdigit(): # Literais inteiros
                    while i < len(self.source) and self.source[i].isdigit():
                        current_lexeme += self.source[i]
                        i += 1
                    tokens.append(Token(TokenKind.INT_LITERAL, current_lexeme, int(current_lexeme), line, column))
                elif char == '"': # Literais de string
                    i += 1
                    while i < len(self.source) and self.source[i] != '"' or (self.source[i] == '"' and self.source[i - 1] == '\\'):
                        current_lexeme += self.source[i]
                        i += 1
                    if i < len(self.source) and self.source[i] == '"':
                        tokens.append(Token(TokenKind.STRING_LITERAL, current_lexeme, current_lexeme, line, column))
                    i += 1
                elif char.isalpha() or char == '_': # Identificadores ou keywords
                    while i < len(self.source) and (self.source[i].isalnum() or self.source[i] == '_'):
                        current_lexeme += self.source[i]
                        i += 1
                    if current_lexeme in ['int', 'bool', 'void', 'if', 'else', 'while', 'return', 'print']:
                        tokens.append(Token(TokenKind[f'KW_{current_lexeme.upper()}'], current_lexeme, None, line, column))
                    elif current_lexeme in ['true']:
                        tokens.append(Token(TokenKind[f'KW_{current_lexeme.upper()}'], current_lexeme, True, line, column))
                    elif current_lexeme in ['false']:
                        tokens.append(Token(TokenKind[f'KW_{current_lexeme.upper()}'], current_lexeme, False, line, column))
                    else:
                        tokens.append(Token(TokenKind.IDENTIFIER, current_lexeme, current_lexeme, line, column))
                elif char in ['<', '>', '=', '!', '&', '|']: # Operadores compostos
                    if i + 1 < len(self.source):
                        next_char = self.source[i + 1]
                        if char == '<' and next_char == '=':
                            tokens.append(Token(TokenKind.LESS_EQUAL, '<=', None, line, column))
                            i += 1
                        elif char == '>' and next_char == '=':
                            tokens.append(Token(TokenKind.GREATER_EQUAL, '>=', None, line, column))
                            i += 1
                        elif char == '=' and next_char == '=':
                            tokens.append(Token(TokenKind.EQUAL_EQUAL, '==', None, line, column))
                            i += 1
                        elif char == '!' and next_char == '=':
                            tokens.append(Token(TokenKind.NOT_EQUAL, '!=', None, line, column))
                            i += 1
                        elif char == '&' and next_char == '&':
                            tokens.append(Token(TokenKind.LOGICAL_AND, '&&', None, line, column))
                            i += 1
                        elif char == '|' and next_char == '|':
                            tokens.append(Token(TokenKind.LOGICAL_OR, '||', None, line, column))
                            i += 1
                        else:
                            if char == '<':
                                tokens.append(Token(TokenKind.LESS, '<', None, line, column))
                            elif char == '>':
                                tokens.append(Token(TokenKind.GREATER, '>', None, line, column))
                            elif char == '=':
                                tokens.append(Token(TokenKind.ASSIGN, '=', None, line, column))
                            elif char == '!':
                                tokens.append(Token(TokenKind.LOGICAL_NOT, '!', None, line, column))
                    else:
                        if char == '<':
                            tokens.append(Token(TokenKind.LESS, '<', None, line, column))
                        elif char == '>':
                            tokens.append(Token(TokenKind.GREATER, '>', None, line, column))
                        elif char == '=':
                            tokens.append(Token(TokenKind.ASSIGN, '=', None, line, column))
                        elif char == '!':
                            tokens.append(Token(TokenKind.LOGICAL_NOT, '!', None, line, column))
                    i += 1
                elif char == '/': # Comentários ou operador de divisão
                    if i + 1 < len(self.source):
                        next_char = self.source[i + 1]
                        if next_char == '/': # Comentário de linha
                            while i < len(self.source) and self.source[i] != '\n':
                                i += 1
                        elif next_char == '*': # Comentário de bloco
                            i += 2
                            while i + 1 < len(self.source) and not (self.source[i] == '*' and self.source[i + 1] == '/'):
                                if (self.source[i] == '\n'):
                                    line += 1
                                i += 1
                            if i + 1 < len(self.source):
                                i += 2
                    else:
                        tokens.append(Token(TokenKind.SLASH, '/', None, line, column))
            
            column += 1
            current_lexeme = ""

        tokens.append(Token(TokenKind.EOF, "", None, line, column))
        
        return tokens

    def scan(self) -> list[Token]:
        return list(self.tokens())

