package grid

import (
	"fmt"
	"slices"
	"utils"
)

type Grid[E any] [][]E

func (g *Grid[E]) Get(x, y int) E {
	return (*g)[y][x]
}

func (g *Grid[E]) GetRow(y int) *[]E {
	return &(*g)[y]
}

func (g *Grid[E]) GetCol(x int) []E {
	col := make([]E, len(*g))
	for i := range *g {
		col[i] = (*g)[i][x]
	}
	return col
}

func (g *Grid[E]) InsertRow(y int, data []E) {
	if len(data) != g.NCols() {
		panic(fmt.Errorf("Length of new data was %d. Existing row length is %d. These values must match",
			len(data), g.NRows()))
	}
	*g = slices.Insert(*g, y, data)
}

func (g *Grid[E]) NCols() int {
	return len((*g)[0])
}

func (g *Grid[E]) NRows() int {
	return len(*g)
}

func (g *Grid[E]) Size() (ncols, nrows int) {
	return g.NCols(), g.NRows()
}

func Full[E any](x, y int, content E) Grid[E] {
	g := make(Grid[E], y)
	for i := range g {
		g[i] = utils.FullSlice[[]E](x, content)
	}
	return g
}

func (g *Grid[E]) checkLengths() {
	for i := range *g {
		if len((*g)[i]) != len((*g)[0]) {
			panic("All lines in a grid must have the same length")
		}
	}
}

func New[E any](input [][]E) Grid[E] {
	g := Grid[E](input)
	g.checkLengths()
	return g
}
