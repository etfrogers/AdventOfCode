package set

import (
	"iter"
	"reflect"
	"sync"
)

type void interface{}

var member void

type Set[T comparable] struct {
	mutex sync.RWMutex
	items map[T]void
}

func (s *Set[T]) Items() []T {
	s.mutex.RLock()
	defer s.mutex.RUnlock()
	items := make([]T, len(s.items))
	i := 0
	for k := range s.items {
		items[i] = k
		i++
	}
	return items
}

func (s *Set[T]) Len() int {
	s.mutex.RLock()
	defer s.mutex.RUnlock()
	return len(s.items)
}

func New[T comparable](items ...T) *Set[T] {
	s := Set[T]{items: map[T]void{}}
	s.Add(items...)
	return &s
}

func (s *Set[T]) Add(items ...T) {
	s.mutex.Lock()
	defer s.mutex.Unlock()
	for _, item := range items {
		s.items[item] = member
	}
}

func Union[T comparable](s1, s2 *Set[T]) *Set[T] {
	s1.mutex.RLock()
	s2.mutex.RLock()
	defer s1.mutex.RUnlock()
	defer s2.mutex.RUnlock()
	s := New[T](s1.Items()...)
	s.Add(s2.Items()...)
	return s
}

func Difference[T comparable](s1, s2 *Set[T]) *Set[T] {
	s1.mutex.RLock()
	s2.mutex.RLock()
	defer s1.mutex.RUnlock()
	defer s2.mutex.RUnlock()
	s := New[T](s1.Items()...)
	s.Remove(s2.Items()...)
	return s
}

func (s *Set[T]) Contains(item T) bool {
	s.mutex.RLock()
	defer s.mutex.RUnlock()
	_, ok := s.items[item]
	return ok
}

func (s *Set[T]) Remove(items ...T) {
	s.mutex.Lock()
	defer s.mutex.Unlock()
	for _, item := range items {
		delete(s.items, item)
	}
}

func Intersection[T comparable](s1, s2 *Set[T]) *Set[T] {
	s1.mutex.RLock()
	s2.mutex.RLock()
	defer s1.mutex.RUnlock()
	defer s2.mutex.RUnlock()

	s := New[T]()
	for item := range s1.items {
		if s2.Contains(item) {
			s.Add(item)
		}
	}
	return s
}

func (s *Set[T]) Equals(other *Set[T]) bool {
	s.mutex.RLock()
	other.mutex.RLock()
	defer s.mutex.RUnlock()
	defer other.mutex.RUnlock()
	return reflect.DeepEqual(s.items, other.items)
}

// isdisjoint
// issubset
// issuperset
// symmetric_difference

func (s *Set[T]) Clear() {
	s.mutex.Lock()
	defer s.mutex.Unlock()
	clear(s.items)
}

func (s *Set[T]) All() iter.Seq[T] {
	return func(yield func(T) bool) {
		for item := range s.items {
			if !yield(item) {
				return
			}
		}
	}
}
