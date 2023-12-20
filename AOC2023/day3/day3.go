package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"

	"day1/match"
)

var digit_regexp *regexp.Regexp = regexp.MustCompile(`\d+`)
var symbol_regexp *regexp.Regexp = regexp.MustCompile(`[^.\d]`)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func FindPartNumbers(lines []string) []int {

	partNumbers := []int{}
	for row, line := range lines {
		matches := match.NewFromRegexp(line, *digit_regexp)
		for _, match := range matches {
			if TouchingSymbol(match, row, lines) {
				number, err := strconv.Atoi(match.Text)
				check(err)
				partNumbers = append(partNumbers, number)
			}
		}
	}
	return partNumbers
}

func TouchingSymbol(match match.Match, row int, lines []string) bool {
	first_row := row
	if row > 0 {
		first_row--
	}
	last_row := row
	if last_row < len(lines)-1 {
		last_row++
	}
	first_col := match.Start
	if first_col > 0 {
		first_col--
	}
	last_col := match.Start + match.Len
	if last_col < len(lines[0])-1 {
		last_col++
	}

	for line_no := first_row; line_no <= last_row; line_no++ {
		fragment := lines[line_no][first_col:last_col]
		symbol_match := symbol_regexp.FindString(fragment)
		if symbol_match != "" {
			return true
		}
	}
	return false
}

func SumPartNumbers(lines []string) int {
	return sum(FindPartNumbers(lines))
}
func sum(data []int) int {
	total := 0
	for _, val := range data {
		total += val
	}
	return total
}

func main() {
	doc, err := os.ReadFile("input.txt")
	check(err)
	lines := strings.Split(string(doc), "\n")

	fmt.Printf("Day 3, Part 1 answer: %d\n", SumPartNumbers(lines))
}
