package main

import (
	"fmt"
	"regexp"
	"utils"
)

type Node struct {
	label string
	left  string
	right string
}

type Network map[string]Node

var nodeRe regexp.Regexp = *regexp.MustCompile(`([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)`)

func NewNetwork(lines []string) (instructions string, net Network) {
	net = Network{}
	instructionSlice, nodes := utils.CutSlice[string](lines, "")
	instructions = instructionSlice[0]
	for _, nodeStr := range nodes {
		tokens := nodeRe.FindStringSubmatch(nodeStr)
		if tokens == nil {
			panic(fmt.Errorf("failed to match string: %s", nodeStr))
		}
		label, left, right := tokens[1], tokens[2], tokens[3]
		node := Node{label, left, right}
		net[label] = node
	}
	return
}

func (n *Network) Walk(instructions string) (pathLength int) {
	instInd := 0
	pathLength = 0
	label := "AAA"
	for label != "ZZZ" {
		switch string(instructions[instInd]) {
		case "R":
			label = (*n)[label].right
		case "L":
			label = (*n)[label].left
		}
		instInd++
		instInd %= len(instructions)
		pathLength++
	}
	return
}

func main() {
	lines := utils.ReadInput()
	inst, net := NewNetwork(lines)
	part1Answer := net.Walk(inst)
	fmt.Printf("Day 8, Part 1 answer: %d\n", part1Answer)
}
