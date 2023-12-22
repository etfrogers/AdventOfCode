package main

import (
	"fmt"
	"os"
	"utils"
)

var package_line_temp string = "package day%s"

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

	package_line := fmt.Sprintf(package_line_temp, day)
	package_bytes := []byte(package_line)
	err = os.WriteFile(dirname+string(os.PathSeparator)+fname, package_bytes, 0644)
	utils.Check(err)

	err = os.WriteFile(dirname+string(os.PathSeparator)+test_name, package_bytes, 0644)
	utils.Check(err)

	err = os.WriteFile(dirname+string(os.PathSeparator)+"input.txt", []byte(""), 0644)
	utils.Check(err)

}
