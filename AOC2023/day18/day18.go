package main

import (
	"fmt"
	"regexp"
	"slices"
	"utils"
	"utils/grid"
	"utils/iter"
)

type Instruction struct {
	dir       direction
	len       int
	colorCode string
}

type InstructionSet []Instruction

type image struct {
	grid.Grid[string]
	minx, miny int
}

type direction rune

type TrenchSquare struct {
	x, y         int
	colorCode    string
	moveToHere   direction
	moveFromHere direction
}

type Trench []TrenchSquare

var instRe = regexp.MustCompile(`(L|R|U|D) (\d+) \(\#([0-9a-f]{6})\)`)

func NewInstruction(line string) Instruction {
	tokens := instRe.FindStringSubmatch(line)
	var dir direction
	if len(tokens[1]) == 1 {
		dir = direction(tokens[1][0])
	} else {
		panic("failed to find dir")
	}
	len := utils.AtoiError(tokens[2])
	code := tokens[3]
	return Instruction{dir, len, code}
}

func BuildInstructions(lines []string) InstructionSet {
	return utils.Map(lines, NewInstruction)
}

func (is *InstructionSet) Walk() Trench {
	t := make(Trench, 0)
	x, y := 0, 0
	for i, inst := range *is {
		for j := range inst.len {
			switch inst.dir {
			case 'U':
				y--
			case 'D':
				y++
			case 'L':
				x--
			case 'R':
				x++
			}
			var nextMove direction
			if j == inst.len-1 {
				nextInd := (i + 1) % len(*is)
				nextMove = (*is)[nextInd].dir
			} else {
				nextMove = inst.dir
			}
			t = append(t, TrenchSquare{x, y, inst.colorCode, inst.dir, nextMove})
		}
	}
	return t
}

func Compare(ts1, ts2 TrenchSquare) int {
	switch {
	case ts1.y < ts2.y:
		return -1
	case ts1.y > ts2.y:
		return 1
	default:
		// ys are equal
		switch {
		case ts1.x < ts2.x:
			return -1
		case ts1.x > ts2.x:
			return 1
		default:
			panic("equal squares should not occur")
		}
	}
}

func sameHorzDir(s1, s2 TrenchSquare) bool {
	// can assume one off s1.to and s1.from is U, D
	to1, to2 := s1.moveToHere, s2.moveToHere
	if to1.isHorizontal() {
		return to1 == to2
	}
	from1, from2 := s1.moveFromHere, s2.moveFromHere
	if from1.isHorizontal() {
		return from1 == from2
	}
	panic("unexpected state")
}

func (d direction) isVertical() bool {
	return d == 'U' || d == 'D'
}
func (d direction) isHorizontal() bool {
	return d == 'L' || d == 'R'
}
func (d direction) invert() direction {
	switch d {
	case 'U':
		return 'D'
	case 'D':
		return 'U'
	case 'L':
		return 'R'
	case 'R':
		return 'L'
	default:
		panic("invalid value")
	}
}

func (ts *TrenchSquare) purelyVertical() bool {
	return ts.moveFromHere.isVertical() && ts.moveToHere.isVertical()
}
func (ts *TrenchSquare) purelyHorizontal() bool {
	return ts.moveFromHere.isHorizontal() && ts.moveToHere.isHorizontal()
}

func (ts *TrenchSquare) verticalComponent() direction {
	switch {
	case ts.purelyVertical():
		panic("cannot return vertical component for purely vertical square")
	case ts.moveFromHere.isVertical():
		return ts.moveFromHere
	case ts.moveToHere.isVertical():
		return ts.moveToHere
	default:
		panic("square does not have a vertical component")
	}
}

func haveSameVerticalComponents(ts1, ts2 TrenchSquare) bool {
	// Can assume that exactly one component of each is vertical
	return ts1.verticalComponent() == ts2.verticalComponent()

}

func (t *Trench) Sort() {
	slices.SortFunc(*t, Compare)
}

type Segment struct {
	crossing bool
	start    int
	len      int
}

func (s Segment) end() int {
	return s.start + s.len - 1
}

func (t *Trench) FilledArea(args ...image) int {
	render := false
	var im image
	switch len(args) {
	case 0:
		//do nothing
	case 1:
		render = true
		im = args[0]
	default:
		panic("incorrect args")
	}
	area := 0
	t.Sort()
	i := 0
	for i < len(*t) {
		startI := i
		y := (*t)[i].y
		for i < len(*t) && (*t)[i].y == y {
			i++
		}
		currLine := (*t)[startI:i]

		segments := make([]Segment, 0, len(currLine))
		for j := 0; j < len(currLine); j++ {
			ts := currLine[j]
			segment := Segment{start: ts.x, len: 1}
			if ts.purelyVertical() {
				segment.crossing = true
			} else {
				segment.len = 2
				for currLine[j+segment.len-1].purelyHorizontal() {
					segment.len++
				}
				segment.crossing = haveSameVerticalComponents(currLine[j], currLine[j+segment.len-1])
			}
			segments = append(segments, segment)
			j += segment.len - 1
		}

		inside := false
		for j, seg := range segments {
			// cannot happen on first segment
			if inside {
				precEndX := seg.start
				precStartX := segments[j-1].end() + 1
				area += (precEndX - precStartX)
				if render {
					for x_ := range iter.Count(precStartX+1, precEndX) {
						if im.Get(x_-im.minx, y-im.miny) == "+" {
							panic("double counting")
						}
						im.Set(x_-im.minx, y-im.miny, "+")
					}
				}
			}
			area += seg.len
			if seg.crossing {
				inside = !inside
			}

		}
	}
	return area
}

func (t *Trench) buildImage() image {
	t.Sort()
	miny := (*t)[0].y
	maxy := (*t)[len(*t)-1].y
	xs := utils.Map(*t, func(v TrenchSquare) int { return v.x })
	maxx := slices.Max(xs)
	minx := slices.Min(xs)
	sx := (maxx - minx) + 1
	sy := (maxy - miny) + 1
	g := grid.Full(sx, sy, ".")
	for _, s := range *t {
		g.Set(s.x-minx, s.y-miny, "#")
	}
	return image{g, minx, miny}
}

func printImage(g image) {
	fmt.Println()
	fmt.Println(g.String())

}

func (t *Trench) Render() {
	printImage(t.buildImage())
}

func main() {
	lines := utils.ReadInput()
	is := BuildInstructions(lines)
	tr := is.Walk()
	im := tr.buildImage()
	part1Answer := tr.FilledArea(im)
	printImage(im)
	fmt.Printf("Day 18, Part 1 answer: %d\n", part1Answer)
}
