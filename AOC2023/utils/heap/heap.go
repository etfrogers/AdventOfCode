package heap

import "container/heap"

type Heaper interface {
	Less(other Heaper) bool
}

type SliceHeap[T Heaper] []*T

func NewSliceHeap[T Heaper]() SliceHeap[T] {
	h := SliceHeap[T](make([]*T, 0))
	heap.Init(&h)
	return h
}

func (h SliceHeap[T]) Len() int { return len(h) }

func (ch SliceHeap[T]) Less(i, j int) bool {
	v1 := ch[i]
	return (*v1).Less(*ch[j])
}

func (ch SliceHeap[T]) Swap(i, j int) {
	ch[i], ch[j] = ch[j], ch[i]

}

func (ch *SliceHeap[T]) PushH(ts ...T) {
	for _, v := range ts {
		heap.Push(ch, v)
	}
}

func (ch *SliceHeap[T]) PopH() T {
	c := heap.Pop(ch).(*T)
	return *c

}

func (ch *SliceHeap[T]) Push(x any) {
	item := x.(T)
	*ch = append(*ch, &item)
}

func (ch *SliceHeap[T]) Pop() any {
	old := *ch
	n := len(old) - 1
	item := old[n]
	old[n] = nil // avoid memory leak
	*ch = old[0:n]
	return item
}

func (ch SliceHeap[T]) Peek() *T {
	if ch.Len() == 0 {
		return nil
	}
	return ch[0]
}
