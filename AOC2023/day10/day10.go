package main

import (
	"fmt"
	"strings"
	"utils"

	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/simple"
	"gonum.org/v1/gonum/graph/traverse"
)

const Y_FACTOR int = 10_000_000

type Pipeline struct {
	startPos graph.Node
	*simple.DirectedGraph
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
	p.DirectedGraph = simple.NewDirectedGraph()

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
				if p.Node(node.ID()) == nil {
					p.AddNode(node)
				}
				continue // to avoid adding edges
			default:
				panic("unexpected value")
			}
			// No need to add Nodes explicitly: adding edges implicitly adds the end nodes
			p.SetEdge(edge1)
			p.SetEdge(edge2)
		}
	}
	// Add edges out from startPos
	toStart := p.To(p.startPos.ID())
	if toStart.Len() != 2 {
		panic("wrong number of connections to start")
	}
	for toStart.Next() {
		n := toStart.Node()
		edge := p.NewEdge(p.startPos, n)
		p.SetEdge(edge)
	}
	return p
}

func (p *Pipeline) MaxDistFromStart() int {
	dists := map[int64]int{}
	dist := 0
	search := traverse.BreadthFirst{
		Visit: func(n graph.Node) {
			dists[n.ID()] = dist
		},
		Traverse: func(e graph.Edge) bool {
			// only traverse an edge if there is also an edge back
			dist = dists[e.From().ID()] + 1
			return p.HasEdgeFromTo(e.To().ID(), e.From().ID())

		},
	}
	// search all nodes (func will stop when it has visited all)
	until := func(graph.Node, int) bool { return false }
	search.Walk(p, p.startPos, until)
	maxDist := 0
	for _, v := range dists {
		if v > maxDist {
			maxDist = v
		}
	}
	return maxDist
}

func main() {
	lines := utils.ReadInput()
	p := NewPipeline(lines)
	part1Answer := p.MaxDistFromStart()
	fmt.Printf("Day 10, Part 1 answer: %d\n", part1Answer)
}
