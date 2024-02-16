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
	// can assume on off s1.to and s1.from is U, D
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

func (ts *TrenchSquare) connectedToH(other TrenchSquare, useFrom bool) bool {
	if useFrom {
		return ts.moveFromHere.isHorizontal() && ts.moveFromHere == other.moveToHere
	} else {
		return ts.moveToHere.isHorizontal() && ts.moveToHere == other.moveFromHere
	}
}

func (t *Trench) Sort() {
	slices.SortFunc(*t, Compare)
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
		inside := false
		var lastMoveTo, lastMoveFrom direction
		for j, ts := range currLine {
			if ts.moveToHere == 'U' || ts.moveToHere == 'D' || ts.moveFromHere == 'U' || ts.moveFromHere == 'D' {
				// already established that at least one of them is U or D
				// so if both U, or both D, then we are on a vertical line, and we toggle
				toggleInside := ts.moveToHere == ts.moveFromHere

				// the other case we toggle is if the start of oursegment came in from the same
				// direction as we are no wbout to leave it...
				// so: if we came in from up, and go out up
				toggleInside = toggleInside ||
					(lastMoveTo.isVertical() && (lastMoveTo == ts.moveFromHere)) || // covers leftward moving line...
					(lastMoveFrom.isVertical() && (lastMoveFrom == ts.moveToHere))
				lastMoveTo = ts.moveToHere
				lastMoveFrom = ts.moveFromHere
				movedOutside := false
				movedInside := false

				if toggleInside {
					if inside {
						movedOutside = true
					} else {
						movedInside = true
					}
					inside = !inside
				}
				notTouchingNeighbour := j > 0 && currLine[j-1].x+1 != currLine[j].x
				// if movedOutside || (inside && notTouchingNeighbour && !movedInside) {
				if movedOutside && notTouchingNeighbour || (inside && notTouchingNeighbour && !movedInside) {
					// cannot happen on first square
					segmentStartInd := findStartOfSegment(currLine, j)
					if segmentStartInd == 0 {
						continue
					}
					endX := currLine[segmentStartInd].x
					startX := currLine[segmentStartInd-1].x
					area += (endX - startX)
					if render {
						for x_ := range iter.Count(startX+1, endX) {
							if im.Get(x_-im.minx, y-im.miny) == "+" {
								panic("double counting")
							}
							im.Set(x_-im.minx, y-im.miny, "+")
						}
					}
				} else {
					// if !inside {
					area++
					// }
				}
			} else {
				//L or R
				// if !inside {
				area++
				// }
			}

		}
	}
	return area
}

func findStartOfSegment(line []TrenchSquare, startInd int) int {
	segmentStartInd := startInd
	ts := line[startInd]
	if !ts.purelyVertical() {
		useFrom := ts.moveFromHere.isHorizontal()
		for segmentStartInd > 0 &&
			// sameHorzDir(currLine[j], currLine[segmentStartInd-1]) {
			line[segmentStartInd].connectedToH(line[segmentStartInd-1], useFrom) {
			segmentStartInd--
		}
	}
	return segmentStartInd
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
