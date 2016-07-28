#coding=utf-8
import Levenshtein
import igraph


class Cluster:

    def __init__(self, news_dict):

        """
        :param news_dict:{新闻猎户:[新闻1,新闻2,..,新闻n],新闻猎户2}
        """

        self.news_list = Cluster.get_news_list(news_dict)
        self.news_similar_matrix = self.calculate_simiarity(self.news_list)

    @staticmethod
    def get_news_list(news_dict):
        news_list = []   #汇总所有的新闻,形成[新闻1, 新闻2, 新闻3, ..., 新闻n ]
        for news in news_dict:
            news_list.extend(news_dict[news])
        return news_list

    def calculate_simiarity(self, news_list):
        """
        构建新闻相似度矩阵
        :param news_list:新闻列表
        :return:新闻相似度矩阵
        """
        news_similar_matrix = [[0 for col in range(news_list.__len__())] for row in range(news_list.__len__())] #创建新闻相似度矩阵
        for i in range(0, news_list.__len__(), 1):
            new_i = news_list[i]
            for j in range(0, news_list.__len__(),1):
                new_j = news_list[j]
                similarity = Levenshtein.ratio(new_i,new_j)
                if similarity > 0.4:
                    news_similar_matrix[i][j] = news_similar_matrix[j][i] = similarity*10
                else:
                    news_similar_matrix[i][j] = news_similar_matrix[j][i] = 0
        return news_similar_matrix


    def cluster_news(self):
        """
        function:新闻的聚合
        :return: 聚合后的新闻情况
        """
        nodes = self.news_similar_matrix.__len__()
        g = igraph.Graph(nodes)
        weights = []
        edges = []
        for i in range(0, nodes, 1):
            for j in range(0, nodes, 1):
                if self.news_similar_matrix[i][j] > 0:
                    edges += [(i, j)]
                    weights.append(self.news_similar_matrix[i][j])
        g.add_edges(edges)
        g = g.simplify()
        clusters = g.community_multilevel(weights)
        news_clusters =[]
        for one_cluster in clusters:
            news_one_cluster = []
            # print one_cluster
            for i in one_cluster:
                news_one_cluster.append(self.news_list[i])
            news_clusters.append(news_one_cluster)
        return news_clusters


if __name__ == '__main__':
    news_dict = {'网易新闻':['1234','2345'],'环球时报':['666','12']}
    cluster = Cluster(news_dict)
    print cluster.cluster_news()

