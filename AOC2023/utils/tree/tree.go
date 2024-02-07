package tree

import (
	"fmt"
	"slices"
	"strings"
	"utils"
	"utils/iter"
)

type Node[T any] struct {
	parent   *Node[T]
	children []*Node[T]
	value    T
}

type Tree[T any] struct {
	root *Node[T]
}

func NewNode[T any](value T) *Node[T] {
	return &Node[T]{children: make([]*Node[T], 0), value: value}
}

func New[T any](node *Node[T]) *Tree[T] {
	return &Tree[T]{root: node}
}

func (n *Node[T]) AddChild(nodes ...*Node[T]) {
	for _, node := range nodes {
		node.parent = n
		n.children = append(n.children, node)
	}
}

func (n *Node[T]) String() string {
	var parentVal any
	if n.parent == nil {
		parentVal = "nil"
	} else {
		parentVal = n.parent.value
	}
	childStrs := utils.Map(n.children, func(c *Node[T]) string { return fmt.Sprint(c.value) })
	childStr := strings.Join(childStrs, ", ")
	return fmt.Sprintf("Val: %v - Parent: %v, Children: %s", n.value, parentVal, childStr)
}

func (t *Tree[T]) Traverse(f func(*Node[T])) {
	if t.root == nil {
		return
	}
	t.root.traverse(f)
}

func (n *Node[T]) traverse(f func(*Node[T])) bool {
	f(n)
	for _, node := range n.children {
		if !node.traverse(f) {
			return false
		}
	}
	return true
}

func (t *Tree[T]) Size() int {
	if t.root == nil {
		return 0
	}
	return t.root.NDescendents() + 1
}

func (n *Node[T]) NDescendents() int {
	s := 0
	for _, c := range n.children {
		s += c.NDescendents() + 1
	}
	return s
}

func (t *Tree[T]) GetLeaves() []*Node[T] {
	leaves := make([]*Node[T], 0)
	t.Traverse(func(n *Node[T]) {
		if n.IsLeaf() {
			leaves = append(leaves, n)
		}
	})
	return leaves
}

func (n *Node[T]) IsLeaf() bool {
	return len(n.children) == 0
}

func (t *Tree[T]) NodeToRootValues(from *Node[T]) []T {
	values := make([]T, 0)
	t.WalkToRoot(from, func(n *Node[T]) {
		values = append(values, n.value)
	})
	return values
}

func (t *Tree[T]) WalkToRoot(from *Node[T], fun func(*Node[T])) {
	for n := from; n != nil; n = n.parent {
		fun(n)
	}
}

func (t *Tree[T]) String() string {
	strs := make([]string, 0)
	t.Traverse(func(n *Node[T]) { strs = append(strs, n.String()) })
	return strings.Join(strs, "\n")
}

func (t *Tree[T]) Render() {
	fmt.Println(t)
	fmt.Println("")
}

func (t *Tree[T]) PruneBranchTo(node *Node[T]) {
	for node != nil && node.IsLeaf() {
		p := node.parent
		t.Remove(node)
		node = p
	}
}

func (t *Tree[T]) Remove(node *Node[T]) {
	if node.parent == nil {
		t.root = nil
		return
	}
	i := slices.Index(node.parent.children, node)
	node.parent.children[i] = nil
	node.parent.children = slices.Delete(node.parent.children, i, i+1)
	node.parent = nil
}

func (t *Tree[T]) AllNodes() iter.Iter[*Node[T]] {
	return iter.NewGen[*Node[T]](func(yield func(*Node[T]) bool) {
		t.Traverse(func(n *Node[T]) { yield(n) })
	})
}
