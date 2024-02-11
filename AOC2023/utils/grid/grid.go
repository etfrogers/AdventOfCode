package grid

import (
	"fmt"
	"iter"
	"slices"
	"strings"
	"utils"
	i "utils/iter"
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
func (g *Grid[E]) Iterator(args ...bool) iter.Seq[E] {
	return func(yield func(E) bool) {
		for x, y := range g.IndIterator(args...) {
			if !yield(g.Get(x, y)) {
				return
			}
		}
	}
}

func (g *Grid[E]) LineIterator() iter.Seq[[]E] {
	return func(yield func([]E) bool) {
		for y := range g.NRows() {
			if !yield(g.GetRow(y)) {
				return
			}
		}
	}
}

// two args: invert, and colMajor, both bool, default false
func (g *Grid[E]) IndIterator(args ...bool) iter.Seq2[int, int] {
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
		panic("function IndIterator take a maximum of two args")
	}
	return newIndIter[E](g, invert, colMajor)
}

func Map[E any, T any](g *Grid[E], fn func(E) T) Grid[T] {
	var elem T
	new := Full[T](g.NRows(), g.NCols(), elem)
	ind_it := g.IndIterator()
	for x, y := range ind_it {
		elem := g.Get(x, y)
		new.Set(x, y, fn(elem))
	}
	return new
}

func newIndIter[E any](g *Grid[E], invert, colMajor bool) iter.Seq2[int, int] {
	switch {
	case !invert && !colMajor:
		{
			return func(yield func(int, int) bool) {
				for y := range g.NRows() {
					for x := range g.NCols() {
						if !yield(x, y) {
							return
						}
					}
				}
			}
		}
	case invert && !colMajor:
		{
			return func(yield func(int, int) bool) {
				for y := range i.CountDown(g.NRows()) {
					for x := range i.CountDown(g.NCols()) {
						if !yield(x, y) {
							return
						}
					}
				}
			}
		}
	case !invert && colMajor:
		{
			return func(yield func(int, int) bool) {
				for x := range g.NCols() {
					for y := range g.NRows() {
						if !yield(x, y) {
							return
						}
					}
				}
			}
		}
	case invert && colMajor:
		{
			return func(yield func(int, int) bool) {
				for x := range i.CountDown(g.NCols()) {
					for y := range i.CountDown(g.NRows()) {
						if !yield(x, y) {
							return
						}
					}
				}
			}
		}
	default:
		panic("Not implemented")
	}
}
