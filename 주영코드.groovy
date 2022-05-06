func simplifyNode_iteration_bfs(n node) node {
        list := []Item{}
        curIndex := 0
        list = append(list, Item{
                parentIndex: -1,
                node: n,
                position: -1,
        })

        for {
                if curIndex >= len(list) { break }

                switch node := list[curIndex].node.(type) {
                case *shortNode:
                        // Short nodes discard the flags and cascade
                        newNode := &rawShortNode{Key: node.Key, Val: nil}
                        list[curIndex].node = newNode
                        list = append(list, Item{
                                parentIndex: curIndex,
                                node: node.Val,
                                position: -1,
                        })

                case *fullNode:
                        // Full nodes discard the flags and cascade
                        newNode := rawFullNode(node.Children)
                        list[curIndex].node = newNode
                        for i := 0; i < len(newNode); i++ {
                                if newNode[i] != nil {
                                        list = append(list, Item{
                                                parentIndex: curIndex,
                                                node: newNode[i],
                                                position: i,
                                        })
                                }
                        }

                case valueNode, hashNode, rawNode:
                        if curIndex == 0 { return node }
                        if node, ok := list[list[curIndex].parentIndex].node.(*rawShortNode); ok {
                                node.Val = list[curIndex].node
                                list[list[curIndex].parentIndex].node = node
                        } else if node, ok := list[list[curIndex].parentIndex].node.(rawFullNode); ok {
                                node[list[curIndex].position] = list[curIndex].node
                                list[list[curIndex].parentIndex].node = node
                        }

                default:
                        panic(fmt.Sprintf("unknown node type: %T", n))
                }

                curIndex += 1
        }

        return list[0].node
}