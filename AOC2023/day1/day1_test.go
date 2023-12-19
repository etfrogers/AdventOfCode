package main

import (
	"os"
	"testing"
)

// Test the first test case give the part 1 result
func TestPart1TestCase(t *testing.T) {
	data := `1abc2
 pqr3stu8vwx
 a1b2c3d4e5f
 treb7uchet`
	expected := 142
	calibration_code := GetCalibration(data, false)
	if calibration_code != expected {
		t.Fatalf("Unexpected value %v. Expected %d", calibration_code, expected)
	}
}

func TestPart1(t *testing.T) {
	doc_bytes, err := os.ReadFile("input.txt")
	var document string = string(doc_bytes[:])
	check(err)
	calibration_code := GetCalibration(document, false)
	expected := 53651
	if calibration_code != expected {
		t.Fatalf("Unexpected value %v. Expected %d", calibration_code, expected)
	}
}

func TestPart2TestCase(t *testing.T) {
	data := `two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen`
	expected := 281

	calibration_code := GetCalibration(data, true)
	if calibration_code != expected {
		t.Fatalf("Unexpected value %v. Expected %d", calibration_code, expected)
	}
}

func TestPart2CaseSeparate(t *testing.T) {
	testCases := []struct {
		line string
		want int
	}{
		{"two1nine", 29},
		{"eightwothree", 83},
		{"abcone2threexyz", 13},
		{"xtwone3four", 24},
		{"4nineeightseven2", 42},
		{"zoneight234", 14},
		{"7pqrstsixteen", 76},
		{"eighthree", 83},
		{"sevenine", 79},
	}
	for _, tc := range testCases {
		t.Run(tc.line, func(t *testing.T) {
			calibration_code := GetCalibration(tc.line, true)
			if calibration_code != tc.want {
				t.Fatalf("Unexpected value %v. Expected %d", calibration_code, tc.want)
			}
		})
	}
}

func TestPart2(t *testing.T) {
	doc_bytes, err := os.ReadFile("input.txt")
	var document string = string(doc_bytes[:])
	check(err)
	calibration_code := GetCalibration(document, true)
	expected := 53894
	if calibration_code != expected {
		t.Fatalf("Unexpected value %v. Expected %d", calibration_code, expected)
	}
}
