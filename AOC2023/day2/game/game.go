package game

import (
	"regexp"
	"strconv"
	"strings"
)

type Game struct {
	ID     int
	Phases []Phase
}

var header_regexp *regexp.Regexp = regexp.MustCompile(`(Game )(\d+)`)
var event_regexp *regexp.Regexp = regexp.MustCompile(`(\d+) (\w+)`)

func Check(e error) {
	if e != nil {
		panic(e)
	}
}

func GameFromLine(line string) Game {
	tokens := strings.Split(line, ":")
	header := tokens[0]
	data := tokens[1]
	matches := header_regexp.FindStringSubmatch(header)
	if matches[1] != "Game " {
		panic("Unexpected header")
	}
	id, err := strconv.Atoi(matches[2])
	Check(err)
	phases := PhasesFromString(data)
	return Game{ID: id, Phases: phases}
}

func GameSliceFromLines(lines []string) []Game {
	return Map(lines, GameFromLine)
}

func (g *Game) NPhases() int {
	return len(g.Phases)
}

func (g *Game) IsValid(bag Phase) bool {
	for _, phase := range g.Phases {
		for key, val := range bag {
			if phase[key] > val {
				return false
			}
		}
	}
	return true
}

type Phase map[Color]int

func PhasesFromString(data string) []Phase {
	tokens := strings.Split(data, ";")
	phases := Map(tokens, PhaseFromString)
	return phases
}

func PhaseFromString(str string) Phase {
	phase := Phase{}
	tokens := strings.Split(str, ",")
	for _, token := range tokens {
		matches := event_regexp.FindStringSubmatch(token)
		number, ok := strconv.Atoi(matches[1])
		Check(ok)
		color := ColorFromString(matches[2])
		phase[color] = number
	}
	return phase
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

func Map[T, V any](ts []T, fn func(T) V) []V {
	result := make([]V, len(ts))
	for i, t := range ts {
		result[i] = fn(t)
	}
	return result
}
