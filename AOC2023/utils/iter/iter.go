package iter

// Iter supports iterating over a sequence of values of type `E`.
type Iter[E any] interface {
	// Next returns the next value in the iteration if there is one,
	// and reports whether the returned value is valid.
	// Once Next returns ok==false, the iteration is over,
	// and all subsequent calls will return ok==false.
	Next() (elem E, ok bool)
}

// Iter2 is like Iter but each iteration returns a pair of values.
type Iter2[E1, E2 any] interface {
	Next() (E1, E2, bool)
}

// StopIter is an optional interface for Iter.
type StopIter[E any] interface {
	Iter[E]

	// Stop indicates that the iterator will no longer be used.
	// After a call to Stop, future calls to Next may panic.
	// Stop may be called multiple times;
	// all calls after the first will have no effect.
	Stop()
}

// StopIter2 is like StopIter, but for Iter2.
type StopIter2[E1, E2 any] interface {
	Iter2[E1, E2]
	Stop()
}

// NewNext2 is like NewNext for Iter2.
// func NewNext2[E1, E2 any](next func(E1, E2, bool)) Iter2[E1, E2]

// NewGen2 is like NewGen for Iter2.
// func NewGen2[E1, E2 any](gen func(yield func(E1, E2) bool)) StopIter2[E1, E2]

// FromMap returns an iterator over a map.
// func FromMap[K comparable, V any](map[K]V) Iter2[K, V]

// ToMap collects the elements of the iterator into a map.
// [ Perhaps this should be maps.FromIter. ]
// func ToMap[K comparable, V any](it Iter2[K, V]) map[K]V

// DeleteIter is an Iter that implements a Delete method.
type DeleteIter[E any] interface {
	Iter[E]

	// Delete deletes the current iterator element;
	// that is, the one returned by the last call to Next.
	// Delete should panic if called before Next or after
	// Next returns false.
	Delete()
}

// SetIter is an Iter that implements a Set method.
type SetIter[E any] interface {
	Iter[E]

	// Set replaces the current iterator element with v.
	// Set should panic if called before Next or after
	// Next returns false.
	Set(v E)
}

// PrevIter is an iterator with a Prev method.
type PrevIter[E any] interface {
	Iter[E]

	// Prev moves the iterator to the previous position.
	// After calling Prev, Next will return the value at
	// that position in the container. For example, after
	//   it.Next() returning (v, true)
	//   it.Prev()
	// another call to it.Next will again return (v, true).
	// Calling Prev before calling Next may panic.
	// Calling Prev after Next returns false will move
	// to the last element, or, if there are no elements,
	// to the iterator's initial state.
	Prev()
}

// ToSlice returns a slice containing all the elements in an iterator.
// [ This might be in the slices package, as slices.FromIter. ]
func ToSlice[E any](it Iter[E]) []E {
	var r []E
	for v, _ok := it.Next(); _ok; v, _ok = it.Next() {
		r = append(r, v)
	}
	return r
}

// Filter returns a new iterator that only contains the elements of it
// for which f returns true.
func Filter[E any](f func(E) bool, it Iter[E]) Iter[E] {
	return NewNext(func() (E, bool) {
		for {
			e, ok := it.Next()
			if !ok || f(e) {
				return e, ok
			}
		}
	})
}

// Reduce reduces an iterator to a value using a function.
func Reduce[E1, E2 any](f func(E2, E1) E2, it Iter[E1], init E2) E2 {
	r := init
	for v, _ok := it.Next(); _ok; v, _ok = it.Next() {
		r = f(r, v)
	}
	return r
}

func Map[E1, E2 any](f func(E1) E2, it Iter[E1]) Iter[E2] {
	return NewNext(func() (E2, bool) {
		e, ok := it.Next()
		var r E2
		if ok {
			r = f(e)
		}
		return r, ok
	})
}

func All(s Iter[bool]) bool {
	for val, ok := s.Next(); ok; val, ok = s.Next() {
		if !val {
			return false
		}
	}
	return true
}

func Any(s Iter[bool]) bool {
	for val, ok := s.Next(); ok; val, ok = s.Next() {
		if val {
			return true
		}
	}
	return false
}

// Equal reports whether two iterators have the same values
// in the same order.
func Equal[E comparable](it1, it2 Iter[E]) bool {
	for {
		v1, ok1 := it1.Next()
		v2, ok2 := it2.Next()
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
func Concat[E any](it1, it2 Iter[E]) Iter[E] {
	return NewNext(func() (E, bool) {
		e, ok := it1.Next()
		var r E
		if ok {
			r = e
		} else {
			e, ok := it2.Next()
			if ok {
				r = e
			}
		}
		return r, ok
	})
}
