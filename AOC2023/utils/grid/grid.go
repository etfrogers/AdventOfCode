package grid

import (
	"fmt"
	"slices"
	"strings"
	"utils"
	"utils/iter"
)

type Grid[E any] struct {
	data [][]E
}

func (g *Grid[E]) Get(x, y int) E {
	return g.data[y][x]
}

func (g *Grid[E]) Set(x, y int, val E) {
	g.data[y][x] = val
}

// Can edit the returned values to set elements
func (g *Grid[E]) GetRow(y int) []E {
	return g.data[y]
}

// CanNOT edit the returned values to set elements
func (g *Grid[E]) GetCol(x int) []E {
	col := make([]E, len(g.data))
	for i := range g.data {
		col[i] = g.data[i][x]
	}
	return col
}

func (g *Grid[E]) InsertRow(y int, data []E) {
	if len(data) != g.NCols() {
		panic(fmt.Errorf("length of new data was %d. Existing row length is %d. These values must match",
			len(data), g.NRows()))
	}
	g.data = slices.Insert(g.data, y, data)
}

func (g *Grid[E]) InsertCol(x int, data []E) {
	if len(data) != g.NRows() {
		panic(fmt.Errorf("length of new data was %d. Existing row length is %d. These values must match",
			len(data), g.NRows()))
	}
	for i := range g.data {
		g.data[i] = slices.Insert(g.data[i], x, data[i])
	}
}

func (g *Grid[E]) NCols() int {
	return len(g.data[0])
}

func (g *Grid[E]) NRows() int {
	return len(g.data)
}

func (g *Grid[E]) Size() (ncols, nrows int) {
	return g.NCols(), g.NRows()
}

func Full[E any](x, y int, content E) Grid[E] {
	g := Grid[E]{make([][]E, y)}
	for i := range g.data {
		g.data[i] = utils.FullSlice[[]E](x, content)
	}
	return g
}

func (g *Grid[E]) checkLengths() {
	for i := range g.data {
		if len(g.data[i]) != len(g.data[0]) {
			panic("All lines in a grid must have the same length")
		}
	}
}

func New[E any](input [][]E) Grid[E] {
	g := Grid[E]{input}
	g.checkLengths()
	return g
}

func NewFromStrings(lines []string) Grid[string] {
	g := Grid[string]{make([][]string, len(lines))}
	for i, line := range lines {
		g.data[i] = strings.Split(line, "")
	}
	return g
}

func (g *Grid[E]) Clone() Grid[E] {
	new := Grid[E]{make([][]E, g.NRows())}
	for i := range g.data {
		new.data[i] = slices.Clone(g.data[i])
	}
	return new
}

func (g *Grid[E]) String() string {
	arr := make([]string, len(g.data))
	for i, elems := range g.data {
		var chars []string
		// switch any(elems[0]).(type){
		chars, ok := any(elems).([]string)
		if !ok {
			chars = utils.Map[E, string](elems, func(elem E) string { return fmt.Sprint(elem) })
		}
		arr[i] = strings.Join(chars, "")
	}
	return strings.Join(arr, "\n")
}

// two args: invert, and colMajor, both bool, default false
func (g *Grid[E]) Iterator(args ...bool) iter.SetIter[E] {
	return &gridIter[E]{g, g.IndIterator(args...)}
}

func (g *Grid[E]) LineIterator() iter.Iter[[]E] {
	return &lineIter[E]{g, -1}
}

// two args: invert, and colMajor, both bool, default false
func (g *Grid[E]) IndIterator(args ...bool) iter.Iter2[int, int] {
	invert, colMajor := false, false
	switch len(args) {

	case 2:
		colMajor = args[1]
		fallthrough
	case 1:
		invert = args[0]
	case 0:
		// do nothing
	default:
		panic("function IndIterator take a maximu of two args")
	}
	return newIndIter[E](g, invert, colMajor)
}

func Map[E any, T any](g *Grid[E], fn func(E) T) Grid[T] {
	var elem T
	new := Full[T](g.NRows(), g.NCols(), elem)
	old_it := g.Iterator()
	new_it := new.Iterator()
	for elem, ok := old_it.Next(); ok; elem, ok = old_it.Next() {
		new_it.Next()
		new_it.Set(fn(elem))
	}
	return new
}

type gridIter[E any] struct {
	grid *Grid[E]
	inds iter.Iter2[int, int]
}

type lineIter[E any] struct {
	grid *Grid[E]
	i    int
}

type indIter[E any] struct {
	grid     *Grid[E]
	x, y     int
	invert   bool
	colMajor bool
}

func newIndIter[E any](g *Grid[E], invert, colMajor bool) *indIter[E] {
	it := indIter[E]{grid: g, invert: invert, colMajor: colMajor}
	if invert {
		if colMajor {
			it.x, it.y = g.NCols()-1, g.NRows()
		} else {
			it.x, it.y = g.NCols(), g.NRows()-1
		}
	} else {
		if colMajor {
			it.x, it.y = 0, -1
		} else {
			it.x, it.y = -1, 0
		}
	}
	return &it
}

func (it *indIter[E]) Next() (x, y int, ok bool) {
	if it.invert {
		return it.prev()
	} else {
		return it.next()
	}
}

func (it *indIter[E]) Prev() (x, y int, ok bool) {
	if it.invert {
		return it.next()
	} else {
		return it.prev()
	}
}

func (it *indIter[E]) next() (x, y int, ok bool) {
	if it.colMajor {
		return it.colMajorNext()
	} else {
		return it.rowMajorNext()
	}
}

func (it *indIter[E]) prev() (x, y int, ok bool) {
	if it.colMajor {
		return it.colMajorPrev()
	} else {
		return it.rowMajorPrev()
	}
}

func (it *indIter[E]) colMajorNext() (x, y int, ok bool) {
	it.y++
	if it.y == it.grid.NRows() {
		it.x++
		it.y = 0
	}
	if it.x == it.grid.NCols() {
		return -1, -1, false
	}
	return it.x, it.y, true
}

func (it *indIter[E]) rowMajorNext() (x, y int, ok bool) {
	it.x++
	if it.x == it.grid.NCols() {
		it.y++
		it.x = 0
	}
	if it.y == it.grid.NRows() {
		return -1, -1, false
	}
	return it.x, it.y, true
}

func (it *indIter[E]) colMajorPrev() (x, y int, ok bool) {
	it.y--
	if it.y < 0 {
		it.x--
		it.y = it.grid.NRows() - 1
	}
	if it.x < 0 {
		return -1, -1, false
	}
	return it.x, it.y, true
}
func (it *indIter[E]) rowMajorPrev() (x, y int, ok bool) {
	it.x--
	if it.x < 0 {
		it.y--
		it.x = it.grid.NCols() - 1
	}
	if it.y < 0 {
		return -1, -1, false
	}
	return it.x, it.y, true
}

func (it *gridIter[E]) Next() (E, bool) {
	x, y, ok := it.inds.Next()
	if ok {
		return it.grid.Get(x, y), true
	} else {
		var r E
		return r, false
	}
}

func (it *gridIter[E]) Set(val E) {
	inds := it.inds.(*indIter[E])
	it.grid.Set(inds.x, inds.y, val)
}

func (it *lineIter[E]) Next() ([]E, bool) {
	it.i++
	if it.i == it.grid.NRows() {
		return nil, false
	}
	return it.grid.GetRow(it.i), true
}
