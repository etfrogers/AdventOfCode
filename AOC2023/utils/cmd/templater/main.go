package main

import (
	"fmt"
	"os"
	"utils"
)

var package_line_temp string = "package day%s\n"

func main() {
	args := os.Args
	if len(args) != 2 {
		fmt.Println("templater takes exactly one argument: the day number")
		return
	}
	day := args[1]
	fmt.Printf("templater creating files for day %s\n", day)
	os.Chdir("../../..")
	wd, err := os.Getwd()
	utils.Check(err)
	fmt.Printf("%v\n", wd)

	dirname := "day" + day
	fname := dirname + ".go"
	test_name := dirname + "_test.go"
	os.Mkdir(dirname, 0777)

	modCode := fmt.Sprintf(modText, day)
	mainCode := fmt.Sprintf(mainText, day, "%d")

	err = os.WriteFile(dirname+string(os.PathSeparator)+fname, []byte(mainCode), 0644)
	utils.Check(err)

	err = os.WriteFile(dirname+string(os.PathSeparator)+test_name, []byte(testText), 0644)
	utils.Check(err)

	err = os.WriteFile(dirname+string(os.PathSeparator)+"go.mod", []byte(modCode), 0644)
	utils.Check(err)

	err = os.WriteFile(dirname+string(os.PathSeparator)+"input.txt", []byte(""), 0644)
	utils.Check(err)

}

const mainText string = `package main

import (
	"fmt"
	"utils"
)

func main() {
	lines := utils.ReadInput()
	fmt.Println(lines)
	part1Answer := 0
	fmt.Printf("Day %s, Part 1 answer: %s\n", part1Answer)
}
`

const testText string = `package main

import "strings"

var testCase string = ` + "`...`" + `

var testLines []string = strings.Split(testCase, "\n")

`

const modText string = `module day%s

go 1.21

require github.com/stretchr/testify v1.8.4

require (
	github.com/davecgh/go-spew v1.1.1 // indirect
	github.com/pmezard/go-difflib v1.0.0 // indirect
	gopkg.in/yaml.v3 v3.0.1 // indirect
)

`
