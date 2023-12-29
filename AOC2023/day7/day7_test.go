package main

import (
	"fmt"
	"strings"
	"testing"
	"utils"

	"github.com/stretchr/testify/assert"
)

var testCase string = `32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483`

var testLines []string = strings.Split(testCase, "\n")

func TestTypeExamples(t *testing.T) {
	testCases := []struct {
		cards string
		type_ HandType
	}{
		{"AAAAA", FiveOfAKind},
		{"AA8AA", FourOfAKind},
		{"23332", FullHouse},
		{"TTT98", ThreeOfAKind},
		{"23432", TwoPair},
		{"A23A4", OnePair},
		{"23456", HighCard},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			hand := Hand{cards: tc.cards}
			assert.Equal(t, tc.type_, hand.Type(false))
		})
	}
}

func TestTypeExamplesWildcards(t *testing.T) {
	testCases := []struct {
		cards string
		type_ HandType
	}{
		{"32T3K", OnePair},
		{"32TQJ", OnePair},
		{"32TJJ", ThreeOfAKind},
		{"32TTJ", ThreeOfAKind},
		{"T55J5", FourOfAKind},
		{"KK677", TwoPair},
		{"KK6J7", ThreeOfAKind},
		{"KK7J7", FullHouse},
		{"KTJJT", FourOfAKind},
		{"QQQJA", FourOfAKind},
		{"QQQJQ", FiveOfAKind},
		{"QQQQQ", FiveOfAKind},
		{"JJJJJ", FiveOfAKind},
		{"KQJJJ", FourOfAKind},
		{"234JJ", ThreeOfAKind},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			hand := Hand{cards: tc.cards}
			assert.Equal(t, tc.type_, hand.Type(true))
		})
	}
}

func TestRankExamples(t *testing.T) {
	testCases := []struct {
		lower  string
		higher string
	}{
		{"2AAAA", "33332"},
		{"77788", "77888"},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			assert.True(t, Less(Hand{cards: tc.lower}, Hand{cards: tc.higher}, false))
		})
	}
}

func TestRankExamplesWildcards(t *testing.T) {
	testCases := []struct {
		lower  string
		higher string
	}{
		{"2AAAA", "33332"},
		{"77788", "77888"},
		{"77J88", "77888"},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			assert.True(t, Less(Hand{cards: tc.lower}, Hand{cards: tc.higher}, true))
		})
	}
}

func TestRanks(t *testing.T) {
	expectedOrder := []string{"32T3K", "KTJJT", "KK677", "T55J5", "QQQJA"}
	hands := MakeHands(testLines)
	hands.Sort(false)
	for i, hand := range hands {
		assert.Equal(t, expectedOrder[i], hand.cards)
	}
}

func TestRanksWildcard(t *testing.T) {
	expectedOrder := []string{"32T3K", "KK677", "T55J5", "QQQJA", "KTJJT"}
	hands := MakeHands(testLines)
	hands.Sort(true)
	for i, hand := range hands {
		assert.Equal(t, expectedOrder[i], hand.cards)
	}
}

func TestWinnings(t *testing.T) {
	hands := MakeHands(testLines)
	expected := []int{765 * 1, 220 * 2, 28 * 3, 684 * 4, 483 * 5}
	assert.Equal(t, expected, hands.Winnings(false))
}

func TestTotalWinnings(t *testing.T) {
	testCases := []struct {
		useWildCards     bool
		expectedWinnings int
	}{
		{false, 6440},
		{true, 5905},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			hands := MakeHands(testLines)
			assert.Equal(t, tc.expectedWinnings, hands.TotalWinnings(tc.useWildCards))
		})
	}
}

func TestPart1(t *testing.T) {
	lines := utils.ReadInput()
	hands := MakeHands(lines)
	part1Answer := hands.TotalWinnings(false)
	assert.Equal(t, 248396258, part1Answer)
}

func TestPart2(t *testing.T) {
	lines := utils.ReadInput()
	hands := MakeHands(lines)
	part2Answer := hands.TotalWinnings(true)
	assert.Equal(t, 246436046, part2Answer)
}
