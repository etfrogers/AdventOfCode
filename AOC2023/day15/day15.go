package main

import (
	"fmt"
	"regexp"
	"strings"
	"utils"

	orderedmap "github.com/wk8/go-ordered-map"
)

func Hash(s string) int {
	hash := 0
	for _, r := range s {
		hash += int(r)
		hash *= 17
		hash %= 256
	}
	return hash
}

func HashSlice(csv string) []int {
	tokens := strings.Split(csv, ",")
	return utils.Map(tokens, Hash)
}

func Checksum(csv string) int {
	return utils.Sum(HashSlice(csv))
}

var cmdRe = regexp.MustCompile(`([a-z]*)([=-])(\d?)`)

type Boxes []orderedmap.OrderedMap
type Lens struct {
	box   int
	slot  int
	label string
	lens  int
}

func FollowManual(csv string) Boxes {
	boxes := make(Boxes, 256)
	for i := range boxes {
		boxes[i] = *orderedmap.New()
	}
	commands := strings.Split(csv, ",")
	for _, cmd := range commands {
		tokens := cmdRe.FindStringSubmatch(cmd)
		label := tokens[1]
		op := tokens[2]
		box_ind := Hash(label)
		switch op {
		case "=":
			lens := utils.AtoiError(tokens[3])
			boxes[box_ind].Set(label, lens)
		case "-":
			boxes[box_ind].Delete(label)
		}
	}
	return boxes
}

func GetLenses(boxes Boxes) []Lens {
	lenses := make([]Lens, 0, 256)
	for box_ind, box := range boxes {
		slot := 1
		for pair := box.Oldest(); pair != nil; pair = pair.Next() {
			lens := Lens{box: box_ind, slot: slot, label: pair.Key.(string), lens: pair.Value.(int)}
			lenses = append(lenses, lens)
			slot++
		}
	}
	return lenses
}

func (l Lens) FocusingPower() int {
	return (l.box + 1) * l.slot * l.lens
}

func FocusingPowers(boxes Boxes) []int {
	lenses := GetLenses(boxes)
	powers := utils.Map(lenses, func(l Lens) int { return l.FocusingPower() })
	return powers
}

func TotalPower(boxes Boxes) int {
	return utils.Sum(FocusingPowers(boxes))
}

func main() {
	input := utils.ReadInput()[0]
	part1Answer := Checksum(input)
	fmt.Printf("Day 15, Part 1 answer: %d\n", part1Answer)

	boxes := FollowManual(input)
	part2Answer := TotalPower(boxes)
	fmt.Printf("Day 15, Part 2 answer: %d\n", part2Answer)

}
