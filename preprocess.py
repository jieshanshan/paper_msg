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
    def __init__(self, inpath_issue, inpath_msg):

        self._issues = pd.read_excel(inpath_issue, sheet_name="precomment", usecols=[2,3,4,6], names=None)
        self._msg = pd.read_excel(inpath_msg, sheet_name="msg", usecols=[1,2,4,6,8])

    def filter(self):
        #     """
        #     Extract last_comment, msg_within_7days
        #     :param last_comment:
        #     :param msg:
        #     :return:
        #     """

        issue=self._issues.values

        last_comment=issue.copy()
        len_issue=len(issue)
        i=0
        while i < len_issue-1:
            if last_comment[i][0]==last_comment[i+1][0]:
                last_comment = np.delete(last_comment,i,axis=0)
                len_issue-=1
            else:
                i+=1

        msg=self._msg.values


        len_msg=len(msg)
        j=0

        while j < len_msg-1:
            k=0
            for k in range(len_issue):
                d1 = datetime.datetime.strptime(str(issue[k][3]),'%Y-%m-%d %H:%M:%S')
                d2 = datetime.datetime.strptime(str(msg[j][4]),'%Y-%m-%d %H:%M:%S')
                if abs((d1-d2).days) < 8:
                    j+=1
                    break
                else:
                    k+=1
                    if k == len_issue-1:
                        msg = np.delete(msg,j,axis=0)
                        len_msg-=1

        last_comment=last_comment.tolist()
        msg=msg.tolist()

        return self._process(last_comment, msg)

    # def extract(self):
    #     """
    #     Extract issue, msg
    #     :param issue:
    #     :param msg:
    #     :return:
    #     """
    #     issues = self._issues.values.tolist()
    #     msg = self._msg.values.tolist()
    #
    #     #return issue, msg, self._sentoken(issue, msg)
    #     return self._process(issues, msg)

    def _process(self, last_comment, msg):

        """
        NLP preprocessing
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

        msg = [str(i[3]) for i in msg]
        new_msg=[]
        for message in str(msg):

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

        return new_comment, new_msg

def data_write_csv(file_path, datas):
    file_csv=codecs.open(file_path, 'w+', 'utf-8')
    writer=csv.writer(file_csv)
    for data in datas:
        writer.writerow(data)

if __name__ == '__main__':

    inpath = 'D:\PhD Groningen\Publications\TechDebt2021\project_impala.xlsx'

    step = TextPreprocess(inpath_issue=inpath, inpath_msg=inpath)
    last_comment, msg = step.filter()


    # print(issue)
    # dimen = np.array(issue).shape
    # print(dimen)
    # print(len(issue))
    print(msg)
    dimen = np.array(msg).shape
    print(dimen)
    print(len(msg))
    #data_write_csv("D:\PhD Groningen\Publications\Survey2020\Example2.xls", issue)

