package main

import (
	"fmt"
	"os"
	"strings"
)

const EOF = string(-1)
const EOF_TYPE = 1
const NAME = 2
const COMMA = 3
const LBRACK = 4
const RBRACK = 5

var TokenNames = []string{"n/a", "<EOF>", "NAME", "COMMA", "LBRACK", "RBRACK"}

type Lexer struct {
	input string
	p     int
	c     string
}

func NewLexer(input string) *Lexer {
	c := string(input[0])
	return &Lexer{input, 0, c}
}

func (l *Lexer) consume() {
	l.p += 1
	if l.p >= len(l.input) {
		l.c = EOF
	} else {
		l.c = string(l.input[l.p])
	}
}
func (l *Lexer) match(x string) error {
	if l.c == x {
		l.consume()
		return nil
	} else {
		return fmt.Errorf("expecting " + x + "; found " + l.c)
	}
}

type BaseLexer interface {
	NextToken() Token
	GetTokenName() string
}

type ListLexer struct {
	Lexer
}

func (l *ListLexer) NextToken() *Token {
	for l.c != EOF {
		switch l.c {
		case " ":
			fallthrough
		case "\t":
			fallthrough
		case "\n":
			fallthrough
		case "\r":
			l.WS()
			continue
		case ",":
			l.consume()
			return NewToken(COMMA, ",")
		case "[":
			l.consume()
			return NewToken(LBRACK, "[")
		case "]":
			l.consume()
			return NewToken(RBRACK, "]")
		default:
			if l.isLETTER() {
				return l.NAME()
			} else {
				fmt.Printf("invalid character: " + l.c + "\n")
				os.Exit(0)
			}
		}
	}
	return NewToken(EOF_TYPE, EOF)
}

func (l *ListLexer) NAME() *Token {
	buf := []string{}
	for {
		buf = append(buf, l.c)
		l.consume()
		if l.isLETTER() {
			continue
		} else {
			break
		}
	}
	return NewToken(NAME, strings.Join(buf, ""))
}
func (l *ListLexer) WS() {
	for l.c == " " || l.c == "\t" || l.c == "\n" || l.c == "\r" {
		l.consume()
	}
}
func (l *ListLexer) isLETTER() bool {
	return l.c >= "a" && l.c <= "z" || l.c >= "A" && l.c <= "Z"
}
func (l *ListLexer) GetTokenName(x int) string {
	return TokenNames[x]

}

type Token struct {
	type_ int
	text  string
}

func NewToken(type_ int, text string) *Token {
	return &Token{type_, text}
}
func (t *Token) String() string {
	tname := TokenNames[t.type_]
	return "<" + t.text + "," + tname + ">"
}
func NewListLexer(input string) *ListLexer {
	lexer := NewLexer(input)
	return &ListLexer{Lexer: *lexer}
}
func main() {
	lexer := NewListLexer(os.Args[1])
	t := lexer.NextToken()
	for t.type_ != EOF_TYPE {
		fmt.Println(t)
		t = lexer.NextToken()
	}
}
