package utils

import (
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

func Map[T, V any](ts []T, fn func(T) V) []V {
	result := make([]V, len(ts))
	for i, t := range ts {
		result[i] = fn(t)
	}
	return result
}

func Sum(data []int) int {
	total := 0
	for _, val := range data {
		total += val
	}
	return total
}

func Prod(data []int) int {
	if len(data) == 0 {
		return 0
	}
	prod := 1
	for _, val := range data {
		prod *= val
	}
	return prod
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

func PowInts(x, n int) (int, error) {
	var err error = nil
	if n < 0 {
		err = fmt.Errorf("n must be >= 0")
		return 0, err
	}
	if n == 0 {
		return 1, err
	}
	if n == 1 {
		return x, err
	}
	y, err := PowInts(x, n/2)
	if n%2 == 0 {
		return y * y, err
	}
	return x * y * y, err
}

func SplitSlice[T comparable](s []T, sep T) [][]T {
	output := [][]T{}
	current_ind := 0
	output = append(output, []T{})
	for _, val := range s {
		if val == sep {
			if len(output[current_ind]) > 0 {
				current_ind++
				output = append(output, []T{})
			}
		} else {
			output[current_ind] = append(output[current_ind], val)
		}
	}
	if len(output[current_ind]) == 0 {
		output = output[:len(output)-1]
	}
	return output
}

// Splits on fist instance of sep
func CutSlice[T comparable](s []T, sep T) (part1, part2 []T) {
	index := slices.Index[[]T, T](s, sep)
	if index < 0 {
		// Separator not found
		part1 = s[:]
		part2 = []T{}
		return
	}
	part1 = s[:index]
	part2 = s[index+1:]
	return
}

func DropEmpty[T string | []any](s []T) []T {
	new := []T{}
	for _, val := range s {
		if len(val) != 0 {
			new = append(new, val)
		}
	}
	return new
}

func AtoiError(x string) int {
	v, e := strconv.Atoi(x)
	Check(e)
	return v
}
