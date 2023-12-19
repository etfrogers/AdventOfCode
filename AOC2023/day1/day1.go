package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

var DIGIT_MAPPING = map[string]string{
	"one":   "1",
	"two":   "2",
	"three": "3",
	"four":  "4",
	"five":  "5",
	"six":   "6",
	"seven": "7",
	"eight": "8",
	"nine":  "9",
}

func GetCalibration(data string) int {
	lines := strings.Split(data, "\n")
	digit_pattern, _ := regexp.Compile(`\d`)
	total := 0
	for _, line := range lines {
		digits := digit_pattern.FindAllString(line, -1)
		str_number := digits[0] + digits[len(digits)-1]
		fmt.Println(line, str_number)
		value, err := strconv.Atoi(str_number)
		check(err)
		total += value
	}
	fmt.Println("")
	return total
}

func ConvertTextToDigit(data string) string {
	new_data := data
	var keys []string
	i := 0
	for k := range DIGIT_MAPPING {
		keys = append(keys, "("+k+")")
		i++
	}
	re_str := strings.Join(keys, "|")
	re, err := regexp.Compile(re_str)
	check(err)
	new_data = re.ReplaceAllStringFunc(new_data, func(k string) string { return DIGIT_MAPPING[k] })
	return new_data
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
	calibration_code := GetCalibration(document)
	fmt.Printf("Day 1, Part 1: %d\n", calibration_code)

	converted_doc := ConvertTextToDigit(document)
	part2_code := GetCalibration(converted_doc)
	fmt.Printf("Day 1, Part 2: %d\n", part2_code)

}
