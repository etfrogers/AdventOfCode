package counter

import (
	"iter"
	"sort"
	"strings"
)

type Counter[T comparable] struct {
	counts map[T]int
}

type counterPair[T comparable] struct {
	item  T
	count int
}

func FromString(str string) Counter[string] {
	return New(strings.Split(str, "")...)
}

func FromIter[T comparable](it iter.Seq[T]) Counter[T] {
	counter := New[T]()
	for v := range it {
		counter.Add(v)
	}
	return counter
}

func New[T comparable](x ...T) Counter[T] {
	counter := Counter[T]{counts: map[T]int{}}
	counter.Add(x...)
	return counter
}

func (c Counter[T]) Add(vals ...T) {
	for _, val := range vals {
		c.counts[val] += 1
	}
}

func (c Counter[T]) Get(item T) (count int) {
	return c.counts[item]
}

func (c Counter[T]) Len() int {
	return len(c.counts)
}

func (c Counter[T]) pairsInOrder() []counterPair[T] {
	pairs := make([]counterPair[T], len(c.counts))
	i := 0
	for item, count := range c.counts {
		pairs[i] = counterPair[T]{item, count}
		i++
	}
	// Note less is inverted here to achieve a reverse sort (high -> low)
	sort.SliceStable(pairs, func(i, j int) bool { return pairs[i].count > pairs[j].count })
	return pairs
}

func (c Counter[T]) KeysInOrder() (keys []T, counts []int) {
	pairs := c.pairsInOrder()
	keys = make([]T, len(pairs))
	counts = make([]int, len(pairs))
	for i, pair := range pairs {
		keys[i] = pair.item
		counts[i] = pair.count
	}
	return
}

func (c *Counter[T]) Delete(key T) {
	delete(c.counts, key)
}
