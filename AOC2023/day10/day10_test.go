package main

import (
	"fmt"
	"strings"
	"testing"
	"utils"
	"utils/set"

	"github.com/stretchr/testify/assert"
	"gonum.org/v1/gonum/graph"
)

var testCase1plain string = `.....
.S-7.
.|.|.
.L-J.
.....`

var testCase1real string = `-L|F7
7S-7|
L|7||
-L-J|
L|-JF`

var testCase2plain string = `..F7.
.FJ|.
SJ.L7
|F--J
LJ...`

var testCase2real string = `7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ`

var testCases []string = []string{testCase1plain, testCase1real, testCase2plain, testCase2real}

var testCaseLines [][]string = utils.Map(testCases, func(s string) []string { return strings.Split(s, "\n") })

func TestPart1(t *testing.T) {
	expected := 6640
	lines := utils.ReadInput()
	p := NewPipeline(lines)
	part1Answer := p.MaxDistFromStart()
	assert.Equal(t, expected, part1Answer)
}

func TestPart2(t *testing.T) {
	expected := 411
	lines := utils.ReadInput()
	p := NewPipeline(lines)
	part2Answer := p.EnclosedArea()
	assert.Equal(t, expected, part2Answer)
}

func TestMaxDist(t *testing.T) {
	expectedDist := []int{4, 4, 8, 8}
	for i, lines := range testCaseLines {
		t.Run(fmt.Sprint(lines), func(t *testing.T) {
			pipes := NewPipeline(lines)
			assert.Equal(t, expectedDist[i], pipes.MaxDistFromStart())
		})
	}
}

func TestMainLoopClean(t *testing.T) {
	testCases := []string{testCase1plain, testCase2plain}
	for _, tc := range testCases {
		t.Run(tc, func(t *testing.T) {
			lines := strings.Split(tc, "\n")
			pipes := NewPipeline(lines)
			assert.True(t, graphsEqual(&pipes.mainLoop, pipes.DirectedGraph))
		})
	}
}

func TestMainLoopDirty(t *testing.T) {
	testCases := []struct {
		clean string
		dirty string
	}{
		{testCase1plain, testCase1real},
		{testCase2plain, testCase2real},
	}
	for i, tc := range testCases {
		t.Run(fmt.Sprint(i), func(t *testing.T) {
			linesClean := strings.Split(tc.clean, "\n")
			pipesClean := NewPipeline(linesClean)
			linesDirty := strings.Split(tc.dirty, "\n")
			pipesDirty := NewPipeline(linesDirty)
			assert.True(t, graphsEqual(&pipesClean.mainLoop, &pipesDirty.mainLoop))
		})
	}
}

func nodeIdSet(g simpleGraph) set.Set[int64] {
	return *set.New(utils.Map(graph.NodesOf(g.Nodes()), func(n graph.Node) int64 { return n.ID() })...)
}

type simpleGraph interface {
	Nodes() graph.Nodes
	Edges() graph.Edges
	HasEdgeBetween(int64, int64) bool
}

func graphsEqual(g1, g2 simpleGraph) bool {
	nodeSet1 := nodeIdSet(g1)
	nodeSet2 := nodeIdSet(g2)
	if !nodeSet1.Equals(&nodeSet2) {
		return false
	}

	edges1 := g1.Edges()
	for edges1.Next() {
		edge := edges1.Edge()
		if !g2.HasEdgeBetween(edge.From().ID(), edge.To().ID()) {
			return false
		}
	}
	return true
}

func TestLoop(t *testing.T) {
	expectedArea := []int{4, 4, 8, 10}
	for i, lines := range testLinesLoop {
		t.Run(fmt.Sprint(lines), func(t *testing.T) {
			pipes := NewPipeline(lines)
			assert.Equal(t, expectedArea[i], pipes.EnclosedArea())
		})
	}
}

func TestLoopPart1Cases(t *testing.T) {
	expectedArea := []int{1, 1, 1, 1}
	for i, lines := range testCaseLines {
		t.Run(fmt.Sprint(lines), func(t *testing.T) {
			pipes := NewPipeline(lines)
			assert.Equal(t, expectedArea[i], pipes.EnclosedArea())
		})
	}
}

func TestCleanup(t *testing.T) {
	testCases := []struct {
		clean string
		dirty string
	}{
		{testCase1plain, testCase1real},
		{testCase2plain, testCase2real},
	}
	for i, tc := range testCases {
		t.Run(fmt.Sprint(i), func(t *testing.T) {
			linesClean := strings.Split(tc.clean, "\n")
			pipesClean := NewPipeline(linesClean)
			pipesClean.CloneTiles()
			pipesClean.CleanupTiles()
			linesDirty := strings.Split(tc.dirty, "\n")
			pipesDirty := NewPipeline(linesDirty)
			pipesDirty.CloneTiles()
			pipesDirty.CleanupTiles()
			assert.Equal(t, pipesClean.markedTiles, pipesDirty.markedTiles)
		})
	}
}

var testLinesLoop [][]string = utils.Map(testCaseLoop, func(s string) []string { return strings.Split(s, "\n") })

var testCaseLoop []string = []string{
	`...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........`,
	`..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........`,
	`.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...`,
	`FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L`,
}
