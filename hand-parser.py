import sys

EOF = -1
EOF_TYPE = 1
NAME = 2
COMMA = 3
LBRACK = 4
RBRACK = 5

TOKEN_NAMES = [
    'n/a', '<EOF>',"NAME",'COMMAN','LBRACK','RBRACK'
]
class Token:
    def __init__(self, type_:int, text:str):
        self.type_ = type_
        self.text = text
    
    def __str__(self):
        tname = TOKEN_NAMES[self.type_]
        return f"<{self.text},{tname}>"

class Lexer:
    def __init__(self, text:str):
        self.input = text
        self.p = 0
        self.c = self.input[self.p]

    def consume(self):
        self.p += 1
        if len(self.input) <= self.p:
            self.c = EOF
        else:
            self.c = self.input[self.p]


    def get_token_name(self, type_):
        return TOKEN_NAMES[type_]
    
    def get_next_token(self):
        pass
class ListLexer(Lexer):
    def __init__(self, text):
        super().__init__(text)

    def get_next_token(self):
        while self.c != EOF:
            if self.c in ' \n\t\r':
                # skip ws
                self.WS()
                # continue
            elif self.c == ',':
                self.consume()
                return Token(COMMA, ",")
            elif self.c == '[':
                self.consume()
                return Token(LBRACK, "[")
            elif self.c == ']':
                self.consume()
                return Token(RBRACK, "]")
            else:
                if self.isLetter():
                    return self.NAME()
                else:
                    raise Exception("invalid characer: ", self.c)
        return Token(EOF_TYPE,EOF)



    def isLetter(self):
        return self.c.isalpha()

    def WS(self):
        while self.c in ' \t\n\r':
            self.consume()
        
    def NAME(self):
        buf = []
        while True:
            buf.append(self.c)
            self.consume()
            if self.isLetter():
                continue
            else:
                break
        return Token(NAME, ''.join(buf))
            
if __name__ == '__main__':
    lexer = ListLexer(sys.argv[1])
    token = lexer.get_next_token()
    while token.type_ != EOF_TYPE:
        print(token)
        token = lexer.get_next_token()
