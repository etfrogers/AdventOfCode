package stack

import (
	"iter"
	"sync"
)

type (
	Stack[T any] struct {
		top    *node[T]
		length int
		mutex  sync.RWMutex
	}
	node[T any] struct {
		value T
		prev  *node[T]
	}
)

// Create a new stack
func New[T any]() *Stack[T] {
	return &Stack[T]{top: nil, length: 0}
}

// Return the number of items in the stack
func (this *Stack[T]) Len() int {
	this.mutex.RLock()
	defer this.mutex.RUnlock()
	return this.length
}

// View the top item on the stack
func (this *Stack[T]) Peek() (T, bool) {
	this.mutex.RLock()
	defer this.mutex.RUnlock()
	if this.length == 0 {
		var result T
		return result, false
	}
	return this.top.value, true
}

// Pop the top item of the stack and return it
func (this *Stack[T]) Pop() (result T, ok bool) {
	this.mutex.Lock()
	defer this.mutex.Unlock()
	if this.length == 0 {
		var result T
		return result, false
	}

	n := this.top
	this.top = n.prev
	this.length--
	return n.value, true
}

// Push a value onto the top of the stack
func (this *Stack[T]) Push(value T) {
	this.mutex.Lock()
	defer this.mutex.Unlock()
	n := &node[T]{value, this.top}
	this.top = n
	this.length++
}

func (this *Stack[T]) PushAll(values ...T) {
	for _, value := range values {
		this.Push(value)
	}
}

// All returns an iterator over all elements in the stack. Consumes the stack
func (this *Stack[T]) All() iter.Seq[T] {
	return func(yield func(T) bool) {
		for this.length > 0 {
			if val, ok := this.Pop(); !(ok && yield(val)) {
				return
			}
		}
	}
}
