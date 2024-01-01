package main

import (
	"fmt"
	"math"
	"slices"
	"strings"
	"utils"
)

type SpaceImage [][]string
type Galaxy struct {
	x, y int
}

func (im *SpaceImage) Size() (int, int) {
	return len(*im), len((*im)[0])
}

func NewSpaceImage(lines []string) SpaceImage {
	arr := make([][]string, len(lines))
	for i, line := range lines {
		arr[i] = strings.Split(line, "")
	}
	return SpaceImage(arr)
}

func (im *SpaceImage) colAllDots(x int) bool {
	for y := range *im {
		if (*im)[y][x] != "." {
			return false
		}
	}
	return true
}

func (im *SpaceImage) rowAllDots(y int) bool {
	return allDots(&(*im)[y])
}

func allDots(s *[]string) bool {
	for _, v := range *s {
		if v != "." {
			return false
		}
	}
	return true
}

// If elem is a pointer type all elements will point to the same item
func fullSlice[T ~[]E, E any](n int, elem E) T {
	s := make(T, n)
	for i := range s {
		s[i] = elem
	}
	return s
}

func (im *SpaceImage) InsertColDots(x int) {
	for i := range *im {
		(*im)[i] = slices.Insert((*im)[i], x, ".")
	}
}

func (im *SpaceImage) Expand() {
	_, rowLen := im.Size()
	//insert rows first (easiest)
	for y := 0; y < len(*im); y++ {
		if im.rowAllDots(y) {
			newRow := fullSlice[[]string, string](rowLen, ".")
			*im = slices.Insert((*im), y, newRow)
			y++
		}
	}

	for x := 0; x < len((*im)[0]); x++ {
		if im.colAllDots(x) {
			im.InsertColDots(x)
			x++
		}
	}
}

func (im *SpaceImage) String() string {
	arr := make([]string, len(*im))
	for i, chars := range *im {
		arr[i] = strings.Join(chars, "")
	}
	return strings.Join(arr, "\n")
}

func (im *SpaceImage) FindGalaxies() []Galaxy {
	galaxies := []Galaxy{}
	for y := range *im {
		for x := range (*im)[0] {
			if (*im)[y][x] == "#" {
				galaxies = append(galaxies, Galaxy{x, y})
			}
		}
	}
	return galaxies
}

func (im *SpaceImage) GalaxyDistances() []int {
	galaxies := im.FindGalaxies()
	dists := []int{}
	for i := range galaxies {
		for j := i + 1; j < len(galaxies); j++ {
			dist := FindDistance(galaxies[i], galaxies[j])
			dists = append(dists, dist)
		}
	}
	return dists
}

func FindDistance(g1, g2 Galaxy) int {
	return int(math.Abs(float64(g1.x-g2.x)) + math.Abs(float64(g1.y-g2.y)))
}

func (im *SpaceImage) SumGalaxyDistances() int {
	return utils.Sum(im.GalaxyDistances())
}

func main() {
	lines := utils.ReadInput()
	im := NewSpaceImage(lines)
	im.Expand()
	part1Answer := im.SumGalaxyDistances()
	fmt.Printf("Day 11, Part 1 answer: %d\n", part1Answer)
}
