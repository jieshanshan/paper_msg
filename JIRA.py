import openpyxl
import re
import pandas as pd
import numpy as np
import xlwt
from jira import JIRA

class JiraReader:
    """
    Class for querying information from jira
    """

    def __init__(self, url, re_remove):
        """
        Initialization
        :param url:
        :param re_remove:
        """
        self._jira = JIRA(url)
        self._re_remove = re_remove

    def query_issue(self, issue_id):
        """
        Query issue by issue ID

        :param issue_id:
        :return:
        """
        issue = self._jira.issue(issue_id)
        #return issue, self._sum_descrip(issue=issue), self._comment_process(issue=issue)
        return issue, self._sum_descrip(issue=issue)

    def _sum_descrip(self, issue):
        """
        Process summary and description

        :param issue:
        :return:
        """
        list_summary = []
        list_description = []
        list_summary.append(str(issue.fields.summary))

        #content = re.sub(self._re_remove, '', c.body.strip(), flags=re.DOTALL))

        issue.fields.description = re.sub(self._re_remove, '', str(issue.fields.description), flags=re.DOTALL)
        list_description.append(str(issue.fields.description))

        return list_summary, list_description

    # def _comment_process(self, issue):
    #     """
    #     Process comments
    #
    #     :param issue:
    #     :return:
    #     """
    #     list_comment = []
    #
    #     for com in issue.fields.comment.comments:
    #
    #         com.body = re.sub(self._re_remove, ' ', com.body, flags=re.DOTALL)
    #
    #         list_comment.append(str(com.body))
    #
    #     return list_comment


    # def query_issue_ids_with_index(self, project_key, start_idx, block_size):
    #     """
    #     Query issue by project key
    #
    #     :param project_key:
    #     :param start_idx:
    #     :param block_size:
    #     :return:
    #     """
    #     issues = self._jira.search_issues('project=' + project_key, start_idx, block_size)
    #     return [issue.key for issue in issues]

def data_write(file_path, datas):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    i = 0
    for data in datas:
        for j in range(len(data)):
                sheet1.write(i,j,data[j])
        i = i + 1
    f.save(file_path)


if __name__ == '__main__':


    excel="D:\PhD Groningen\Publications\Survey2020\Example.xlsx"
    re_remove_str = '(\{code\}.*?\{code\})|(\{noformat\}.*?\{noformat\})'
    jira = JiraReader(url='https://issues.apache.org/jira', re_remove=re_remove_str)

    df = pd.read_excel(excel, usecols=[0], names=None)
    list_key = df.values.tolist()
    list_info = []

    #:param reporter:
    #:param type:
    #:param status:
    #:param priority:
    #:param resolution:
    #:param created_date:
    #:param resolution_date:
    #:param updated_date:

    for key in list_key:
        #iss, sum_des, comments = jira.query_issue(issue_id=key[0])
        iss, sum_des = jira.query_issue(issue_id=key[0])
        for s in sum_des:
            list_info.append([s, str(iss.key), str(iss.fields.creator), str(iss.fields.created),
                              str(iss.fields.reporter.displayName), str(iss.fields.issuetype), str(iss.fields.status),
                              str(iss.fields.priority), str(iss.fields.resolution),
                              iss.fields.created, iss.fields.resolutiondate, iss.fields.updated])
        for c in iss.fields.comment.comments:
            c.body = re.sub(re_remove_str, ' ', c.body, flags=re.DOTALL)
            list_info.append([c.body, str(iss.key), str(c.author),str(c.created),
                                str(iss.fields.reporter.displayName), str(iss.fields.issuetype), str(iss.fields.status),
                                str(iss.fields.priority), str(iss.fields.resolution),
                                iss.fields.created, iss.fields.resolutiondate, iss.fields.updated])

    print(list_info)
    # dimen = np.array(list_info).shape
    # print(dimen)
    # print(len(list_info))
    data_write("D:\PhD Groningen\Publications\Survey2020\Example2.xls", list_info)
