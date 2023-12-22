package set

import "reflect"

type void interface{}

var member void

type Set[T comparable] struct {
	items map[T]void
}

func (s *Set[T]) Items() []T {
	items := make([]T, len(s.items))
	i := 0
	for k := range s.items {
		items[i] = k
		i++
	}
	return items
}

func (s *Set[T]) Len() int {
	return len(s.items)
}

func New[T comparable](items ...T) Set[T] {
	s := Set[T]{items: map[T]void{}}
	s.Add(items...)
	return s
}

func (s *Set[T]) Add(items ...T) {
	for _, item := range items {
		s.items[item] = member
	}
}

func Union[T comparable](s1, s2 Set[T]) Set[T] {
	s := New[T](s1.Items()...)
	s.Add(s2.Items()...)
	return s
}

func Difference[T comparable](s1, s2 Set[T]) Set[T] {
	s := New[T](s1.Items()...)
	s.Remove(s2.Items()...)
	return s
}

func (s *Set[T]) Contains(item T) bool {
	_, ok := s.items[item]
	return ok
}

func (s *Set[T]) Remove(items ...T) {
	for _, item := range items {
		if s.Contains(item) {
			delete(s.items, item)
		}
	}
}

func Intersection[T comparable](s1, s2 Set[T]) Set[T] {
	s := New[T]()
	for item := range s1.items {
		if s2.Contains(item) {
			s.Add(item)
		}
	}
	return s
}

func (s Set[T]) Equals(other Set[T]) bool {
	return reflect.DeepEqual(s.items, other.items)
}

// isdisjoint
// issubset
// issuperset
// symmetric_difference

func (s *Set[T]) Clear() {
	clear(s.items)
}
