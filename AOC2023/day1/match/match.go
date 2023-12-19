package match

import (
	"day1/digits"
	"regexp"
)

type Match struct {
	start int
	len   int
	text  string
}

func NewFromInds(str string, inds []int) Match {
	return Match{
		start: inds[0],
		len:   inds[1] - inds[0],
		text:  str[inds[0]:inds[1]],
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
	return digits.DIGIT_MAPPING[m.text]
}

func (m *Match) LessThan(other Match) bool {
	return m.start < other.start
}
