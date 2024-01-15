package grid

import (
	"fmt"
	"slices"
	"strings"
	"utils"
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

func (g *Grid[E]) Iterator() *gridIter[E] {
	return &gridIter[E]{g, *g.IndIterator()}
}

func (g *Grid[E]) LineIterator() *lineIter[E] {
	return &lineIter[E]{g, -1}
}

func (g *Grid[E]) IndIterator() *indIter[E] {
	return &indIter[E]{g, -1, 0}
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
	inds indIter[E]
}

type lineIter[E any] struct {
	grid *Grid[E]
	i    int
}

type indIter[E any] struct {
	grid *Grid[E]
	x, y int
}

func (g *indIter[E]) Next() (x, y int, ok bool) {
	g.x++
	if g.x == g.grid.NCols() {
		g.y++
		g.x = 0
	}
	if g.y == g.grid.NRows() {
		return -1, -1, false
	}
	return g.x, g.y, true
}

func (g *gridIter[E]) Next() (E, bool) {
	x, y, ok := g.inds.Next()
	if ok {
		return g.grid.Get(x, y), true
	} else {
		var r E
		return r, false
	}
}

func (g *gridIter[E]) Set(val E) {
	g.grid.Set(g.inds.x, g.inds.y, val)
}

func (g *lineIter[E]) Next() ([]E, bool) {
	g.i++
	if g.i == g.grid.NRows() {
		return nil, false
	}
	return g.grid.GetRow(g.i), true
}
