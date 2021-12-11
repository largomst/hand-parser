import logging
import sys

EOF = -1
EOF_TYPE = 1
NAME =2
COMMA = 3
LBRACK = 4
RBRACK = 5

TokensNames = [
    'n/a','<EOF>','NAME','COMMA','LBRACK','RBRACK'
]

class AbstractLexer:
    def get_next_token(self):
        pass
    def get_token_name(self, token_type):
        pass

class Lexer:
    def __init__(self, text):
        self.input = text
        self.pos = 0
        self.current_char = self.input[self.pos]
    def consume(self):
        self.pos += 1
        if self.pos >= len(self.input) :
            self.current_char = EOF
        else:
            self.current_char = self.input[self.pos]

    def match(self, char):
        if self.current_char == char:
            self.consume()
        else:
            raise Exception('expect {} but get {}'.format(char, self.current_char))
    
class ListLexer(Lexer, AbstractLexer):
    def __init__(self, text):
        super().__init__(text)
    
    def get_next_token(self):
        while self.current_char != EOF:
            if self.current_char in [' ' ,'\n' ,'\t' , '\r']:
                self.WS()
                self.consume()
            elif self.current_char == ',':
                self.consume()
                return Token(COMMA, ',')
            elif self.current_char == '[':
                self.consume()
                return Token(LBRACK, '[')
            elif self.current_char == ']':
                self.consume()
                return Token(RBRACK, ']')
            else:
                if self.isLetter():
                    return self.NAME()
                else:
                    raise Exception("invalid character: "  + self.current_char + '\n')
                    os.exit(1)
        return Token(EOF_TYPE,EOF)
    

    def isLetter(self):
        return self.current_char.isalpha()
    
    def NAME(self):
        buf = []
        while True:
            buf.append(self.current_char)
            self.consume()
            if self.isLetter():
                continue
            else:
                break
        return Token(NAME, ''.join(buf))

    def WS(self):
        while self.current_char in [' ' ,'\n' ,'\t' , '\r']:
            self.consume()       
    
    def get_token_name(self, token_type):
        return TokensNames[token_type]


class Token:
    def __init__(self, type, text):
        self.type = type
        self.text = text

    def __str__(self):
        tname = TokensNames[self.type]
        return "<" + self.text + "," + tname + ">"

    

if __name__ == "__main__":
    lexer = ListLexer(sys.argv[1])
    token = lexer.get_next_token()
    while token.type != EOF_TYPE:
        print(token)
        token = lexer.get_next_token()
