package main

import (
	"fmt"
	"slices"
	"strings"
	"utils"
	"utils/set"
)

type SpaceImage struct {
	data            [][]string
	expX, expY      set.Set[int]
	expansionFactor int
}
type Galaxy struct {
	x, y int
}

func (im *SpaceImage) Size() (int, int) {
	return len(im.data), len((im.data)[0])
}

func NewSpaceImage(lines []string, expansion int) SpaceImage {
	arr := make([][]string, len(lines))
	for i, line := range lines {
		arr[i] = strings.Split(line, "")
	}
	im := SpaceImage{data: arr, expansionFactor: expansion, expX: *set.New[int](), expY: *set.New[int]()}
	im.Expand()
	return im
}

func (im *SpaceImage) colAllDots(x int) bool {
	for y := range im.data {
		if im.data[y][x] != "." {
			return false
		}
	}
	return true
}

func (im *SpaceImage) rowAllDots(y int) bool {
	return allDots(&im.data[y])
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
	for i := range im.data {
		im.data[i] = slices.Insert(im.data[i], x, ".")
	}
}

func (im *SpaceImage) Expand() {
	//insert rows first (easiest)
	for y := 0; y < len(im.data); y++ {
		if im.rowAllDots(y) {
			im.expY.Add(y)
		}
	}

	for x := 0; x < len(im.data[0]); x++ {
		if im.colAllDots(x) {
			im.expX.Add(x)
		}
	}
}

func (im *SpaceImage) String() string {

	_, rowLen := im.Size()
	// //insert rows first (easiest)
	insertInd := 0
	for y := range im.data {
		if im.expY.Contains(y) {
			newRow := fullSlice[[]string, string](rowLen, ".")
			im.data = slices.Insert(im.data, insertInd, newRow)
			insertInd++
		}
		insertInd++
	}

	insertInd = 0
	for x := range im.data[0] {
		if im.expX.Contains(x) {
			im.InsertColDots(insertInd)
			insertInd++
		}
		insertInd++
	}

	arr := make([]string, len(im.data))
	for i, chars := range im.data {
		arr[i] = strings.Join(chars, "")
	}
	return strings.Join(arr, "\n")
}

func (im *SpaceImage) FindGalaxies() []Galaxy {
	galaxies := []Galaxy{}
	for y := range im.data {
		for x := range im.data[0] {
			if im.data[y][x] == "#" {
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
			dist := im.FindDistance(galaxies[i], galaxies[j])
			dists = append(dists, dist)
		}
	}
	return dists
}

func minmax(x, y int) (int, int) {
	return min(x, y), max(x, y)
}

func (im *SpaceImage) FindDistance(g1, g2 Galaxy) int {
	nExpansions := 0
	minX, maxX := minmax(g1.x, g2.x)
	for x := minX; x <= maxX; x++ {
		if im.expX.Contains(x) {
			nExpansions++
		}
	}
	minY, maxY := minmax(g1.y, g2.y)
	for y := minY; y <= maxY; y++ {
		if im.expY.Contains(y) {
			nExpansions++
		}
	}
	baseDist := maxX - minX + maxY - minY
	return baseDist + nExpansions*(im.expansionFactor-1)
}

func (im *SpaceImage) SumGalaxyDistances() int {
	return utils.Sum(im.GalaxyDistances())
}

func main() {
	lines := utils.ReadInput()
	expansion := 2
	im1 := NewSpaceImage(lines, expansion)
	part1Answer := im1.SumGalaxyDistances()
	fmt.Printf("Day 11, Part 1 answer: %d\n", part1Answer)
	im2 := NewSpaceImage(lines, 1_000_000)
	part2Answer := im2.SumGalaxyDistances()
	fmt.Printf("Day 11, Part 2 answer: %d\n", part2Answer)
}
