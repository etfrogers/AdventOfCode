package main

import (
	"fmt"
	"slices"
	"strings"
	"utils"

	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/path"
	"gonum.org/v1/gonum/graph/simple"
	"gonum.org/v1/gonum/graph/traverse"
)

const Y_FACTOR int = 10_000_000

type Pipeline struct {
	startPos graph.Node
	*simple.UndirectedGraph
}

type xyNode struct {
	x int
	y int
}

func (n xyNode) ID() (id int64) {
	return GenerateID(n.x, n.y)
}

func GenerateID(x, y int) (id int64) {
	return int64(y*Y_FACTOR + x)
}

func NewPipeline(lines []string) Pipeline {
	p := Pipeline{}
	p.UndirectedGraph = simple.NewUndirectedGraph()

	// First add nodes
	for y, line := range lines {
		chars := strings.Split(line, "")
		for x, char := range chars {
			node := xyNode{x, y}
			var north, south, east, west graph.Node
			north = xyNode{x, y - 1}
			south = xyNode{x, y + 1}
			east = xyNode{x + 1, y}
			west = xyNode{x - 1, y}

			var edge1, edge2 graph.Edge
			switch char {
			case "|":
				edge1 = p.NewEdge(node, north)
				edge2 = p.NewEdge(node, south)
			case "-":
				edge1 = p.NewEdge(node, east)
				edge2 = p.NewEdge(node, west)
			case "L":
				edge1 = p.NewEdge(node, north)
				edge2 = p.NewEdge(node, east)
			case "J":
				edge1 = p.NewEdge(node, north)
				edge2 = p.NewEdge(node, west)
			case "7":
				edge1 = p.NewEdge(node, south)
				edge2 = p.NewEdge(node, west)
			case "F":
				edge1 = p.NewEdge(node, south)
				edge2 = p.NewEdge(node, east)
			case ".":
				// do nothing
				continue // to avoid adding edges
			case "S":
				// add nothing to graph: edge should have been added by other nodes
				p.startPos = node
				p.AddNode(node)
				continue // to avoid adding edges
			default:
				panic("unexpected value")
			}
			// No need to add Nodes explicitly: adding edges implicitly adds the end nodes
			p.SetEdge(edge1)
			p.SetEdge(edge2)
		}
	}
	return p
}

func (p *Pipeline) MaxDistFromStart() int {
	paths := path.DijkstraFrom(p.startPos, p.UndirectedGraph)
	dists := []int{}
	search := traverse.DepthFirst{Visit: func(n graph.Node) {
		dists = append(dists, int(paths.WeightTo(n.ID())))
	}}
	// search all nodes (func will stop when it has visited all)
	until := func(n graph.Node) bool { return false }
	search.Walk(p, p.startPos, until)
	return slices.Max[[]int, int](dists)
}

func main() {
	lines := utils.ReadInput()
	fmt.Println(lines)
	part1Answer := 0
	fmt.Printf("Day 10, Part 1 answer: %d\n", part1Answer)
}
