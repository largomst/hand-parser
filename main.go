package main

import "fmt"

var tokens = []string{"return", "x", "+", "1", ";"}
var current int = 0

func stat() {
	returnstat()
}
func returnstat() {
	match("return")
	expr()
	match(";")
}
func expr() {
	match("x")
	match("+")
	match("1")
}

func match(s string) {
	if tokens[current] == s {
		fmt.Printf("Match %s\n", tokens[current])
		current++
	} else {
		fmt.Printf("Error at %d\n", current)
	}
}

func main() {
	stat()
}
