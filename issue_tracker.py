import re

from jira import JIRA

from scripts.others.config import Config
from scripts.tools.common import CommentInDiscussion, Attachment


class JiraReader:
    """
    Class for querying information from jira
    """

    def __init__(self, url, re_author, re_remove):
        """
        Initialization

        :param url:
        :param re_author:
        :param re_remove:
        """
        self._jira = JIRA(url)
        self._re_author = re_author
        self._re_remove = re_remove

    def query_issue(self, issue_id):
        """
        Query issue by issue ID

        :param issue_id:
        :return:
        """
        issue = self._jira.issue(issue_id)
        return issue, self._comment_and_attachment_process(issue=issue)

    def _comment_and_attachment_process(self, issue):
        """
        Process comments

        :param issue:
        :return:
        """
        list_comments = []
        list_attachment = []

        for c in issue.fields.comment.comments:
            if re.match(self._re_author, str(c.author)) is not None:
                list_comments.append(str(c.author))
                continue

            cid = CommentInDiscussion(author=str(c.author), date=str(c.created),
                                      content=re.sub(self._re_remove, '', c.body.strip(), flags=re.DOTALL))
            list_comments.append(cid)

        for a in issue.fields.attachment:
            if not str(a.filename).endswith('.patch'):
                continue

            at = Attachment(author=str(a.author), date=str(a.created),
                            content=str(a.content), filename=str(a.filename))
            list_attachment.append(at)

        return list_comments, list_attachment

    def query_issue_ids_with_index(self, project_key, start_idx, block_size):
        """
        Query issue by project key

        :param project_key:
        :param start_idx:
        :param block_size:
        :return:
        """
        issues = self._jira.search_issues('project=' + project_key, start_idx, block_size)
        return [issue.key for issue in issues]


if __name__ == '__main__':
    # cf = Config('hadoop.ini')
    jr = JiraReader(url='https://issues.apache.org/jira', re_author='(Hadoop QA)|(Hudson)',
                    re_remove='(\{code\}.*?\{code\})|(\{noformat\}.*?\{noformat\})')
    iss, comments = jr.query_issue(issue_id='HADOOP-7233')
    print(iss.key)
    print(iss.fields.summary)
    print(iss.fields.priority)
    print(iss.fields.issuetype.name)
    print(iss.fields.description)
    print(comments)
    print(jr.query_issue_ids_with_index('HADOOP', 1, 500))
