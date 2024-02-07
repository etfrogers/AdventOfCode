package tree_test

import (
	"testing"
	"utils/iter"
	"utils/tree"

	"github.com/stretchr/testify/assert"
)

func TestBasic(t *testing.T) {
	rootNode := tree.NewNode(0)
	tr := tree.New[int](rootNode)

	assert.Equal(t, 1, tr.Size())
	assert.Equal(t, 0, rootNode.NDescendents())
	assert.Equal(t, []*tree.Node[int]{rootNode}, tr.GetLeaves())

	child1 := tree.NewNode(1)
	rootNode.AddChild(child1)
	assert.Equal(t, 2, tr.Size())
	assert.Equal(t, 1, rootNode.NDescendents())
	assert.Equal(t, 0, child1.NDescendents())
	assert.Equal(t, []*tree.Node[int]{child1}, tr.GetLeaves())

	assert.Equal(t, iter.ToSlice(tr.AllNodes()), []*tree.Node[int]{rootNode, child1})

	child2 := tree.NewNode(2)
	rootNode.AddChild(child2)
	assert.Equal(t, 3, tr.Size())
	assert.Equal(t, 2, rootNode.NDescendents())
	assert.Equal(t, 0, child1.NDescendents())
	assert.Equal(t, 0, child2.NDescendents())
	assert.Equal(t, []*tree.Node[int]{child1, child2}, tr.GetLeaves())

	assert.Equal(t, iter.ToSlice(tr.AllNodes()), []*tree.Node[int]{rootNode, child1, child2})

	branch := make([]*tree.Node[int], 0)
	n := child1
	for i := 3; i <= 6; i++ {
		new := tree.NewNode(i)
		branch = append(branch, new)
		n.AddChild(new)
		n = new
	}

	assert.Equal(t, 7, tr.Size())
	assert.Equal(t, 6, rootNode.NDescendents())
	assert.Equal(t, 4, child1.NDescendents())
	assert.Equal(t, 0, child2.NDescendents())
	assert.Equal(t, []*tree.Node[int]{n, child2}, tr.GetLeaves())

	expected := []*tree.Node[int]{rootNode, child1}
	expected = append(expected, branch...)
	expected = append(expected, child2)
	assert.Equal(t, expected, iter.ToSlice(tr.AllNodes()))
	assert.Equal(t, []int{6, 5, 4, 3, 1, 0}, tr.NodeToRootValues(n))

	tr.PruneBranchTo(branch[len(branch)-1])
	assert.Equal(t, 2, tr.Size())
	assert.Equal(t, 1, rootNode.NDescendents())
	// assert.Equal(t, 4, child1.NDescendents())
	assert.Equal(t, 0, child2.NDescendents())
	assert.Equal(t, []*tree.Node[int]{child2}, tr.GetLeaves())
	assert.Equal(t, []*tree.Node[int]{rootNode, child2}, iter.ToSlice(tr.AllNodes()))

	expectedStr := "Val: 0 - Parent: nil, Children: 2\nVal: 2 - Parent: 0, Children: "
	assert.Equal(t, expectedStr, tr.String())
	// Just check it runs
	tr.Render()

	tr.Remove(rootNode)
	assert.Equal(t, 0, tr.Size())
}

func TestZeroSize(t *testing.T) {
	tr := tree.New[int](nil)
	assert.Equal(t, 0, tr.Size())
	assert.Equal(t, "", tr.String())
}
