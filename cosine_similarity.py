import re
import pandas as pd
import numpy as np

import string
import xlwt
import csv
import codecs
import math
from collections import Counter
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class CosineSimilarity:
    """
    Class for calculating cosine similarity
    """
    def __init__(self, inpath_last_comment, inpath_final_msg):

        self._last_comments = pd.read_excel(inpath_last_comment, sheet_name="last_comment", usecols=[0, 2, 3, 4, 5], header=None)
        self._final_msg = pd.read_excel(inpath_final_msg, sheet_name="final_msg", usecols=[0, 1, 2, 3, 4, 5], header=None)

    def data(self):
        """
        Extract comments, msg
        :param comments:
        :param msg:
        :return:
        """

        comments = self._last_comments.values.tolist()
        msg=self._final_msg.values.tolist()

        return comments, msg

    # def text_to_vector(self, text):
    #
    #     text=list(text)
    #     # word = re.compile(r"\w+")
    #     # words = word.findall(text)
    #     return Counter(text)

    # def get_cosine(self, vec1, vec2):
    #     """
    #     Extract word vector
    #     :param word vector comment:
    #     :param word vector msg:
    #     :return:
    #     """
    #     intersection = set(vec1.keys()) & set(vec2.keys())
    #     numerator = sum([vec1[x] * vec2[x] for x in intersection])
    #
    #     sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    #     sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    #     denominator = math.sqrt(sum1) * math.sqrt(sum2)
    #
    #     if not denominator:
    #         return 0.0
    #     else:
    #         return float(numerator) / denominator

    def get_cosine(self, str1, str2):
        """
        Calculate cosine similarity
        :param cosine similarity:
        :return:
        """

        str = (str1, str2)
        tfidf_vectorizer =  TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(str)
        cosine = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
        return cosine[0][1]

def data_write_csv(file_path, datas):
    file_csv=codecs.open(file_path, 'w+', 'utf-8')
    writer=csv.writer(file_csv)
    for data in datas:
        writer.writerow(data)

if __name__ == '__main__':

    inpath = 'D:\PhD Groningen\Publications\TechDebt2021\project_impala.xlsx'

    cs = CosineSimilarity(inpath_last_comment=inpath, inpath_final_msg=inpath)
    comments, msg = cs.data()

    similarity=[]

    i=0
    while i < len(comments)-1:

        #vector1 = cs.text_to_vector(str(comments[i][4]))
        str1=str(comments[i][4])
        d1 = datetime.datetime.strptime(str(comments[i][3]), '%Y-%m-%d %H:%M:%S')

        j=0
        while j < len(msg)-1:

            #vector2 = cs.text_to_vector(str(msg[j][5]))
            str2 = str(msg[j][5])
            d2 = datetime.datetime.strptime(str(msg[j][4]), '%Y-%m-%d %H:%M:%S')
            #cosine = cs.get_cosine(vector1, vector2)
            cosine = cs.get_cosine(str1, str2)
            if abs((d1 - d2).days) < 8 and cosine > 0.7:
                if comments[i][2] == msg[j][1]:
                    similarity.append([comments[i][0], msg[j][0], comments[i][2], msg[j][1], msg[j][2],
                                       comments[i][3], msg[j][4], comments[i][1], msg[j][3], cosine])
                    j+=1
                    break
                elif comments[i][2] == msg[j][2]:
                    similarity.append([comments[i][0], msg[j][0], comments[i][2], msg[j][1], msg[j][2],
                                       comments[i][3], msg[j][4], comments[i][1], msg[j][3], cosine])
                    j += 1
                    break
                else:
                    j += 1
            else:
                j += 1
        i+=1

    print(similarity)

    data_write_csv("D:\PhD Groningen\Publications\TechDebt2021\example.csv", similarity)
