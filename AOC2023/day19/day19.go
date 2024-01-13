package main

import (
	"fmt"
	"maps"
	"regexp"
	"slices"
	"strings"
	"utils"
	"utils/stack"
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

type ConditionKey struct {
	name string
	op   Op
}

var NIL_CONDITION Condition = Condition{}

type Status string

const (
	ACCEPTED   Status = "A"
	REJECTED   Status = "R"
	NIL_STATUS Status = ""
)

var FIELDS []string = []string{"x", "m", "a", "s"}

type Rule struct {
	condition Condition
	dest      string
}

type RuleHistory struct {
	*Rule
	passed bool
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

func (r *Rule) Inverted() Rule {
	return Rule{r.condition.Inverted(), r.dest}
}

func (c *Condition) Inverted() Condition {
	var val int
	var op Op
	switch c.op {
	case gt:
		op = lt
		val = c.value + 1
	case lt:
		op = gt
		val = c.value - 1
	}
	return Condition{c.name, op, val}
}

func (c *Condition) GetKey() ConditionKey {
	return ConditionKey{c.name, c.op}
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
		return REJECTED, true
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

type limitMap map[ConditionKey]int

type Path struct {
	history          []RuleHistory
	limits           limitMap
	currentWf        string
	cuurentRuleIndex int
}

func NewPath(wf string) Path {
	limits := limitMap{}
	for _, name := range FIELDS {
		limits[ConditionKey{name, gt}] = 0
		limits[ConditionKey{name, lt}] = 4001
	}
	p := Path{
		currentWf:        wf,
		cuurentRuleIndex: 0,
		limits:           limits,
		history:          make([]RuleHistory, 0, 100),
	}
	return p
}

func (p *Path) Copy() Path {
	return Path{
		currentWf:        p.currentWf,
		cuurentRuleIndex: p.cuurentRuleIndex,
		limits:           maps.Clone(p.limits),
		history:          slices.Clone(p.history),
	}
}

func (r *Rule) CreateHistory(passed bool) RuleHistory {
	h := RuleHistory{Rule: r, passed: passed}
	return h
}

func (p *Path) AddRule(rule Rule, passedRule bool) (dest string) {
	p.history = append(p.history, rule.CreateHistory(passedRule))
	condition := rule.condition
	if condition != NIL_CONDITION {
		key := condition.GetKey()
		switch condition.op {
		case gt:
			p.limits[key] = max(p.limits[key], condition.value)
		case lt:
			p.limits[key] = min(p.limits[key], condition.value)
		default:
			panic(fmt.Errorf("unexpected value: %v", condition.op))
		}
	}
	if passedRule {
		p.currentWf = rule.dest
		p.cuurentRuleIndex = 0
	} else {
		p.cuurentRuleIndex++
	}
	return p.currentWf
}

func (p *Path) isValid() bool {
	for _, name := range FIELDS {
		if p.nPassingField(name) < 1 {
			return false
		}
	}
	return true
}

func (p *Path) nPassingField(name string) int {
	upper := p.limits[ConditionKey{name, lt}]
	lower := p.limits[ConditionKey{name, gt}]
	// subtract 2 because gt 0 + less than 4001 is 4000 valid numbers
	diff := upper - lower - 1
	if diff < 1 {
		return 0
	}
	return diff
}

func (p *Path) ValidCombinations() int {
	combs := 1
	for _, name := range FIELDS {
		combs *= p.nPassingField(name)
	}
	return combs
}

func FindPaths(rs RuleSet) (accepted, rejected, aborted []Path) {
	accepted = []Path{}
	rejected = []Path{}
	aborted = []Path{}
	paths := stack.New[Path]()

	processRule := func(path Path, rule Rule, passedRule bool) {
		dest := path.AddRule(rule, passedRule)
		if !path.isValid() {
			aborted = append(aborted, path)
			return
		}
		switch Status(dest) {
		case ACCEPTED:
			accepted = append(accepted, path)
		case REJECTED:
			rejected = append(rejected, path)
		default:
			paths.Push(path)
		}
	}

	paths.Push(NewPath("in"))
	for paths.Len() > 0 {
		path, _ := paths.Pop()
		rule := rs[path.currentWf][path.cuurentRuleIndex]
		if rule.condition != NIL_CONDITION {
			// ensure copying happens before the other rule is applied
			// more effficient to only copy someitmes, rather than always
			processRule(path.Copy(), rule.Inverted(), false)
		}
		processRule(path, rule, true)
	}
	return
}

func FindCombinations(paths []Path) int {
	return utils.Sum(utils.Map(paths, func(p Path) int { return p.ValidCombinations() }))
}

func TotalCombinationsAccepted(rs RuleSet) int {
	accepted, _, _ := FindPaths(rs)
	return FindCombinations(accepted)
}

func main() {
	lines := utils.ReadInput()
	rs, items := BuildWorkflowAndItems(lines)
	part1Answer := TotalRatings(items, rs)
	fmt.Printf("Day 19, Part 1 answer: %d\n", part1Answer)
	part2Answer := TotalCombinationsAccepted(rs)
	fmt.Printf("Day 19, Part 2 answer: %d\n", part2Answer)
}
