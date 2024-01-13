package main

import (
	"fmt"
	"utils"
	"utils/counter"
	"utils/grid"
	"utils/set"

	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/simple"
	"gonum.org/v1/gonum/graph/traverse"
)

const Y_FACTOR int = 10_000_000

type Pipeline struct {
	startPos graph.Node
	*simple.DirectedGraph
	dists       map[int64]int
	mainLoop    simple.UndirectedGraph
	tiles       grid.Grid[string]
	markedTiles grid.Grid[string]
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

	p.tiles = grid.NewFromStrings(lines)
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

type direction int

const (
	up direction = iota
	down
	left
	right
)

type TileWalker struct {
	isInside       bool
	isOnPipe       bool
	lastPipeInFrom direction
}

func (w *TileWalker) Reset() {
	w.isInside = false
	w.isOnPipe = false
	w.lastPipeInFrom = up
}

func (w *TileWalker) ToggleInside() {
	w.isInside = !w.isInside
}
func (w *TileWalker) WalkLine(chars []string) {
	for i, char := range chars {
		switch char {
		case "|":
			w.ToggleInside()
		case "-":
			// do nothing
		case "L":
			w.isOnPipe = true
			w.lastPipeInFrom = up
		case "J":
			w.isOnPipe = false
			if w.lastPipeInFrom == down {
				w.ToggleInside()
			}
		case "7":
			w.isOnPipe = false
			if w.lastPipeInFrom == up {
				w.ToggleInside()
			}
		case "F":
			w.isOnPipe = true
			w.lastPipeInFrom = down
		case ".":
			if w.isInside {
				chars[i] = "I"
			} else {
				chars[i] = "O"
			}
		case "S":
			panic("S should have been removed")
		default:
			panic("unexpected value")
		}
	}
}

func (p *Pipeline) CloneTiles() {
	p.markedTiles = p.tiles.Clone()
}

func (p *Pipeline) EnclosedArea() int {
	p.MarkupTiles()
	counter := counter.New[string]()
	for _, line := range p.markedTiles {
		counter.Add(line...)
	}
	return counter.Get("I")
}

func (p *Pipeline) CleanupTiles() {
	for y, line := range p.markedTiles {
		for x := range line {
			id := GenerateID(x, y)
			if n := p.mainLoop.Node(id); n == nil {
				line[x] = "."
			}
			if line[x] == "S" {
				n := p.mainLoop.Node(id)
				canReach := graph.NodesOf(p.mainLoop.From(id))
				if len(canReach) != 2 {
					panic("Unexpected number of connections")
				}
				outDirs := set.New[direction]()
				for _, to := range canReach {
					outDirs.Add(directionFrom(n.(xyNode), to.(xyNode)))
				}
				line[x] = dirPairToChar(outDirs)
			}
		}
	}
}

func dirPairToChar(s *set.Set[direction]) (char string) {
	if s.Len() != 2 {
		panic("wrong number of dirs")
	}
	switch {
	case s.Equals(set.New(up, down)):
		char = "|"
	case s.Equals(set.New(left, right)):
		char = "-"
	case s.Equals(set.New(left, up)):
		char = "J"
	case s.Equals(set.New(left, down)):
		char = "7"
	case s.Equals(set.New(right, up)):
		char = "L"
	case s.Equals(set.New(right, down)):
		char = "F"
	}
	return
}

func directionFrom(node, to xyNode) (dir direction) {
	dx := to.x - node.x
	dy := to.y - node.y
	switch {
	case dx == -1 && dy == 0:
		dir = left
	case dx == 1 && dy == 0:
		dir = right
	case dx == 0 && dy == -1:
		dir = up
	case dx == 0 && dy == 1:
		dir = down
	default:
		panic("Unexpected case")
	}
	return
}

func (p *Pipeline) MarkupTiles() {
	p.CloneTiles()
	p.CleanupTiles()
	w := TileWalker{}
	for _, line := range p.markedTiles {
		w.WalkLine(line)
	}
}

func main() {
	lines := utils.ReadInput()
	p := NewPipeline(lines)
	part1Answer := p.MaxDistFromStart()
	fmt.Printf("Day 10, Part 1 answer: %d\n", part1Answer)
	part2Answer := p.EnclosedArea()
	fmt.Printf("Day 10, Part 2 answer: %d\n", part2Answer)
}
