package queue

type node struct {
	next  *node
	value any
}

// A FIFO queue
type Queue[T any] struct {
	front, back *node
	len         int
}

func New[T any]() Queue[T] {
	return Queue[T]{}
}

func (q *Queue[T]) Push(items ...T) {
	for _, item := range items {
		q.push(item)
	}
}

func (q *Queue[T]) push(item T) {
	n := node{value: item, next: nil}
	if q.len == 0 {
		q.back = &n
		q.front = q.back
	} else {
		q.back.next = &n
		q.back = q.back.next
	}
	q.len++
}

func (q *Queue[T]) Pop() T {
	n := *q.front
	q.front = n.next
	n.next = nil // to avoid memory leaks
	q.len--
	return n.value.(T)
}

func (q *Queue[T]) Len() int {
	return q.len
}
