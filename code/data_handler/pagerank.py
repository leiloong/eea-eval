import numpy as np


class PRIterator:
    def __init__(self, graph_matrix):
        self.damping_factor = 0.85  # 阻尼系数,即α
        self.max_iterations = 100  # 最大迭代次数
        self.min_delta = 0.00001  # 确定迭代是否结束的参数,即ϵ
        self.graph_matrix = graph_matrix

    def page_rank(self):

        #  先将图中没有出链的节点改为对所有节点都有出链
        size = self.graph_matrix.shape[0]
        # print(self.graph_matrix)
        col_sum = np.sum(self.graph_matrix, axis=1)
        for j in range(size):
            if col_sum[j] == 0:
                for i in range(size):
                    self.graph_matrix[i][j] = 1.0/size

        # 统计相邻结点的个数
        neighbors = [0 for i in range(size)]
        for j in range(size):
            cnt = 0
            for i in range(size):
                if self.graph_matrix[i][j] != 0:
                    cnt += 1
            neighbors[j] = cnt

        # 给每个节点赋予初始的PR值
        page_rank = [1.0/size for i in range(size)]
        # 公式中的(1−α)/N部分
        damping_value = (1.0 - self.damping_factor) / size

        flag = False
        for iter_cnt in range(self.max_iterations):
            change = 0
            for i in range(size):
                rank = 0
                for j in range(size):  # 遍历所有“入射”的页面
                    if self.graph_matrix[i][j] != 0:
                        rank += self.damping_factor * (page_rank[j] / neighbors[j])
                rank += damping_value
                change += abs(page_rank[i] - rank)  # 绝对值
                page_rank[i] = rank

            # print("This is NO.%s iteration" % (iter_cnt + 1))
            # print(page_rank)

            if change < self.min_delta:
                flag = True
                break
        if flag:
            print("finished in %s iterations!" % (iter_cnt+1))
        else:
            print("finished out of 100 iterations!")
        print(page_rank)
        return page_rank


if __name__ == '__main__':
    # dg = digraph()

    # dg.add_nodes(["A", "B", "C", "D", "E"])
    #
    # dg.add_edge(("A", "B"))
    # dg.add_edge(("A", "C"))
    # dg.add_edge(("A", "D"))
    # dg.add_edge(("B", "D"))
    # dg.add_edge(("C", "E"))
    # dg.add_edge(("D", "E"))
    # dg.add_edge(("B", "E"))
    # dg.add_edge(("E", "A"))
    #
    # pr = PRIterator(dg)
    # page_ranks = pr.page_rank()
    #
    # print("The final page rank is\n", page_ranks)
    # m = np.array([[0, 0.5, 0, 0], [1.0/3, 0, 0, 0.5], [1.0/3, 0, 1, 0.5], [1.0/3, 0.5, 0, 0]])
    m = np.array([[0, 0, 0, 0, 1],
                  [1.0/3, 0, 0, 0, 0],
                  [1.0/3, 0, 0, 0, 0],
                  [1.0/3, 0.5, 0, 0, 0],
                  [0, 0.5, 1, 1, 0]])
    pr = PRIterator(m)
    page_ranks = pr.page_rank()
    print(sum(m[1]))
