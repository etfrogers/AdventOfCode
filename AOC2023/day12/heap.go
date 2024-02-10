package main

import "container/heap"

type CursorHeap []*Cursor

func NewCursorHeap() CursorHeap {
	ch := CursorHeap((make([]*Cursor, 0)))
	heap.Init(&ch)
	return ch
}

func (c Cursor) LessThan(other Cursor) bool {
	switch {
	case c.Position < other.Position:
		{
			return true
		}
	case c.Position > other.Position:
		{
			return false
		}
	}
	// positions are equal

	clen, olen := len(c.RemainingGroups), len(other.RemainingGroups)
	switch {
	case clen < olen:
		{
			return true
		}
	case clen > olen:
		{
			return false
		}
	}
	// lengths are equal

	for i := 0; i < clen; i++ {
		if c.RemainingGroups[i] < other.RemainingGroups[i] {
			return true
		}
	}
	// all equal, so less is false
	return false
}

func (ch CursorHeap) Len() int { return len(ch) }

func (ch CursorHeap) Less(i, j int) bool {
	return ch[i].LessThan(*ch[j])
}

func (ch CursorHeap) Swap(i, j int) {
	ch[i], ch[j] = ch[j], ch[i]
	// pq[i].index = i
	// pq[j].index = j
}

func (ch *CursorHeap) PushH(cs ...Cursor) {
	for _, c := range cs {
		heap.Push(ch, c)
	}
}

func (ch *CursorHeap) PopH() Cursor {
	c := heap.Pop(ch).(*Cursor)
	return *c

}

func (ch *CursorHeap) Push(x any) {
	// n := len(*ch)
	item := x.(Cursor)
	// item.index = n
	*ch = append(*ch, &item)
}

func (ch *CursorHeap) Pop() any {
	old := *ch
	n := len(old) - 1
	item := old[n]
	old[n] = nil // avoid memory leak
	// item.index = -1 // for safety
	*ch = old[0:n]
	return item
}

func (ch CursorHeap) Peek() *Cursor {
	if ch.Len() == 0 {
		return nil
	}
	return ch[0]
}
