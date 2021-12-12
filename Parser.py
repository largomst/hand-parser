import Lexer
import sys

class Parser:
    def __init__(self,input: Lexer.Lexer):
        self.input = input
        self.lookhead = input.get_next_token()
    def match(self, x):
        if self.lookhead.type_ == x:
            self.consume()
        else:
            raise Exception(f"expceting {self.input.get_token_name(x)} + ';' found {self.lookhead}")

    def consume(self):
        self.lookhead = self.input.get_next_token()
        
class ListParser(Parser):
    def __init__(self, input):
        super().__init__(input)
    
    def list_(self):
        self.match(Lexer.LBRACK)
        self.elements()
        self.match(Lexer.RBRACK)
    
    def elements(self):
        self.element()
        while self.lookhead.type_ == Lexer.COMMA:
            self.match(Lexer.COMMA)
            self.element()
        
    def element(self):
        if self.lookhead.type_ == Lexer.NAME:
            self.match(Lexer.NAME)
        elif self.lookhead.type_ == Lexer.LBRACK:
            self.list_()
        else:
            raise Exception(f"excepting name or list; found {self.lookhead}")

if __name__ == '__main__':
    lexer = Lexer.ListLexer(sys.argv[1])
    parser = ListParser(lexer)
    parser.list_()
    


