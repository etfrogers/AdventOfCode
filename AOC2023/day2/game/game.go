package game

import (
	"regexp"
	"strconv"
	"strings"
	"utils"
)

type Game struct {
	ID     int
	Phases []Phase
}

var header_regexp *regexp.Regexp = regexp.MustCompile(`(Game )(\d+)`)
var event_regexp *regexp.Regexp = regexp.MustCompile(`(\d+) (\w+)`)

func GameFromLine(line string) Game {
	tokens := strings.Split(line, ":")
	header := tokens[0]
	data := tokens[1]
	matches := header_regexp.FindStringSubmatch(header)
	if matches[1] != "Game " {
		panic("Unexpected header")
	}
	id, err := strconv.Atoi(matches[2])
	utils.Check(err)
	phases := PhasesFromString(data)
	return Game{ID: id, Phases: phases}
}

func GameSliceFromLines(lines []string) []Game {
	return utils.Map(lines, GameFromLine)
}

func (g *Game) NPhases() int {
	return len(g.Phases)
}

func (g *Game) IsValid(bag Bag) bool {
	for _, phase := range g.Phases {
		for key, val := range bag {
			if phase[key] > val {
				return false
			}
		}
	}
	return true
}

func (g *Game) MinBag() Bag {
	bag := Bag{}
	for _, phase := range g.Phases {
		for key, val := range phase {
			if val > bag[key] {
				bag[key] = val
			}
		}
	}
	return bag
}

func (g *Game) MinBagPower() int {
	return g.MinBag().Power()
}

type Phase map[Color]int
type Bag Phase

func PhasesFromString(data string) []Phase {
	tokens := strings.Split(data, ";")
	phases := utils.Map(tokens, PhaseFromString)
	return phases
}

func PhaseFromString(str string) Phase {
	phase := Phase{}
	tokens := strings.Split(str, ",")
	for _, token := range tokens {
		matches := event_regexp.FindStringSubmatch(token)
		number, ok := strconv.Atoi(matches[1])
		utils.Check(ok)
		color := ColorFromString(matches[2])
		phase[color] = number
	}
	return phase
}

func (b Bag) Power() int {
	return b[Red] * b[Green] * b[Blue]
}

type Color int

const (
	Red   Color = iota
	Green Color = iota
	Blue  Color = iota
)

var colorMap = map[string]Color{
	"red":   Red,
	"green": Green,
	"blue":  Blue,
}

func ColorFromString(str string) Color {
	val, ok := colorMap[str]
	if !ok {
		panic("Invalid value passed to ColorFromString")
	}
	return val
}
