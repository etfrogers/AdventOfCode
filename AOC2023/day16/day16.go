package main

import (
	"fmt"
	"utils"
	"utils/counter"
	"utils/grid"
	"utils/iter"
	"utils/stack"
)

type Layout struct {
	grid.Grid[Tile]
}

type Tile struct {
	energised bool
	lightFlow LightDir
	cat       Category
}

type LightDir int

const (
	NO_LIGHT LightDir = iota
	UP
	DOWN
	LEFT
	RIGHT
)

type Category int

const (
	EMPTY Category = iota
	MIRROR_LD
	MIRROR_RD
	H_SPLITTER
	V_SPLITTER
)

type Beam struct {
	x, y int
	dir  LightDir
}

func BuildLayout(lines []string) Layout {
	g := grid.NewFromStrings(lines)
	layout := grid.Map[string, Tile](&g, TileFromString)
	return Layout{layout}
}

func StrToCategory(s string) Category {
	switch s {
	case ".":
		return EMPTY
	case "-":
		return H_SPLITTER
	case "|":
		return V_SPLITTER
	case "/":
		return MIRROR_LD
	case `\`:
		return MIRROR_RD
	default:
		panic(fmt.Errorf("unexpected string: %s", s))
	}
}

func TileFromString(s string) Tile {
	return Tile{
		cat:       StrToCategory(s),
		lightFlow: NO_LIGHT,
		energised: false,
	}
}

func (b *Beam) Move() {
	switch b.dir {
	case LEFT:
		b.x--
	case RIGHT:
		b.x++
	case UP:
		b.y--
	case DOWN:
		b.y++
	default:
		panic("unexpected value")
	}
}

func (b *Beam) isInside(layout *Layout) bool {
	return (b.x >= 0) &&
		(b.x < layout.NCols()) &&
		b.y >= 0 &&
		b.y < layout.NRows()
}

var NIL_BEAM Beam = Beam{-1, -1, NO_LIGHT}

func (l *Layout) Illuminate(initBeam Beam) {
	beams := stack.New[Beam]()
	beams.Push(initBeam)
	for beams.Len() > 0 {
		beam, _ := beams.Pop()
		for beam.isInside(l) {
			tile := l.Get(beam.x, beam.y)
			newBeam := tile.Interact(&beam)
			l.Set(beam.x, beam.y, tile)
			if beam.dir == NO_LIGHT {
				// delete beam as it would create a loop
				break
			}
			if newBeam != NIL_BEAM {
				beams.Push(newBeam)
			}
			beam.Move()

		}
	}
}

func (t *Tile) Interact(beam *Beam) Beam {
	newBeam := NIL_BEAM
	t.energised = true
	if t.lightFlow == beam.dir {
		beam.dir = NO_LIGHT
		return NIL_BEAM
	}
	t.lightFlow = beam.dir
	switch t.cat {
	case EMPTY:
		// do nothing
	case H_SPLITTER:
		// no effect on LEFT/RIGHT
		if beam.dir == UP || beam.dir == DOWN {
			beam.dir = LEFT // arbitrarily - as long as the new beam goes in the other direction
			newBeam = Beam{beam.x, beam.y, RIGHT}

		}
	case V_SPLITTER:
		// no effect on UP/DOWN
		if beam.dir == LEFT || beam.dir == RIGHT {
			beam.dir = UP // arbitrarily - as long as the new beam goes in the other direction
			newBeam = Beam{beam.x, beam.y, DOWN}
		}
	case MIRROR_LD:
		switch beam.dir {
		case LEFT:
			beam.dir = DOWN
		case DOWN:
			beam.dir = LEFT
		case UP:
			beam.dir = RIGHT
		case RIGHT:
			beam.dir = UP
		default:
			panic("unexpected value")
		}
	case MIRROR_RD:
		switch beam.dir {
		case RIGHT:
			beam.dir = DOWN
		case DOWN:
			beam.dir = RIGHT
		case UP:
			beam.dir = LEFT
		case LEFT:
			beam.dir = UP
		default:
			panic("unexpected value")
		}

	default:
		panic("unexpected value")
	}
	return newBeam
}

func (l *Layout) EnergisedString() string {
	newGrid := grid.Map[Tile, string](&l.Grid, func(e Tile) string {
		if e.energised {
			return "#"
		} else {
			return "."
		}
	})
	return newGrid.String()
}

func (l *Layout) NEnergised() int {
	counts := counter.FromIter(iter.Map[Tile, bool](func(t Tile) bool { return t.energised }, l.Iterator()))
	return counts.Get(true)
}

type BeamScore struct {
	beam  Beam
	score int
}

func (l *Layout) MostEnergetic() BeamScore {
	/*
		x := -1
		topRowIt := iter.NewNext[Beam](func() (Beam, bool) {
			x++
			return Beam{x, 0, DOWN}, x < l.NCols()
		})
		x = -1
		bottomRowIt := iter.NewNext[Beam](func() (Beam, bool) {
			x++
			return Beam{x, l.NRows() - 1, UP}, x < l.NCols()
		})

			y := 0
			leftColIt := iter.NewNext[Beam](func() (Beam, bool) {
				y++
				return Beam{0, y, RIGHT}, x < l.NRows()
			})
			y = 0
			rightColIt := iter.NewNext[Beam](func() (Beam, bool) {
				y++
				return Beam{l.NCols() - 1, y, LEFT}, x < l.NRows()
			})*/

	beams := make([]Beam, (l.NCols()+l.NRows())*2)
	i := 0
	for x := 0; x < l.NCols(); x++ {
		beams[i] = Beam{x, 0, DOWN}
		i++
		beams[i] = Beam{x, l.NRows() - 1, UP}
		i++
	}
	for y := 0; y < l.NRows(); y++ {
		beams[i] = Beam{0, y, RIGHT}
		i++
		beams[i] = Beam{l.NCols() - 1, y, LEFT}
		i++
	}

	// beamIt := iter.Chain(topRowIt, bottomRowIt)
	// fmt.Println(iter.ToSlice(beamIt))

	scores := utils.Map(beams, func(b Beam) BeamScore {
		testLayout := Layout{l.Clone()}
		testLayout.Illuminate(b)
		score := testLayout.NEnergised()
		return BeamScore{b, score}
	})

	beamScore := iter.MaxFunc(iter.FromSlice(scores), func(bs1, bs2 BeamScore) bool { return bs1.score < bs2.score })
	return beamScore
}

func main() {
	lines := utils.ReadInput()
	layout := BuildLayout(lines)
	layout.Illuminate(Beam{0, 0, RIGHT})
	part1Answer := layout.NEnergised()
	fmt.Printf("Day 16, Part 1 answer: %d\n", part1Answer)

	layout = BuildLayout(lines)
	maxBeam := layout.MostEnergetic()
	part2Answer := maxBeam.score
	fmt.Printf("Day 16, Part 2 answer: %d\n", part2Answer)

}
