package direction

import (
	"iter"
	"utils"
)

type Direction int

const (
	NORTH Direction = iota
	EAST
	SOUTH
	WEST
	UP    = NORTH
	DOWN  = SOUTH
	LEFT  = WEST
	RIGHT = EAST
)

var all []Direction = []Direction{NORTH, EAST, SOUTH, WEST}

func All() iter.Seq[Direction] {
	return func(yield func(Direction) bool) {
		for _, d := range all {
			if !yield(d) {
				return
			}
		}
	}
}

var arrows map[Direction]string = map[Direction]string{
	NORTH: "^",
	SOUTH: "v",
	EAST:  ">",
	WEST:  "<",
}

var invArrows map[string]Direction = utils.InvertMap(arrows)

func (d Direction) ToArrowString() string {
	return arrows[d]
}

func FromArrowString(s string) Direction {
	return invArrows[s]
}
