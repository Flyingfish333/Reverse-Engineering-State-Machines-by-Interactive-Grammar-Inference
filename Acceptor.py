from queue import Queue
import pygraphviz as pgv

class Node:
    def __init__(self, idx = -1) -> None:
        self.idx = idx
        self.next = []
        self.edge = []
        self.parent = None

class Acceptor:
    def __init__(self, apta_idx):
        self.tree_head = Node()
        self.max_idx = 0
        self.output_file_path = None
        self.ktail = {}
        self.apta_idx = apta_idx
        self.color = ['green', 'purple', 'blue', 'red', 'yellow', 'brown', 'pink', 'coral', 'darkorchid']

    def __add_trace(self, trace):
        i = 0
        tree_node = self.tree_head

        while i < len(trace):
            exist = False
            for j, states in enumerate(tree_node.edge):
                if trace[i] == states:
                    tree_node = tree_node.next[j]
                    exist = True
                    break
            
            if not exist:
                new_tree_node = Node(self.max_idx)
                tree_node.next.append(new_tree_node)
                tree_node.edge.append(trace[i])
                new_tree_node.parent = tree_node
                tree_node = new_tree_node
                self.max_idx += 1

            i += 1

    # 对应load
    def build_tree(self, traces):
        self.tree_head = Node()
        for trace in traces:
            self.__add_trace(trace)

    # 对应merge和ok
    # 找到需要合并的对 ['a', 'a'] -> [[Node(1), Node(2)], [Node(3), Node(4)]]
    def find_ktail(self, k=2):
        ktail = {}
        queue_ = Queue()
        queue_.put(self.tree_head)

        node_visited = set()
        node_visited.add(self.tree_head.idx)

        while not queue_.empty():
            size = queue_.qsize()
            for _ in range(size):
                node = queue_.get()
                paths = []
                all_states = []

                for i, next_node in enumerate(node.next):
                    states = [node]
                    path = [node.edge[i]]
                    if k > 1:
                        if next_node == node:
                            continue

                        self.__dfs(next_node, k, paths, path, states, all_states)
                    else:
                        states.append(next_node)
                        paths.append(node.edge[i])
                        all_states.append(states)

                for i, path in enumerate(paths):
                    if path not in ktail.keys():
                        ktail[path] = [all_states[i]]
                    else:
                        ktail[path].append(all_states[i])

                for tmp_node in node.next:
                    # if tmp_node.idx not in node_visited:
                    if tmp_node.idx not in node_visited and tmp_node.idx != node.idx:
                        queue_.put(tmp_node)
                    node_visited.add(tmp_node.idx)
        
        kequal = {}
        for tail, states in ktail.items():
            if len(states) >= 2:
                kequal[tail] = states

        # self.ktail = kequal

        return kequal
    
    def __dfs(self, cur_node, length, paths, path, state, states):
        state = state + [cur_node]

        if len(path) == length:
            paths.append(tuple(path))
            states.append(state)
            return
        else:
            for i, next_node in enumerate(cur_node.next):
                t_path = path + [cur_node.edge[i]]
                self.__dfs(next_node, length, paths, t_path, state, states)

    def __merge_node(self, node1, node2, exclude_state):
        if node1 == node2: # 此时节点值相同但是进来了，说明后继点中有可合对
            merge_idx = []
            for i in range(len(node2.edge)-1, -1, -1):
                if node2.edge[i] == exclude_state:
                    merge_idx.append(i)

            if len(merge_idx) == 2:
                del node2.next[merge_idx[0]]
                del node2.edge[merge_idx[0]]

            return

        candidate_idx = []

        for i in range(len(node2.edge)):
            if node2.edge[i] == exclude_state:
                continue
            
            candidate_idx.append(i)
        
        candidate_edge = [node2.edge[idx] for idx in candidate_idx]
        candidate_next = [node2.next[idx] for idx in candidate_idx]

        for i in range(len(candidate_edge)):
            flag = False
            for j in range(len(node1.next)):
                if candidate_next[i] == node1.next[j] and candidate_edge[i] == node1.edge[j]:
                    flag = True
                    break
            
            if flag == True:
                continue

            node1.edge.append(candidate_edge[i])
            node1.next.append(candidate_next[i])

        # node1.edge += candidate_edge
        # node1.next += candidate_next

        for node in candidate_next:
            node.parent = node1

    def __merge_tail(self, state_tail1, state_tail2, edge_tail):
        reversed_idx = range(len(state_tail2)-1, -1, -1)
        parent = state_tail2[0].parent

        for idx in reversed_idx:
            if idx == len(state_tail2)-1:
                self.__merge_node(state_tail1[idx], state_tail2[idx], None)
            else:
                self.__merge_node(state_tail1[idx], state_tail2[idx], edge_tail[idx])

        if parent != None and state_tail1[0] != state_tail2[0]:
            # 父节点删除掉合并的子节点
            for i, node in enumerate(parent.next):
                if node.idx == state_tail2[0].idx:
                    # 如果state_tail1在
                    if state_tail1[0] in parent.next and state_tail1[0] == state_tail2[0]:
                        del parent.next[i]
                        del parent.edge[i]
                    else:
                        parent.next[i] = state_tail1[0]
                        
    
    def merge(self, merged_state_tail_idx, merging_state_tail_idx, edge_tail):
        state_tail1 = self.ktail[edge_tail][merged_state_tail_idx]
        state_tail2 = self.ktail[edge_tail][merging_state_tail_idx]
        self.__merge_tail(state_tail1, state_tail2, edge_tail)
        # 每次merge后ktail 里面的序列可能需要发生改变
        # 先看看重新跑ktail会不会发现问题

    # 返回k equal的元组对
    # (-1, 6), (0, 1, 'aa')
    def equal_pair(self):
        pair = []
        pair_idx = []

        for tail, states in self.ktail.items():
            for i in range(len(states)):
                for j in range(i+1, len(states)):
                    pair.append((states[i][0].idx, states[j][0].idx))
                    pair_idx.append((i, j, tail))

        return pair, pair_idx

    def draw_tree(self, merged_tail_idx=None, edge_tail=None, output_path=None):
        if output_path == None:
            self.output_file_path = 'output/%d.jpg' % self.apta_idx
        else:
            self.output_file_path = output_path
            
        G = pgv.AGraph(directed=True, strict=False)
        tree_node = self.tree_head
        queue_ = Queue()
        queue_.put(tree_node)

        visited = set()
        node_visited = set()
        node_visited.add(tree_node.idx)
        bold_node = None
        bold_edge = None
        color = None

        if merged_tail_idx != None:
            bold_node = set()
            bold_edge = set()

            state_tail = self.ktail[edge_tail][merged_tail_idx]

            for i, node in enumerate(state_tail):
                bold_node.add(node.idx)
            
            for i in range(len(edge_tail)):
                bold_edge.add((state_tail[i].idx, state_tail[i+1].idx, edge_tail[i]))

            color = self.color.pop()

        while not queue_.empty():
            size = queue_.qsize()
            for _ in range(size):
                node = queue_.get()

                if bold_node != None and node.idx in bold_node:
                    G.add_node(node.idx, color=color)
                else:
                    G.add_node(node.idx)

                node_visited.add(node.idx)

                for i, tmp_node in enumerate(node.edge):
                    if ((node.idx, node.next[i].idx, node.edge[i]) not in visited):
                        if bold_edge != None and ((node.idx, node.next[i].idx, node.edge[i]) in bold_edge):
                            G.add_edge(node.idx, node.next[i].idx, label=node.edge[i], color=color)
                        else:
                            G.add_edge(node.idx, node.next[i].idx, label=node.edge[i])
                        visited.add((node.idx, node.next[i].idx, node.edge[i]))

                    if node.next[i].idx not in node_visited:
                        queue_.put(node.next[i])

        G.layout()
        G.draw(self.output_file_path, prog="dot", format='jpg', args='-Gsize=10 -Gratio=1.4')

    def remove_equal_pair(self, delete_state_idx, tail):
        del self.ktail[tail][delete_state_idx]
        # 这里需要注意删除后如果剩了1个的情况

    def get_fig_path(self):
        return self.output_file_path