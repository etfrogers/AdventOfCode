package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
	"utils"

	"utils/match"
)

var digit_regexp *regexp.Regexp = regexp.MustCompile(`\d+`)
var symbol_regexp *regexp.Regexp = regexp.MustCompile(`[^.\d]`)
var gear_rexexp *regexp.Regexp = regexp.MustCompile(`\*`)

func numberLocations(lines []string) [][]match.Match {
	locations := make([][]match.Match, len(lines))
	for row, line := range lines {
		matches := match.NewFromRegexp(line, *digit_regexp)
		locations[row] = matches
	}
	return locations
}

func FindPartNumbers(lines []string) []int {
	partNumbers := []int{}
	numberLocations := numberLocations(lines)
	for row, matches := range numberLocations {
		for _, match := range matches {
			if TouchingSymbol(match, row, lines) {
				number, err := strconv.Atoi(match.Text)
				utils.Check(err)
				partNumbers = append(partNumbers, number)
			}
		}
	}
	return partNumbers
}

func FindGearRatios(lines []string) []int {
	ratios := []int{}
	numberLocations := numberLocations(lines)
	for row, line := range lines {
		matches := match.NewFromRegexp(line, *gear_rexexp)
		for _, match := range matches {
			touchingNumbers := FindTouchingNumbers(match, row, numberLocations)
			nTouching := len(touchingNumbers)
			if nTouching > 2 {
				panic("Too many touching numbers")
			} else if nTouching == 2 {
				ratio := touchingNumbers[0] * touchingNumbers[1]
				ratios = append(ratios, ratio)
			}
			// If one or zero touching numbers, do nothing
		}
	}
	return ratios
}

func FindTouchingNumbers(match match.Match, row int, numberLocations [][]match.Match) []int {
	numbers := []int{}
	gearCol := match.Start
	rows := []int{row}
	if row > 0 {
		rows = append(rows, row-1)
	}
	if row < len(numberLocations)-1 {
		rows = append(rows, row+1)
	}
	for _, row := range rows {
		for _, numberMatch := range numberLocations[row] {
			for i := numberMatch.Start; i < numberMatch.End; i++ {
				if i >= gearCol-1 && i <= gearCol+1 {
					val, err := strconv.Atoi(numberMatch.Text)
					utils.Check(err)
					numbers = append(numbers, val)
					break
				}
			}
		}
	}
	return numbers
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
	last_col := match.End
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

func SumGearRatios(lines []string) int {
	return sum(FindGearRatios(lines))
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
	utils.Check(err)
	lines := strings.Split(string(doc), "\n")

	fmt.Printf("Day 3, Part 1 answer: %d\n", SumPartNumbers(lines))
	fmt.Printf("Day 3, Part 2 answer: %d\n", SumGearRatios(lines))
}
