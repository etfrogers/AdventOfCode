package main

import (
	"fmt"
	"strings"
	"utils"
	"utils/set"
)

type Card struct {
	Id      string
	numbers set.Set[string]
	winners set.Set[string]
}

func NewCard(line string) Card {
	header, data, _ := strings.Cut(line, ":")
	label := header[:5]
	if label != "Card " {
		panic(fmt.Errorf("unexpected label: %s", label))
	}
	id := header[5:]
	number_str, winner_str, _ := strings.Cut(data, "|")
	numbers := dropEmpty(strings.Split(number_str, " "))
	winners := dropEmpty(strings.Split(winner_str, " "))
	return Card{
		Id:      id,
		numbers: set.New[string](numbers...),
		winners: set.New[string](winners...),
	}
}

func dropEmpty(s []string) []string {
	new := []string{}
	for _, val := range s {
		if val != "" {
			new = append(new, val)
		}
	}
	return new
}

func NewCardSlice(lines []string) []Card {
	return utils.Map(lines, NewCard)
}

func (c *Card) WinningNumbers() set.Set[string] {
	return set.Intersection(c.numbers, c.winners)
}

func (c *Card) NWinners() int {
	w := c.WinningNumbers()
	return w.Len()
}

func (c *Card) Score() int {
	n := c.NWinners()
	if n == 0 {
		return 0
	} else {
		val, err := utils.PowInts(2, n-1)
		utils.Check(err)
		return val
	}
}

func TotalScore(cards []Card) int {
	total := 0
	for _, card := range cards {
		total += card.Score()
	}
	return total
}

func ProcessCopies(cards []Card) (int, []int) {
	copies := make([]int, len(cards))
	for i := range copies {
		copies[i] = 1
	}

	for i, card := range cards {
		extra_cards := card.NWinners()
		for j := 1; j <= extra_cards && j < len(cards); j++ {
			copies[j+i] += copies[i]
		}
	}
	return utils.Sum(copies), copies
}
