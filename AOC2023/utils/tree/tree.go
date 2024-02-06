package tree

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

func (t *Tree[T]) Traverse(f func(*Node[T])) {
	t.root.traverse(f)
}

func (n *Node[T]) traverse(f func(*Node[T])) {
	f(n)
	for _, node := range n.children {
		node.traverse(f)
	}
}

func (t *Tree[T]) Size() int {
	if t.root == nil {
		return 0
	}
	return t.root.NDescendents()
}

func (n *Node[T]) NDescendents() int {
	s := 1
	for _, c := range n.children {
		s += c.NDescendents()
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
