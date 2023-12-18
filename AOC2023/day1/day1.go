package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func GetCalibration(data string) int {
	lines := strings.Split(data, "\n")
	digit_pattern, _ := regexp.Compile(`\d`)
	total := 0
	for _, line := range lines {
		digits := digit_pattern.FindAll([]byte(line), -1)
		str_number := []byte{digits[0][0], digits[len(digits)-1][0]}
		value, err := strconv.Atoi(string(str_number))
		check(err)
		total += value
	}
	return total
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	doc_bytes, err := os.ReadFile("input.txt")
	var document string = string(doc_bytes[:])
	check(err)
	// fmt.Print(string(document))
	calibration_code := GetCalibration(document)
	fmt.Printf("Day 1, Part 1: %d\n", calibration_code)

}
