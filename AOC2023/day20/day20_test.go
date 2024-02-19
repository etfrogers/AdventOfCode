package main

import (
	"strings"
	"testing"
	"utils"

	"github.com/stretchr/testify/assert"
)

var testCase1 string = `broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a`

var testCase2 string = `broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output`

var testLines1 []string = strings.Split(testCase1, "\n")
var testLines2 []string = strings.Split(testCase2, "\n")

func TestBuild(t *testing.T) {
	m := BuildMachine(testLines1)
	bc := m.nodes["broadcaster"]
	_, ok := bc.(*Broadcaster)
	assert.True(t, ok)
	assert.Equal(t, []string{"a", "b", "c"}, bc.getOutputs())

	_, ok = m.nodes["a"].(*FlipFlop)
	assert.True(t, ok)
	assert.Equal(t, []string{"b"}, m.nodes["a"].getOutputs())

	_, ok = m.nodes["b"].(*FlipFlop)
	assert.True(t, ok)
	assert.Equal(t, []string{"c"}, m.nodes["b"].getOutputs())

	_, ok = m.nodes["c"].(*FlipFlop)
	assert.True(t, ok)
	assert.Equal(t, []string{"inv"}, m.nodes["c"].getOutputs())

	c, ok := m.nodes["inv"].(*Conjunction)
	assert.True(t, ok)
	assert.Equal(t, []string{"a"}, c.getOutputs())
	assert.Equal(t, Inputs{"c": Low}, c.inputs)
}

func TestCase1Single(t *testing.T) {
	m := BuildMachine(testLines1)
	m.RunCycle()
	for _, name := range []string{"a", "b", "c"} {
		n, ok := m.nodes[name].(*FlipFlop)
		assert.True(t, ok)
		assert.Equal(t, false, n.isOn)
	}
	assert.Equal(t, 8, m.nLow)
	assert.Equal(t, 4, m.nHigh)
}

func TestCase1Multi(t *testing.T) {
	m := BuildMachine(testLines1)
	m.Run(1000)
	assert.Equal(t, "000", m.MemoryState())
	assert.Equal(t, 8000, m.nLow)
	assert.Equal(t, 4000, m.nHigh)
	assert.Equal(t, 32000000, m.Checksum())
}

func TestCase2Multi(t *testing.T) {
	m := BuildMachine(testLines2)
	m.Run(1000)
	assert.Equal(t, 11687500, m.Checksum())
}

func TestPart1(t *testing.T) {
	lines := utils.ReadInput()
	m := BuildMachine(lines)
	m.Run(1000)
	part1Answer := m.Checksum()
	assert.Equal(t, 817896682, part1Answer)
}
