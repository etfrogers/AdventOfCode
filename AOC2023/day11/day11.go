package main

import (
	"fmt"
	"slices"
	"strings"
	"utils"
	"utils/grid"
	"utils/set"
)

type SpaceImage struct {
	*grid.Grid[string]
	expX, expY      set.Set[int]
	expansionFactor int
}
type Galaxy struct {
	x, y int
}

func NewSpaceImage(lines []string, expansion int) SpaceImage {
	arr := make([][]string, len(lines))
	for i, line := range lines {
		arr[i] = strings.Split(line, "")
	}
	g := grid.New(arr)
	im := SpaceImage{Grid: &g, expansionFactor: expansion, expX: *set.New[int](), expY: *set.New[int]()}
	im.Expand()
	return im
}

func (im *SpaceImage) colAllDots(x int) bool {
	for y := range *im.Grid {
		if im.Get(x, y) != "." {
			return false
		}
	}
	return true
}

func (im *SpaceImage) rowAllDots(y int) bool {
	return allDots(im.GetRow(y))
}

func allDots(s *[]string) bool {
	for _, v := range *s {
		if v != "." {
			return false
		}
	}
	return true
}

func (im *SpaceImage) InsertColDots(x int) {
	for i := range *im.Grid {
		(*im.Grid)[i] = slices.Insert((*im.Grid)[i], x, ".")
	}
}

func (im *SpaceImage) Expand() {
	//insert rows first (easiest)

	for y := 0; y < im.NRows(); y++ {
		if im.rowAllDots(y) {
			im.expY.Add(y)
		}
	}

	for x := 0; x < im.NCols(); x++ {
		if im.colAllDots(x) {
			im.expX.Add(x)
		}
	}
}

func (im *SpaceImage) String() string {

	_, rowLen := im.Size()
	// //insert rows first (easiest)
	insertInd := 0
	for y := range *im.Grid {
		if im.expY.Contains(y) {
			newRow := utils.FullSlice[[]string, string](rowLen, ".")
			im.InsertRow(insertInd, newRow)
			insertInd++
		}
		insertInd++
	}

	insertInd = 0
	for x := range (*im.Grid)[0] {
		if im.expX.Contains(x) {
			im.InsertColDots(insertInd)
			insertInd++
		}
		insertInd++
	}

	arr := make([]string, len(*im.Grid))
	for i, chars := range *im.Grid {
		arr[i] = strings.Join(chars, "")
	}
	return strings.Join(arr, "\n")
}

func (im *SpaceImage) FindGalaxies() []Galaxy {
	galaxies := []Galaxy{}
	for y := range *im.Grid {
		for x := range (*im.Grid)[0] {
			if im.Get(x, y) == "#" {
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
