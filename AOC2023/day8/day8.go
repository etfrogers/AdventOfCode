package main

import (
	"fmt"
	"regexp"
	"strings"
	"utils"
)

type Node struct {
	label string
	left  string
	right string
}

type Network map[string]Node

var nodeRe regexp.Regexp = *regexp.MustCompile(`([0-9A-Z]{3}) = \(([0-9A-Z]{3}), ([0-9A-Z]{3})\)`)

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

func (n *Network) Walk(instructions string) int {
	return n.baseWalk(instructions, "AAA", func(s string) bool { return s == "ZZZ" }, nil)
}

func (n *Network) baseWalk(instructions, start string, stopper func(string) bool, c chan int) (pathLength int) {
	instInd := 0
	pathLength = 0
	label := start
	for !stopper(label) {
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
	if c != nil {
		c <- pathLength
	}
	return
}

func (n *Network) GhostWalk(instructions string) (pathLength int) {
	labels := utils.Filter(utils.MapKeys(*n), func(k string) bool { return strings.HasSuffix(k, "A") })
	c := make(chan int, len(labels))
	for _, label := range labels {
		go n.baseWalk(instructions, label, func(k string) bool { return strings.HasSuffix(k, "Z") }, c)
	}
	lengths := make([]int, len(labels))
	for i := range labels {
		lengths[i] = <-c
	}
	return utils.LCM(lengths...)
}

func main() {
	lines := utils.ReadInput()
	inst, net := NewNetwork(lines)
	part1Answer := net.Walk(inst)
	fmt.Printf("Day 8, Part 1 answer: %d\n", part1Answer)
	part2Answer := net.GhostWalk(inst)
	fmt.Printf("Day 8, Part 2 answer: %d\n", part2Answer)
}
