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
	dists    map[int64]int
	mainLoop simple.UndirectedGraph
	tiles    [][]string
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
	p := Pipeline{
		dists:         map[int64]int{},
		mainLoop:      *simple.NewUndirectedGraph(),
		DirectedGraph: simple.NewDirectedGraph(),
	}

	p.tiles = make([][]string, len(lines))
	for y, line := range lines {
		p.tiles[y] = strings.Split(line, "")
	}
	p.buildInitialGraph()
	p.buildDistsAndMainLoop()
	return p
}

func (p *Pipeline) buildInitialGraph() {
	for y, line := range p.tiles {
		for x, char := range line {
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
}

type NetWalker struct {
	*traverse.BreadthFirst
	from graph.Node
}

func NewNetWalker(p *Pipeline) NetWalker {
	nw := NetWalker{}
	dist := 0
	nw.BreadthFirst = &traverse.BreadthFirst{
		Visit: func(n graph.Node) {
			p.dists[n.ID()] = dist
			if nw.from != nil {
				edge := p.NewEdge(nw.from, n)
				p.mainLoop.SetEdge(edge)
			}
		},
		Traverse: func(e graph.Edge) bool {
			// only traverse an edge if there is also an edge back
			nw.from = e.From()
			dist = p.dists[e.From().ID()] + 1
			return p.HasEdgeFromTo(e.To().ID(), e.From().ID())
		},
	}
	return nw
}

func (nw *NetWalker) Walk(g *Pipeline, from graph.Node) {
	until := func(graph.Node, int) bool { return false }
	nw.BreadthFirst.Walk(g, from, until)
}

func (p *Pipeline) buildDistsAndMainLoop() {
	search := NewNetWalker(p)
	search.Walk(p, p.startPos)

	// After the walk, the last node from each direction is not connected,
	// so find the two node with only one edge and connect them
	mainNodes := p.mainLoop.Nodes()
	oneEdgeNodes := make([]graph.Node, 2)
	oneEdgeNodeCounter := 0
	for mainNodes.Next() {
		n := mainNodes.Node()
		edges := p.mainLoop.From(n.ID())
		nEdges := edges.Len()
		switch nEdges {
		case 2:
			// Expected - do nothing
		case 1:
			oneEdgeNodes[oneEdgeNodeCounter] = n
			oneEdgeNodeCounter++
			if oneEdgeNodeCounter > 2 {
				panic("Too many unmatched nodes")
			}
		default:
			panic("Node with unexpected number of edges")
		}
	}
	p.mainLoop.SetEdge(p.NewEdge(oneEdgeNodes[0], oneEdgeNodes[1]))

}

func (p *Pipeline) MaxDistFromStart() int {
	maxDist := 0
	for _, v := range p.dists {
		if v > maxDist {
			maxDist = v
		}
	}
	return maxDist
}

func (p *Pipeline) EnclosedArea() int {
	return 0
}

func main() {
	lines := utils.ReadInput()
	p := NewPipeline(lines)
	part1Answer := p.MaxDistFromStart()
	fmt.Printf("Day 10, Part 1 answer: %d\n", part1Answer)
}
