package utils

import (
	"fmt"
	"os"
	"strings"
)

func Map[T, V any](ts []T, fn func(T) V) []V {
	result := make([]V, len(ts))
	for i, t := range ts {
		result[i] = fn(t)
	}
	return result
}

func Check(e error) {
	if e != nil {
		panic(e)
	}
}

func ReadInput() []string {
	doc, err := os.ReadFile("input.txt")
	Check(err)
	lines := strings.Split(string(doc), "\n")
	return lines
}

func PowInts(x, n int) int {
	if n < 0 {
		panic(fmt.Errorf("n must be >= 0"))
	}
	if n == 0 {
		return 1
	}
	if n == 1 {
		return x
	}
	y := PowInts(x, n/2)
	if n%2 == 0 {
		return y * y
	}
	return x * y * y
}
