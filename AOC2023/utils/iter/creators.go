package iter

import (
	"runtime"
	"sync/atomic"
)

func FromString(s string) interface {
	PrevIter[string]
	SetIter[string]
} {
	return &strIter{s: s, i: -1}
}

type strIter struct {
	s string
	i int
}

func (it *strIter) Next() (string, bool) {
	it.i++
	ok := it.i >= 0 && it.i < len(it.s)
	var v string
	if ok {
		v = string(it.s[it.i])
	}
	return v, ok
}

// Prev implements PrevIter.
func (it *strIter) Prev() {
	it.i--
}

// Set implements SetIter.
func (it *strIter) Set(v string) {
	if len(v) != 1 {
		panic("set takes a string of length 1")
	}
	r := rune(v[0])
	rs := []rune(it.s)
	rs[it.i] = rune(r)
	it.s = string(rs)
}

// iter.FromSlice returns an iterator over a slice.
// For example purposes only, this iterator implements
// some of the optional interfaces mentioned earlier.
func FromSlice[E any](s []E) Iter[E] {
	return &sliceIter[E]{
		s: s,
		i: -1,
	}
}

type sliceIter[E any] struct {
	s []E
	i int
}

func (it *sliceIter[E]) Next() (E, bool) {
	it.i++
	ok := it.i >= 0 && it.i < len(it.s)
	var v E
	if ok {
		v = it.s[it.i]
	}
	return v, ok
}

// Prev implements PrevIter.
func (it *sliceIter[E]) Prev() {
	it.i--
}

// Set implements SetIter.
func (it *sliceIter[E]) Set(v E) {
	it.s[it.i] = v
}

// NewNext takes a function that returns (v, bool) and returns
// an iterator that calls the function until the second result is false.
func NewNext[E any](f func() (E, bool)) Iter[E] {
	return funcIter[E](f)
}

// funcIter is used by NewNext to implement Iter.
type funcIter[E any] func() (E, bool)

// Next implements Iter.
func (f funcIter[E]) Next() (E, bool) {
	return f()
}

// NewGen creates a new iterator from a generator function gen.
// The gen function is called once.  It is expected to call
// yield(v) for every value v to be returned by the iterator.
// If yield(v) returns false, gen must stop calling yield and return.
func NewGen[E any](gen func(yield func(E) bool)) StopIter[E] {
	cmore := make(chan bool)
	cnext := make(chan E)

	generator := func() {
		// coroutine switch back to client until Next is called (1)
		var zero E
		cnext <- zero
		if !<-cmore {
			close(cnext)
			return
		}
		gen(func(v E) bool {
			// coroutine switch back to client to deliver v (2)
			cnext <- v
			return <-cmore
		})

		// coroutine switch back to client marking end (3)
		close(cnext)
	}

	// coroutine switch to start generator (4)
	go generator()
	<-cnext

	r := &genIter[E]{cnext: cnext, cmore: cmore}
	runtime.SetFinalizer(r, (*genIter[E]).Stop)
	return r
}

// genIter implements Iter[E] for NewGen.
type genIter[E any] struct {
	cnext  chan E
	cmore  chan bool
	closed atomic.Bool
}

// Next implements Iter[E]
func (it *genIter[E]) Next() (E, bool) {
	// coroutine switch to generator for more (5)
	// (This panics if Stop has been called.)
	it.cmore <- true
	v, ok := <-it.cnext
	return v, ok
}

// Stop implements StopIter[E]
func (it *genIter[E]) Stop() {
	// Use the closed field to make Stop idempotent.
	if !it.closed.CompareAndSwap(false, true) {
		return
	}
	runtime.SetFinalizer(it, nil)
	// coroutine switch to generator to stop (6)
	close(it.cmore)
	<-it.cnext
}
