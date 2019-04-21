import json
import time
import os
import urllib
import requests
import random
from config import *


def _check_quota(response):
    requests_left = int(response.headers['X-RateLimit-Remaining'])
    if (requests_left == 0):
        print("Sleeping for 65 minutes... Good Night.")
        time.sleep(65 * 60)
    if requests_left % 10 == 0: print("Requests Left: " + str(requests_left))





class GitRepoCls:
    def __init__():
        return;

    def Connect(self, user:str,Password:str)->bool:
        self.session = requests.Session()
        self.session.auth = ('user', 'password')
        return (True);


    def _get_user_organizations(self, user):
       response = self.session.get('https://api.github.com/users/' + user + "/orgs")
       _check_quota(response)
       if (response.ok):
          orgs = json.loads(response.text or response.content)
          return [org['login'] for org in orgs]


    # pick a radom repository by searching with a random keyword
    def _get_random_repo(self,random_words:list):
       while True:
          keyword = random.choice(random_words)
          response = self.session.get('https://api.github.com/legacy/repos/search/' + keyword)
          _check_quota(response)
          if (response.ok):
             repos = json.loads(response.text or response.content)
             if (len(repos['repositories']) > 0):
                repo = random.choice(repos['repositories'])
                userame = repo['username']
                orgs = self._get_user_organizations(userame)
                for org in orgs:
                   response = self.session.get('https://api.github.com/users/' + org + '/repos')
                   _check_quota(response)
                   if (response.ok):
                      repos = json.loads(response.text or response.content)
                      return random.choice(repos)

    # crawl around and gather data until the target sample size is reached
    def crawl(self, sample_size):
       while (sample_size > self.db_session.query(self.repository_table).count()):
          try:
             repo = self._get_random_repo();
             i = repository_table.insert([repo])
             i.execute()
             url = 'https://api.github.com/repos/' + repo['full_name'] + '/commits?per_page=100'
             while url is not None:
                response = self.session.get(url)
                _check_quota(response)
                if (response.ok):
                   commits = json.loads(response.text or response.content)
                   for commit in commits:
                      committer = None
                      if 'author' in commit and commit['author'] is not None:
                         committer = commit['author']['login']
                      else:
                         committer = commit['commit']['author']['name'].encode('unicode_escape')

                      i = self.commit_table.insert(
                         dict(
                            repository_id=repo['id'],
                            committer=committer))
                      i.execute()
                   links = response.links
                   if 'next' in links:
                      url = response.links["next"]['url']
                   else:
                      url = None
                else:
                   url = None

             for tag in ['closed', 'open']:
                url = 'https://api.github.com/repos/' + repo['full_name'] + '/issues?per_page=100&state=' + tag
                while url is not None:
                   response = self.session.get(url)
                   _check_quota(response)
                   if (response.ok):
                      issues = json.loads(response.text or response.content)
                      for issue in issues:
                         i = self.issue_table.insert(
                            dict(
                               number=issue['number'],
                               repository_id=repo['id'],
                               creator=issue['user']['login'],
                               open_date=issue['created_at'],
                               close_date=issue['closed_at']))
                         i.execute()
                      links = response.links
                      if 'next' in links:
                         url = response.links["next"]['url']
                      else:
                         url = None
                   else:
                      url = None

             sample_size -= 1

          except Exception as e:
             print(e)
