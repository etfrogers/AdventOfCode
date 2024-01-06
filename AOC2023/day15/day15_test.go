package main

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

var testCase string = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

var expectedHashes []int = []int{30, 253, 97, 47, 14, 180, 9, 197, 48, 214, 231}

var testLines []string = strings.Split(testCase, "\n")

func TestHash(t *testing.T) {
	assert.Equal(t, Hash("HASH"), 52)
}

func TestCaseHashes(t *testing.T) {
	hashes := HashSlice(testCase)
	assert.Equal(t, expectedHashes, hashes)
}

func TestChecksum(t *testing.T) {
	expected := 1320
	assert.Equal(t, expected, Checksum(testCase))
}
