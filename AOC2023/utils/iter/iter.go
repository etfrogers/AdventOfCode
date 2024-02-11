package iter

import (
	"cmp"
	"iter"
	"strings"
)

// ToSlice returns a slice containing all the elements in an iterator.
// [ This might be in the slices package, as slices.FromIter. ]
func ToSlice[E any](it iter.Seq[E]) []E {
	r := make([]E, 0)
	for v := range it {
		r = append(r, v)
	}
	return r
}

func ToString(it iter.Seq[string]) string {
	b := strings.Builder{}
	for v := range it {
		b.WriteString(v)
	}
	return b.String()
}

// Filter returns a new iterator that only contains the elements of it
// for which f returns true.
func Filter[E any](f func(E) bool, it iter.Seq[E]) iter.Seq[E] {
	return func(yield func(E) bool) {
		for e := range it {
			if f(e) {
				if !yield(e) {
					return
				}
			}
		}
	}
}

// Reduce reduces an iterator to a value using a function.
func Reduce[E1, E2 any](f func(E2, E1) E2, it iter.Seq[E1], init E2) E2 {
	r := init
	for v := range it {
		r = f(r, v)
	}
	return r
}

func Map[E1, E2 any](f func(E1) E2, it iter.Seq[E1]) iter.Seq[E2] {
	return func(yield func(E2) bool) {
		for v := range it {
			if !yield(f(v)) {
				return
			}

		}
	}
}

func All(s iter.Seq[bool]) bool {
	for val := range s {
		if !val {
			return false
		}
	}
	return true
}

func Any(s iter.Seq[bool]) bool {
	for val := range s {
		if val {
			return true
		}
	}
	return false
}

func Max[E cmp.Ordered](it iter.Seq[E]) E {
	next, stop := iter.Pull(it)
	defer stop()
	maxVal, ok := next()
	if !ok {
		panic("max called on an empty iterator")
	}
	for val := range it {
		maxVal = max(maxVal, val)
	}
	return maxVal
}

func MaxFunc[E any](it iter.Seq[E], less func(v1, v2 E) bool) E {
	next, stop := iter.Pull(it)
	defer stop()
	maxVal, ok := next()
	if !ok {
		panic("max called on an empty iterator")
	}
	for val := range it {
		if less(maxVal, val) {
			maxVal = val
		}
	}
	return maxVal
}

func Min[E cmp.Ordered](it iter.Seq[E]) E {
	next, stop := iter.Pull(it)
	defer stop()
	minVal, ok := next()
	if !ok {
		panic("max called on an empty iterator")
	}
	for val := range it {
		minVal = min(minVal, val)
	}
	return minVal
}

func MinFunc[E any](it iter.Seq[E], less func(v1, v2 E) bool) E {
	next, stop := iter.Pull(it)
	defer stop()
	minVal, ok := next()
	if !ok {
		panic("max called on an empty iterator")
	}
	for val := range it {
		if less(val, minVal) {
			minVal = val
		}
	}
	return minVal
}

// Equal reports whether two iterators have the same values
// in the same order.
func Equal[E comparable](it1, it2 iter.Seq[E]) bool {
	next1, stop1 := iter.Pull(it1)
	next2, stop2 := iter.Pull(it2)
	defer stop1()
	defer stop2()
	for {
		v1, ok1 := next1()
		v2, ok2 := next2()
		if v1 != v2 || ok1 != ok2 {
			return false
		}
		if !ok1 {
			return true
		}
	}
}

// Concat returns the concatenation of two iterators.
// The resulting iterator returns all the elements of the
// first iterator followed by all the elements of the second.
func Chain[E any](its ...iter.Seq[E]) iter.Seq[E] {
	return func(yield func(E) bool) {
		for _, it := range its {
			for v := range it {
				if !yield(v) {
					return
				}
			}
		}
	}

}
