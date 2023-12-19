package main

import (
	"fmt"
	"os"
	"regexp"
	"sort"
	"strings"

	"day1/digits"
	"day1/match"
)

func DigitsInLine(line string, convertWords bool) []int {

	digit_pattern, _ := regexp.Compile(`\d`)
	matches := []match.Match{}
	matches = append(matches, match.NewFromRegexp(line, *digit_pattern)...)

	if convertWords {
		for _, re := range digits.DigitWordRegexps {
			matches = append(matches, match.NewFromRegexp(line, *re)...)
		}
	}

	sort.Slice(matches, func(i, j int) bool { return matches[i].LessThan(matches[j]) })
	digits_ := make([]int, len(matches))
	for i, m := range matches {
		digits_[i] = m.Digit()
	}
	return digits_
}

func ValidationCode(digits []int) int {
	if len(digits) == 0 {
		return 0
	}
	return 10*digits[0] + digits[len(digits)-1]
}

func GetCalibration(data string, convertWords bool) int {
	lines := strings.Split(data, "\n")
	total := 0
	for _, line := range lines {
		digits := DigitsInLine(line, convertWords)
		value := ValidationCode(digits)
		// fmt.Println(line, value)
		total += value
	}
	// fmt.Println("")
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
	calibration_code := GetCalibration(document, false)
	fmt.Printf("Day 1, Part 1: %d\n", calibration_code)

	part2_code := GetCalibration(document, true)
	fmt.Printf("Day 1, Part 2: %d\n", part2_code)

}
