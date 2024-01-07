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

func Reduce[T any](s []T, fn func(T, T) T) T {
	var result T
	switch len(s) {
	case 0, 1:
		panic("slice input to reduce must have at least 2 elements")
	default:
		result = fn(s[0], s[1])
		for i := 2; i < len(s); i++ {
			result = fn(result, s[i])
		}
	}
	return result
}

func Filter[T any](s []T, fn func(T) bool) (output []T) {
	output = []T{}
	for _, val := range s {
		if fn(val) {
			output = append(output, val)
		}
	}
	return
}

func Sum[T int | float64](data []T) T {
	total := T(0)
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

func DropEmpty[T string | []int](s []T) []T {
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

func MapKeys[T comparable, V any](m map[T]V) (keys []T) {
	keys = make([]T, len(m))
	i := 0
	for k := range m {
		keys[i] = k
		i++
	}
	return
}

func All(s []bool) bool {
	for _, val := range s {
		if !val {
			return false
		}
	}
	return true
}

func Any(s []bool) bool {
	for _, val := range s {
		if val {
			return true
		}
	}
	return false
}

func GCF(n ...int) int {
	switch len(n) {
	case 0:
		return 0
	case 1:
		return n[0]
	default:
		return Reduce(n, gcf2)
	}
}

func gcf2(p, q int) int {
	if p < 0 || q < 0 {
		panic("all inputs to gcf must be non-negative")
	}

	for q > 0 {
		old_q := q
		q = p % q
		p = old_q
	}
	return p
}

func LCM(n ...int) int {
	switch len(n) {
	case 0:
		return 0
	case 1:
		return n[0]
	default:
		return Reduce(n, lcm2)
	}
}

func lcm2(p, q int) int {
	if p < 0 || q < 0 {
		panic("all inputs to gcf must be non-negative")
	}
	return p * q / (gcf2(p, q))
}
