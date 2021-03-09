import openpyxl
import re
import pandas as pd
import numpy as np

import string
import xlwt
import csv
import codecs
import datetime
import nltk
nltk.download('punkt')
from nltk import word_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

class TextPreprocess:
    """
    Class for NLP pre-process of issue and msg
    """
    def __init__(self, inpath_issue, inpath_msg, inpath_comment, inpath_last_comment):

        self._issues = pd.read_excel(inpath_issue, sheet_name="issue", usecols=[2])    #issue_key
        self._comments = pd.read_excel(inpath_comment, sheet_name="precomment", usecols=[2, 3, 4, 5, 6])
        self._msg = pd.read_excel(inpath_msg, sheet_name="msg", usecols=[1,2,4,6,8])
        self._last_comments = pd.read_excel(inpath_last_comment, sheet_name="last_comment", usecols=[0, 2, 3, 4, 5], header=None)

    # def msg_has_issuekey(self):
    #     """
    #     Step 1
    #     If msg has issue key
    #     :param issue key:
    #     :param msg:
    #     :return:
    #     """
    #
    #     issue_key=self._issues.values.tolist()
    #     msg = self._msg.values.tolist()
    #     mapping=[]
    #     simple_key = []                          #remove duplicated
    #     for simple in issue_key:
    #         if simple not in simple_key:
    #             simple_key.append(simple)
    #
    #     for i in range(len(simple_key)):
    #         k = str(simple_key[i]).translate(str.maketrans("", "", string.punctuation))  # remove punctuation
    #         for j in range(len(msg)):
    #             m = str(msg[j][3]).translate(str.maketrans("", "", string.punctuation))  # remove punctuation
    #             if re.search(k, m,flags=0) != None:
    #                  #print(str(issue_key[i]))
    #                  mapping.append([str(simple_key[i]), str(msg[j][3])])
    #                  j+=1
    #             else:
    #                  j+=1
    #
    #
    #     return mapping

    def filter_comment(self):
        """
        Step 2:
        Extract last_comment
        :param last_comment:
        :return:
        """

        comments=self._comments.values

        last_comment=comments.copy()
        len_issue=len(comments)
        i=0
        while i < len_issue-1:
            if last_comment[i][0]==last_comment[i+1][0]:
                last_comment = np.delete(last_comment,i,axis=0)
                len_issue-=1
            else:
                i+=1

        last_comment=last_comment.tolist()

        return self._process_comment(last_comment)


    def _process_comment(self, last_comment):

        """
        Step 3:
        NLP preprocessing for comments
        :return:
        """
        comment=[str(i[2]) for i in last_comment]
        new_comment=[]
        for c in comment:

            url_reg = r'[a-z]*[:.]+\S+'
            c= re.sub(url_reg, '',c)  #remove url
            c=c.lower()               #covert text to lowercase
            c=re.sub(r'\d+','',c)     #remove numbers
            c=c.translate(str.maketrans("","", string.punctuation)) #remove punctuation
            c=c.strip()               #remove whitespaces
            c=word_tokenize(c)        #Tokenization
            stop_words = set(stopwords.words('english'))
            c=[i for i in c if not i in stop_words]     #remove stop words
            stemmer=SnowballStemmer("english")
            c=[stemmer.stem(word) for word in c]        #stemming
            lemmatizer=WordNetLemmatizer()
            c=[lemmatizer.lemmatize(word) for word in c]
            new_comment.append(c)

        return last_comment, new_comment

    def filter_msg(self):
        """
        Step 4:
        Extract msg same contributors and within 7 days
        :param msg:
        :return:
        """

        final_comments=self._last_comments.values
        msg=self._msg.values
        len_msg=len(msg)
        len_final_comment=len(final_comments)
        j=0

        while j < len_msg-1:
            k=0
            #for k in range(len_final_comment-1):
            while k < len_final_comment-1:
                d1 = datetime.datetime.strptime(str(final_comments[k][3]),'%Y-%m-%d %H:%M:%S')
                d2 = datetime.datetime.strptime(str(msg[j][4]),'%Y-%m-%d %H:%M:%S')

                # if final_comments[k][2] == msg([j][1]) and abs((d1-d2).days) < 8:
                if abs((d1 - d2).days) < 8:
                    if final_comments[k][2] == msg[j][1]:
                        j+=1
                        break
                    elif final_comments[k][2] == msg[j][2]:
                        j+=1
                        break
                    else:
                        k+=1
                        if k == len_final_comment-1:
                            msg = np.delete(msg,j,axis=0)
                            len_msg-=1
                else:
                    k += 1
                    if k == len_final_comment - 1:
                        msg = np.delete(msg, j, axis=0)
                        len_msg -= 1
        msg=msg.tolist()

        return self._process_msg(msg)

    def _process_msg(self, msg):

        """
        Step 5:
        NLP preprocessing for msg
        :return:
        """
        mes=[str(i[3]) for i in msg]
        new_msg = []
        for message in mes:

            url_reg = r'[a-z]*[:.]+\S+'
            message= re.sub(url_reg, '',message)  #remove url
            message=message.lower()               #covert text to lowercase
            message=re.sub(r'\d+','',message)     #remove numbers
            message=message.translate(str.maketrans("","", string.punctuation)) #remove punctuation
            message=message.strip()               #remove whitespaces
            message=word_tokenize(message)        #Tokenization
            stop_words = set(stopwords.words('english'))
            message=[i for i in message if not i in stop_words]     #remove stop words
            stemmer=SnowballStemmer("english")
            message=[stemmer.stem(word) for word in message]        #stemming
            lemmatizer=WordNetLemmatizer()
            message=[lemmatizer.lemmatize(word) for word in message]
            new_msg.append(message)

        return msg, new_msg

def data_write_csv(file_path, datas):
    file_csv=codecs.open(file_path, 'w+', 'utf-8')
    writer=csv.writer(file_csv)
    for data in datas:
        writer.writerow(data)

if __name__ == '__main__':

    inpath = 'D:\PhD Groningen\Publications\TechDebt2021\project_impala.xlsx'

    step = TextPreprocess(inpath_issue=inpath, inpath_msg=inpath, inpath_comment=inpath, inpath_last_comment=inpath)

    #mapping = step.msg_has_issuekey()
    #last_comment, new_comment = step.filter_comment()
    msg, new_msg = step.filter_msg()


    #print(mapping)
    # print(last_comment)
    # print(new_comment)
    # dimen = np.array(new_comment).shape
    # print(dimen)
    # print(len(new_comment))
    # print(msg)
    # dimen = np.array(msg).shape
    # print(dimen)
    # print(len(msg))
    data_write_csv("D:\PhD Groningen\Publications\TechDebt2021\example.csv", msg)
    data_write_csv("D:\PhD Groningen\Publications\TechDebt2021\example.xls", new_msg)

