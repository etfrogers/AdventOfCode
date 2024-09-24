package iter

import (
	"iter"
	"math"
)

func FromString(s string) iter.Seq[string] {
	return func(yield func(string) bool) {
		for _, char := range s {
			if !yield(string(char)) {
				return
			}
		}
	}
}

// 3 optional args: start, stop, step
// 0 inputs: counts from 0 in steps of 1 forever (or to MaxInt)
// 1 input: stop (start=0, step=1)
// 2 inputs: start, stop (step=1)
// 3 inputs: start, stop, step
func Count(args ...int) iter.Seq[int] {
	start := 0
	stop := math.MaxInt
	step := 1
	switch len(args) {
	case 0:
		// use defaults
	case 1:
		stop = args[0]
	case 2:
		start = args[0]
		stop = args[1]
	case 3:
		start = args[0]
		stop = args[1]
		step = args[2]
	default:
		panic("invalid number of arguments. Count takes 0-3 integer arguments")
	}
	return func(yield func(int) bool) {
		for i := start; i < stop; i += step {
			if !yield(i) {
				return
			}
		}
	}
}

func CountDown(n int) iter.Seq[int] {
	return func(yield func(int) bool) {
		for i := n - 1; i >= 0; i-- {
			if !yield(i) {
				return
			}
		}
	}
}

// iter.FromSlice returns an iterator over a slice.
// For example purposes only, this iterator implements
// some of the optional interfaces mentioned earlier.
func FromSlice[E any](s []E) iter.Seq[E] {
	return func(yield func(E) bool) {
		for i := range len(s) {
			if !yield(s[i]) {
				return
			}
		}
	}
}

func Zip[T1, T2 any](s1 iter.Seq[T1], s2 iter.Seq[T2]) iter.Seq2[T1, T2] {
	return func(yield func(T1, T2) bool) {
		next1, stop1 := iter.Pull(s1)
		defer stop1()
		next2, stop2 := iter.Pull(s2)
		defer stop2()
		ok1 := true
		ok2 := true
		var v1 T1
		var v2 T2
		for ok1 && ok2 {
			v1, ok1 = next1()
			v2, ok2 = next2()
			if !yield(v1, v2) {
				break
			}
		}
	}
}

func ZipSlice[T1, T2 any](s1 []T1, s2 []T2) iter.Seq2[T1, T2] {
	return Zip(FromSlice(s1), FromSlice(s2))
}

func Keys[K comparable, V any](m map[K]V) iter.Seq[K] {
	return func(yield func(K) bool) {
		for k := range m {
			if !yield(k) {
				break
			}
		}
	}

}

func Values[K comparable, V any](m map[K]V) iter.Seq[V] {
	return func(yield func(V) bool) {
		for _, v := range m {
			if !yield(v) {
				break
			}
		}
	}
}
