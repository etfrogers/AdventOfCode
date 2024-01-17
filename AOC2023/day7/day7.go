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

const CARD_RANKS = "23456789TJQKA"      // "AKQJT98765432"
const CARD_RANKS_WILD = "J23456789TQKA" // "AKQJT98765432"
const WILDCARD = "J"

func (h *Hand) Counter() *counter.Counter[string] {
	if h.counter.Len() == 0 {
		h.counter = counter.FromString(h.cards)
	}
	return &h.counter
}

func (h *Hand) Type(useWildcards bool) HandType {
	counter := h.Counter()
	wcCounts := 0
	if useWildcards {
		wcCounts = counter.Get(WILDCARD)
		counter.Delete(WILDCARD)
	}
	keys, counts := counter.KeysInOrder()
	if s := utils.Sum(counts) + wcCounts; s != 5 {
		panic(fmt.Errorf("sum of counts must be 5. Acutal value %d", s))
	}

	var type_ HandType
	switch {
	case wcCounts == 5 || counts[0]+wcCounts == 5:
		if !useWildcards && (counter.Get(keys[0]) != 5 || counts[0] != 5) {
			panic("unexepcted value")
		}
		type_ = FiveOfAKind
	case counts[0]+wcCounts == 4:
		if !useWildcards && (counter.Len() != 2 || counts[1] != 1) {
			panic("unexepcted value")
		}
		type_ = FourOfAKind
	case counts[0]+wcCounts == 3 && counts[1] == 2:
		return FullHouse
	case counts[0]+wcCounts == 3:
		if !useWildcards && (counter.Len() != 3 && counts[1] == 1 && counts[2] == 1) {
			panic("unexepcted value")
		}
		return ThreeOfAKind
	// Two pair cannot happen beacuase of a wildcard: it would be at least Three of a kind
	case counts[0] == 2 && counts[1] == 2:
		return TwoPair
	// if at least 1 wildcard, then you alway get at least one pair
	case (counts[0] == 2 && counts[1] == 1) || wcCounts > 0:
		if !useWildcards && counter.Len() != 4 {
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

func (h *Hand) CardRank(pos int, useWildcards bool) int {
	var rankings string
	if useWildcards {
		rankings = CARD_RANKS_WILD
	} else {
		rankings = CARD_RANKS
	}
	return strings.Index(rankings, string(h.cards[pos]))
}

func Less(h1, h2 Hand, useWildcards bool) bool {
	t1 := h1.Type(useWildcards)
	t2 := h2.Type(useWildcards)
	switch {
	case t1 < t2:
		return true
	case t1 > t2:
		return false
	case t1 == t2:
		for i := 0; i < len(h1.cards); i++ {
			r1 := h1.CardRank(i, useWildcards)
			r2 := h2.CardRank(i, useWildcards)
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

func (hl *HandList) Sort(useWildcards bool) {
	sort.Slice(*hl, func(i, j int) bool { return Less((*hl)[i], (*hl)[j], useWildcards) })
}

func (hl *HandList) Winnings(useWildcards bool) []int {
	hands := make(HandList, len(*hl))
	copy(hands, *hl)
	hands.Sort(useWildcards)
	winnings := make([]int, len(hands))
	for i, hand := range hands {
		rank := i + 1
		winnings[i] = rank * hand.bid
	}
	return winnings
}

func (hl *HandList) TotalWinnings(useWildcards bool) int {
	return utils.Sum(hl.Winnings(useWildcards))
}

func main() {
	lines := utils.ReadInput()
	hands := MakeHands(lines)
	part1Answer := hands.TotalWinnings(false)
	fmt.Printf("Day 7, Part 1 answer: %d\n", part1Answer)
	part2Answer := hands.TotalWinnings(true)
	fmt.Printf("Day 7, Part 2 answer: %d\n", part2Answer)
}
