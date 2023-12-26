package main

import (
	"fmt"
	"slices"
	"strconv"
	"strings"
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

type MapSet struct {
	SeedNumbers set.Set[int]
	Maps        []LocationMap
}

func AtoiError(x string) int {
	v, e := strconv.Atoi(x)
	utils.Check(e)
	return v
}

func NewMapSet(data []string) MapSet {
	tokens := utils.SplitSplice(data, "")
	seeds_slice := tokens[0]
	seeds_str := seeds_slice[0]
	seed_header, seeds_str, found := strings.Cut(seeds_str, ":")
	if !found || seed_header != "seeds" {
		panic(fmt.Errorf("failed to extract seed header"))
	}
	seed_tokens := utils.DropEmpty(strings.Split(seeds_str, " "))
	seed_slice := utils.Map[string, int](seed_tokens, AtoiError)
	seeds := set.New(seed_slice...)

	map_tokens := tokens[1:]
	maps := utils.Map[[]string, LocationMap](map_tokens, NewLocationMap)
	return MapSet{SeedNumbers: seeds, Maps: maps}
}

func NewLocationMap(data []string) LocationMap {
	header := data[0]
	maps_slice := data[1:]
	id, label, found := strings.Cut(header, " ")
	if !found || label != "map:" {
		panic(fmt.Errorf("failed to extract map header"))
	}
	map_strs := utils.Map[string, []string](maps_slice, func(s string) []string { return strings.Split(s, " ") })
	map_ints := utils.Map(map_strs, func(x []string) []int { return utils.Map[string, int](x, AtoiError) })
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

func (m MapSet) MapThroughSet(input int) int {
	val := input
	for _, map_ := range m.Maps {
		val = map_.DoMapping(val)
	}
	return val
}

func FindLocations(maps MapSet) set.Set[int] {
	slice := utils.Map[int, int](maps.SeedNumbers.Items(), maps.MapThroughSet)
	return set.New(slice...)
}

func main() {
	lines := utils.ReadInput()
	maps := NewMapSet(lines)
	locs := FindLocations(maps)
	part1Answer := slices.Min(locs.Items())
	fmt.Printf("Day 5, Part 1 answer: %d\n", part1Answer)
}
