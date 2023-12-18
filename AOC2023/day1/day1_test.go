package main

import (
	"testing"
)

// Test the first test case give the part 1 result
func TestHelloName(t *testing.T) {
	data := `1abc2
 pqr3stu8vwx
 a1b2c3d4e5f
 treb7uchet`
	expected := 142
	calibration_code := GetCalibration(data)
	if calibration_code != expected {
		t.Fatalf("Unexpected value %v. Expected %d", calibration_code, expected)
	}
}

// TestHelloEmpty calls greetings.Hello with an empty string,
// checking for an error.
/*
func TestHelloEmpty(t *testing.T) {
    msg, err := Hello("")
    if msg != "" || err == nil {
        t.Fatalf(`Hello("") = %q, %v, want "", error`, msg, err)
    }
}
*/
