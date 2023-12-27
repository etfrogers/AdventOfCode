package main

import (
	"fmt"
	"slices"
	"strings"
	"sync"
	"utils"
	"utils/set"
)

type LocationMap struct {
	Id       string
	mappings []Mapping
}

type Mapping struct {
	OutputStart int
	InputStart  int
	Length      int
}

func (m *Mapping) InputEnd() int {
	return m.InputStart + m.Length
}

func (m *Mapping) OutputEnd() int {
	return m.OutputStart + m.Length
}

type MapSetRanges struct {
	SeedRanges [][2]int
	maps       []LocationMap
}

type MapSetInts struct {
	SeedNumbers *set.Set[int]
	maps        []LocationMap
}

type MapSet interface {
	Maps() []LocationMap
	// MapThroughSet(MapSet, int) int
}

func (m MapSetInts) Maps() []LocationMap {
	return m.maps
}

func (m MapSetRanges) Maps() []LocationMap {
	return m.maps
}

func NewMapSet(data []string, withRanges bool) MapSet {
	tokens := utils.SplitSplice(data, "")
	seeds_slice := tokens[0]
	seeds_str := seeds_slice[0]
	seed_header, seeds_str, found := strings.Cut(seeds_str, ":")
	if !found || seed_header != "seeds" {
		panic(fmt.Errorf("failed to extract seed header"))
	}
	seed_tokens := utils.DropEmpty(strings.Split(seeds_str, " "))
	seed_slice := utils.Map[string, int](seed_tokens, utils.AtoiError)

	map_tokens := tokens[1:]
	maps := utils.Map[[]string, LocationMap](map_tokens, NewLocationMap)
	if withRanges {
		seeds := make([][2]int, len(seed_slice)/2)

		for i := 0; i < len(seed_slice)/2; i++ {
			j := i * 2
			seeds[i] = [2]int{seed_slice[j], seed_slice[j+1]}
		}
		return MapSetRanges{SeedRanges: seeds, maps: maps}
	} else {
		seeds := set.New(seed_slice...)
		return MapSetInts{SeedNumbers: seeds, maps: maps}
	}

}

func NewLocationMap(data []string) LocationMap {
	header := data[0]
	maps_slice := data[1:]
	id, label, found := strings.Cut(header, " ")
	if !found || label != "map:" {
		panic(fmt.Errorf("failed to extract map header"))
	}
	map_strs := utils.Map[string, []string](maps_slice, func(s string) []string { return strings.Split(s, " ") })
	map_ints := utils.Map(map_strs, func(x []string) []int { return utils.Map[string, int](x, utils.AtoiError) })
	maps := utils.Map[[]int, Mapping](map_ints, func(i []int) Mapping { return Mapping{i[0], i[1], i[2]} })
	return LocationMap{Id: id, mappings: maps}
}

func (m LocationMap) DoMapping(input int) int {
	found := false
	var output int
	for _, entry := range m.mappings {
		if input >= entry.InputStart && input < entry.InputEnd() {
			found = true
			offset := input - entry.InputStart
			output = entry.OutputStart + offset
		}
	}
	if !found {
		output = input
	}
	return output
}

func MapThroughSet(m MapSet, input int) int {
	val := input
	for _, map_ := range m.Maps() {
		val = map_.DoMapping(val)
	}
	return val
}

func FindLocations(maps MapSetInts) *set.Set[int] {
	slice := utils.Map[int, int](maps.SeedNumbers.Items(), func(x int) int { return MapThroughSet(maps, x) })
	return set.New[int](slice...)
}

const MaxInt = int(^uint(0) >> 1)

func processSeedPair(wg *sync.WaitGroup, label int, pair [2]int, mapSet *MapSetRanges, outputSet *set.Set[int]) {
	fmt.Println(label)
	minLoc := MaxInt
	rangeStart := pair[0]
	rangeLen := pair[1]
	for i := 0; i < rangeLen; i++ {
		input := rangeStart + i
		loc := MapThroughSet(mapSet, input)
		if loc < minLoc {
			minLoc = loc
		}
	}
	outputSet.Add(minLoc)
	wg.Done()
}

func MinLoc(maps MapSet) int {
	locs := set.New[int]()
	switch m := maps.(type) {
	case MapSetInts:
		locs = FindLocations(m)
	case MapSetRanges:
		var wg sync.WaitGroup
		for pair_number, seed_pair := range m.SeedRanges {
			wg.Add(1)
			go processSeedPair(&wg, pair_number, seed_pair, &m, locs)
		}
		wg.Wait()
	}
	return slices.Min(locs.Items())
}

func main() {
	lines := utils.ReadInput()
	maps := NewMapSet(lines, false)
	part1Answer := MinLoc(maps)
	fmt.Printf("Day 5, Part 1 answer: %d\n", part1Answer)

	maps2 := NewMapSet(lines, true)
	part2Answer := MinLoc(maps2)
	fmt.Printf("Day 5, Part 2 answer: %d\n", part2Answer)
}
