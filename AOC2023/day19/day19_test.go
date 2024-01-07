package main

import (
	"strings"
	"testing"
	"utils"

	"github.com/stretchr/testify/assert"
)

var testCase string = `px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}`

var testLines []string = strings.Split(testCase, "\n")

func TestBuildItems(t *testing.T) {
	_, items := BuildWorkflowAndItems(testLines)
	assert.Equal(t, 5, len(items))
	assert.Equal(t, Item{787, 2655, 1222, 2876}, items[0])
	assert.Equal(t, Item{2127, 1623, 2188, 1013}, items[4])
}

func TestBuildWorkflow(t *testing.T) {
	rs, _ := BuildWorkflowAndItems(testLines)
	assert.Equal(t, 11, len(rs))
	// hdj{m>838:A,pv}
	assert.Equal(t, Workflow{Rule{Condition{"m", gt, 838}, "A"}, Rule{NIL_CONDITION, "pv"}}, rs["hdj"])
	// rfg{s<537:gd,x>2440:R,A}
	assert.Equal(t, Workflow{
		Rule{Condition{"s", lt, 537}, "gd"},
		Rule{Condition{"x", gt, 2440}, "R"},
		Rule{NIL_CONDITION, "A"}},
		rs["rfg"])
}

func TestDestination(t *testing.T) {
	rs, items := BuildWorkflowAndItems(testLines)
	dests := ProcessItems(items, rs)
	expected := []Status{ACCEPTED, REJETECTED, ACCEPTED, REJETECTED, ACCEPTED}
	assert.Equal(t, expected, dests)
}

func TestRatings(t *testing.T) {
	expected := []int{7540, 4623, 6951}
	rs, items := BuildWorkflowAndItems(testLines)
	assert.Equal(t, expected, ProcessedRatings(items, rs))
}

func TestTotalRatings(t *testing.T) {
	expected := 19114
	rs, items := BuildWorkflowAndItems(testLines)
	assert.Equal(t, expected, TotalRatings(items, rs))
}

func TestPart1(t *testing.T) {
	expected := 409898
	lines := utils.ReadInput()
	rs, items := BuildWorkflowAndItems(lines)
	assert.Equal(t, expected, TotalRatings(items, rs))
}
