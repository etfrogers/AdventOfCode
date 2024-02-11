package main

import "utils/heap"

type CursorHeap heap.SliceHeap[Cursor]

func (c Cursor) Less(other heap.Heaper) bool {
	o := other.(Cursor)
	switch {
	case c.Position < o.Position:
		{
			return true
		}
	case c.Position > o.Position:
		{
			return false
		}
	}
	// positions are equal

	clen, olen := len(c.RemainingGroups), len(o.RemainingGroups)
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
		if c.RemainingGroups[i] < o.RemainingGroups[i] {
			return true
		}
	}
	// all equal, so less is false
	return false
}
