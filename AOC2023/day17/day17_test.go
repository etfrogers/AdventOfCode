package main

import (
	"strings"
	"testing"
	"utils"

	"github.com/stretchr/testify/assert"
)

var testCase string = `2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533`

var testCase2 string = `111111111111
999999999991
999999999991
999999999991
999999999991`

var testLines []string = strings.Split(testCase, "\n")
var testLines2 []string = strings.Split(testCase2, "\n")

func TestPathLen(t *testing.T) {
	m := NewMap(testLines)
	loss := m.leastLoss(false)
	assert.Equal(t, 102, loss)
}

func TestPart1(t *testing.T) {
	lines := utils.ReadInput()
	m := NewMap(lines)
	part1Answer := m.leastLoss(false)
	assert.Equal(t, 1099, part1Answer)
}

func TestUltra(t *testing.T) {
	m := NewMap(testLines)
	loss := m.leastLoss(true)
	assert.Equal(t, 94, loss)

	m2 := NewMap(testLines2)
	loss = m2.leastLoss(true)
	assert.Equal(t, 71, loss)
}
