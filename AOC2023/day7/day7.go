package main

import (
	"fmt"
	"sort"
	"strings"
	"utils"
	"utils/counter"
)

type Hand struct {
	cards   string
	bid     int
	counter counter.Counter[string]
}

type HandType int

const (
	HighCard     HandType = iota
	OnePair      HandType = iota
	TwoPair      HandType = iota
	ThreeOfAKind HandType = iota
	FullHouse    HandType = iota
	FourOfAKind  HandType = iota
	FiveOfAKind  HandType = iota
)

type HandList []Hand

const CARD_RANKS = "23456789TJQKA" // "AKQJT98765432"

func (h *Hand) Counter() *counter.Counter[string] {
	if h.counter.Len() == 0 {
		h.counter = counter.NewFromString(h.cards)
	}
	return &h.counter
}

func (h *Hand) Type() HandType {
	counter := h.Counter()
	keys, counts := counter.KeysInOrder()
	if s := utils.Sum(counts); s != 5 {
		panic(fmt.Errorf("sum of counts must be 5. Acutal value %d", s))
	}
	var type_ HandType
	switch {
	case counter.Len() == 1:
		if counter.Get(keys[0]) != 5 || counts[0] != 5 {
			panic("unexepcted value")
		}
		type_ = FiveOfAKind
	case counts[0] == 4:
		if counter.Len() != 2 || counts[1] != 1 {
			panic("unexepcted value")
		}
		type_ = FourOfAKind
	case counts[0] == 3 && counts[1] == 2:
		return FullHouse
	case counts[0] == 3 && counts[1] == 1:
		if counter.Len() != 3 && counts[1] == 1 && counts[2] == 1 {
			panic("unexepcted value")
		}
		return ThreeOfAKind
	case counts[0] == 2 && counts[1] == 2:
		return TwoPair
	case counts[0] == 2 && counts[1] == 1:
		if counter.Len() != 4 {
			panic("unexepcted value")
		}
		return OnePair
	case counts[0] == 1:
		if counter.Len() != 5 {
			panic("unexepcted value")
		}
	default:
		panic(fmt.Errorf("unhandled type for cards %s", h.cards))
	}
	return type_
}

func NewHand(line string) Hand {
	cards, bidStr, _ := strings.Cut(line, " ")
	return Hand{cards: cards, bid: utils.AtoiError(bidStr)}
}

func MakeHands(lines []string) HandList {
	return utils.Map(lines, NewHand)
}

func (h *Hand) CardRank(pos int) int {
	return strings.Index(CARD_RANKS, string(h.cards[pos]))
}

func Less(h1, h2 Hand) bool {
	switch {
	case h1.Type() < h2.Type():
		return true
	case h1.Type() > h2.Type():
		return false
	case h1.Type() == h2.Type():
		for i := 0; i < len(h1.cards); i++ {
			r1 := h1.CardRank(i)
			r2 := h2.CardRank(i)
			switch {
			case r1 < r2:
				return true
			case r1 > r2:
				return false
			}
		}
		panic("hands are equal")
	}
	return true
}

func (hl *HandList) Sort() {
	sort.Slice(*hl, func(i, j int) bool { return Less((*hl)[i], (*hl)[j]) })
}

func (hl *HandList) Winnings() []int {
	hands := make(HandList, len(*hl))
	copy(hands, *hl)
	hands.Sort()
	winnings := make([]int, len(hands))
	for i, hand := range hands {
		rank := i + 1
		winnings[i] = rank * hand.bid
	}
	return winnings
}

func (hl *HandList) TotalWinnings() int {
	return utils.Sum(hl.Winnings())
}

func main() {
	lines := utils.ReadInput()
	hands := MakeHands(lines)
	part1Answer := hands.TotalWinnings()
	fmt.Printf("Day 7, Part 1 answer: %d\n", part1Answer)
}
