package main

import (
	"fmt"
	"regexp"
	"strings"
	"utils"
)

var itemRegexp regexp.Regexp = *regexp.MustCompile(`\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}`)
var workflowRegexp regexp.Regexp = *regexp.MustCompile(`(\w+)\{(.*)\}`)
var ruleRegexp regexp.Regexp = *regexp.MustCompile(`(([xmas])([<>])(\d+):)?([ARa-z]*)`)

type Item struct {
	x, m, a, s int
}

type Op int

const (
	lt Op = iota
	gt
)

type Condition struct {
	name  string
	op    Op
	value int
}

var NIL_CONDITION Condition = Condition{}

type Status string

const (
	ACCEPTED   Status = "A"
	REJETECTED Status = "R"
	NIL_STATUS Status = ""
)

type Rule struct {
	condition Condition
	dest      string
}

type Workflow []Rule

type RuleSet map[string]Workflow

func BuildWorkflowAndItems(lines []string) (RuleSet, []Item) {
	ruleData, itemData := utils.CutSlice(lines, "")
	rules := BuildRuleSet(ruleData)
	items := utils.Map(itemData, BuildItem)
	return rules, items
}

func BuildItem(str string) Item {
	var x, m, a, s int
	tokens := itemRegexp.FindStringSubmatch(str)
	t := utils.Map(tokens[1:], utils.AtoiError)
	x, m, a, s = t[0], t[1], t[2], t[3]
	return Item{x, m, a, s}
}

func strToOp(s string) (op Op) {
	switch s {
	case ">":
		op = gt
	case "<":
		op = lt
	default:
		panic(fmt.Errorf("unexpected value: %s", s))
	}
	return
}

func BuildRule(str string) Rule {
	tokens := ruleRegexp.FindStringSubmatch(str)
	name := tokens[2]
	var cond Condition
	if name == "" {
		if tokens[3] != "" || tokens[4] != "" {
			panic("error parsing condition")
		}

	} else {
		op := strToOp(tokens[3])
		value := utils.AtoiError(tokens[4])
		cond = Condition{name, op, value}
	}
	dest := tokens[5]
	return Rule{condition: cond, dest: dest}
}

func BuildRuleSet(data []string) RuleSet {
	rules := RuleSet{}
	for _, line := range data {
		tokens := workflowRegexp.FindStringSubmatch(line)
		name := tokens[1]
		ruleData := tokens[2]
		ruleStrs := strings.Split(ruleData, ",")
		wf := utils.Map(ruleStrs, BuildRule)
		rules[name] = wf
	}
	return rules
}

func ProcessItems(items []Item, rs RuleSet) []Status {
	return utils.Map(items, func(i Item) Status { return processItem(i, rs) })
}

func (item *Item) getValByName(name string) (val int) {
	switch name {
	case "x":
		val = item.x
	case "m":
		val = item.m
	case "a":
		val = item.a
	case "s":
		val = item.s
	default:
		panic(fmt.Errorf("unexpected value %s", name))
	}
	return
}

func (i *Item) TotalRating() int {
	return i.x + i.m + i.a + i.s
}

func (i *Item) IsAcceptedBy(rs RuleSet) bool {
	return processItem(*i, rs) == ACCEPTED
}

func (c Condition) isMet(item Item) (output bool) {
	if c == NIL_CONDITION {
		return true
	}
	val := item.getValByName(c.name)
	switch c.op {
	case lt:
		output = val < c.value
	case gt:
		output = val > c.value
	default:
		panic("unexpected operation")
	}
	return
}

func toStatus(s string) (status Status, ok bool) {
	switch s {
	case "A":
		return ACCEPTED, true
	case "R":
		return REJETECTED, true
	default:
		return NIL_STATUS, false
	}
}

func processItem(item Item, rs RuleSet) Status {
	target := "in"
	for {
		wf := rs[target]
		for _, rule := range wf {
			if rule.condition.isMet(item) {
				target = rule.dest
				break
			}
		}
		if status, ok := toStatus(target); ok {
			return status
		}
	}
}

func ProcessedRatings(items []Item, rs RuleSet) []int {
	return utils.Map(
		utils.Filter(items, func(i Item) bool { return i.IsAcceptedBy(rs) }),
		func(i Item) int { return i.TotalRating() })
}

func TotalRatings(items []Item, rs RuleSet) int {
	return utils.Sum(ProcessedRatings(items, rs))
}

func main() {
	lines := utils.ReadInput()
	rs, items := BuildWorkflowAndItems(lines)
	part1Answer := TotalRatings(items, rs)
	fmt.Printf("Day 19, Part 1 answer: %d\n", part1Answer)
}
