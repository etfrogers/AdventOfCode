package main

import (
	"fmt"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

var testCase string = `32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483`

var testLines []string = strings.Split(testCase, "\n")

func TestPart1(t *testing.T) {
	t.Skip("not implemented")
	assert.Fail(t, "not implemented")
}

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
			assert.Equal(t, tc.type_, hand.Type())
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
			assert.True(t, Less(Hand{cards: tc.lower}, Hand{cards: tc.higher}))
		})
	}
}

func TestRanks(t *testing.T) {
	expectedOrder := []string{"32T3K", "KTJJT", "KK677", "T55J5", "QQQJA"}
	hands := MakeHands(testLines)
	hands.Sort()
	for i, hand := range hands {
		assert.Equal(t, expectedOrder[i], hand.cards)
	}
}

func TestWinnings(t *testing.T) {
	hands := MakeHands(testLines)
	expected := []int{765 * 1, 220 * 2, 28 * 3, 684 * 4, 483 * 5}
	assert.Equal(t, expected, hands.Winnings())
}

func TestTotalWinnings(t *testing.T) {
	hands := MakeHands(testLines)
	expected := 6440
	assert.Equal(t, expected, hands.TotalWinnings())
}
