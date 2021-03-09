from datetime import datetime
from pydriller import RepositoryMining
import pandas as pd
import numpy as np
import xlwt
import re
import csv
import codecs

class MsgExtract:
    """
    Class for extracting msg
    """
    def __init__(self, inpath_msg, re_remove):
        """
        Initialization
        :param inpath_msg:
        :param re_remove:
        """
        self._inpath_msg=inpath_msg
        self._re_remove = re_remove

    def msg_extract(self):
        """
        Extract msg
        :param project name:
        :param hash:
        :param committer name:
        :param committer email:
        :param author name:
        :param author email:
        :param msg:
        :param committer date
        :param author date:
        :return:
        """
        msg = []
        for commit in RepositoryMining(self._inpath_msg, only_in_branch='master').traverse_commits():
            message = re.sub(self._re_remove, '', str(commit.msg), flags=re.DOTALL)
            msg.append([commit.project_name,
                        commit.hash,
                        str(commit.committer.name),
                        str(commit.committer.email),
                        str(commit.author.name),
                        str(commit.author.email),
                        str(message),
                        str(commit.committer_date),
                        str(commit.author_date)])

        return msg

def data_write_csv(file_path, datas):
    file_csv=codecs.open(file_path, 'w+', 'utf-8')
    writer=csv.writer(file_csv)
    for data in datas:
        writer.writerow(data)

if __name__ == '__main__':


    inpath = 'D:\PhD Groningen\Publications\TechDebt2021\project\\chromium'
    re_remove_str = '(\{code\}.*?\{code\})|(\{noformat\}.*?\{noformat\})'
    extract = MsgExtract(inpath_msg=inpath, re_remove=re_remove_str)
    msg=extract.msg_extract()
    # print(len(list_info))
    #(msg)
    print(msg)
    print(len(msg))
    data_write_csv("D:\PhD Groningen\Publications\TechDebt2021\dev.csv", msg)