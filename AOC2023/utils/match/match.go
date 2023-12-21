package match

import (
	"day1/digits"
	"regexp"
)

type Match struct {
	Start int
	End   int
	Text  string
}

func NewFromInds(str string, inds []int) Match {
	return Match{
		Start: inds[0],
		End:   inds[1],
		Text:  str[inds[0]:inds[1]],
	}
}

func NewFromRegexp(str string, re regexp.Regexp) []Match {
	match_inds := re.FindAllStringIndex(str, -1)
	matches := []Match{}
	for _, match := range match_inds {
		matches = append(matches, NewFromInds(str, match))
	}
	return matches
}

func (m *Match) Digit() int {
	return digits.DIGIT_MAPPING[m.Text]
}

func (m *Match) LessThan(other Match) bool {
	return m.Start < other.Start
}

func (m *Match) Len() int {
	return m.End - m.Start
}
