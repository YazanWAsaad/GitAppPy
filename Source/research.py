##############################################################
# research.py
#
# Gathers and stores data using the GitHub REST API (https://developer.github.com/v3/).
#
# License: MIT 2014 Kevin Peterson
##############################################################

import json
import time
import os
import urllib
import requests
import random
from config import *
import json
from datetime import datetime
from Base import Config
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String, DateTime, VARCHAR
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

ConfigFile:Config = Config.ConfigCls('../Config.ini')
db_host = ConfigFile.DbHost();
db_user = ConfigFile.DbUser();
db_password = ConfigFile.DbPassword();
#engine = create_engine('mysql://' + 'root:MySqlPassword' + '@' + '127.0.0.1' + ':' + str(3306) + '/' + 'MySQL', echo=False)
engine = create_engine('mysql://' + 'root:' + db_password + '@' + db_host + ':' + str(3306) + '/' + 'github', echo=False)

metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
db_session = Session()

repo_fields_arr=['id', 'name', 'forks', 'open_issues', 'watchers'];
repository_table = Table('repository', metadata
                         , Column('id', Integer, primary_key=True), Column('name', String(60)), Column('forks', Integer)
                         , Column('open_issues', Integer), Column('watchers', Integer)
                         , mysql_engine='InnoDB', )


issues_arr = ['id', 'repository_id', 'creator', 'number', 'open_date', 'close_date'];
issue_table = Table('issue', metadata,
                    Column('id', Integer, autoincrement=True, primary_key=True),
                    Column('repository_id', Integer, ForeignKey('repository.id')),
                    Column('creator', String(60)),
                    Column('number', Integer),
                    Column('open_date', DateTime),
                    Column('close_date', DateTime),
                     Column('issue', VARCHAR(500)),
                    mysql_engine='InnoDB',
                    )



commit_arr = ['id', 'repository_id', 'committer'];
commit_table = Table('commit', metadata,
                     Column('id', Integer, autoincrement=True, primary_key=True),
                     Column('repository_id', Integer, ForeignKey('repository.id')),
                     Column('committer', String(60)),
                     mysql_engine='InnoDB'
                     )

millstone_arr = ['id', 'repository_id', 'name', 'creator', 'descripcion'];
millstone_table = Table('millstone' ,metadata,
                        Column('id', Integer, autoincrement=True, primary_key=True),
                        Column('repository_id', Integer, ForeignKey('repository.id')),
                        Column('name', String(60)),
                        Column('creator', String(60)),
                        Column('description', VARCHAR(500)),
                    )

comments_arr = ['id', 'issue_id', 'body'];
comments_table = Table('comments', metadata,
                      Column('id', Integer, autoincrement=True, primary_key=True),
                      Column('issue_id',  Integer, ForeignKey('issue.id')),
                      Column('body', VARCHAR),
                       )




# create tables in database
metadata.create_all()

git_session = requests.Session()
git_user=ConfigFile.GitUser()
git_password=ConfigFile.GitPassword()
git_session.auth = (git_user, git_password)

# Get some random words
f = open('words.txt', 'r')
print('Hello')
words = f.read()
print(words)
random_words = words.split('\n')





def _check_quota(response):
   requests_left = int(response.headers['X-RateLimit-Remaining'])
   if (requests_left == 0):
      print("Sleeping for 65 minutes... Good Night.")
      time.sleep(65 * 60)
   if requests_left % 10 == 0: print("Requests Left: " + str(requests_left))


def _get_user_organizations(user):
   response = git_session.get('https://api.github.com/users/' + user + "/orgs")
   _check_quota(response)
   if (response.ok):
      orgs = json.loads(response.text or response.content)
      return [org['login'] for org in orgs]


# pick a radom repository by searching with a random keyword
def _get_random_repo():
   while True:
      keyword = random.choice(random_words)
      response = git_session.get('https://api.github.com/legacy/repos/search/' + keyword)
      _check_quota(response)
      if (response.ok):
         repos = json.loads(response.text or response.content)
         if (len(repos['repositories']) > 0):
            repo = random.choice(repos['repositories'])
            userame = repo['username']
            orgs = _get_user_organizations(userame)
            for org in orgs:
               response = git_session.get('https://api.github.com/users/' + org + '/repos')
               _check_quota(response)
               if (response.ok):
                  repos = json.loads(response.text or response.content)
                  return random.choice(repos)


def InsertFields(names:list,fields:dict, table)->dict:
   filtered = {};
   for field in fields:
      if field in names:
         filtered[field] = fields[field];
   i = table.insert([filtered])
   i.execute()
   return(filtered);


# crawl around and gather data until the target sample size is reached
def crawl(sample_size):
   while (sample_size > db_session.query(repository_table).count()):
      try:
         repo = {};
         repo_rand = _get_random_repo();
#         for repo_field in repo_rand:
#            if repo_field in repo_fields_arr:
#               repo[repo_field]=repo_rand[repo_field]
#         i = repository_table.insert([repo])
#         i.execute()
         repo = InsertFields(repo_fields_arr, repo_rand, repository_table)

         url = 'https://api.github.com/repos/' + repo_rand['full_name'] + '/commits?per_page=100'
         while url is not None:
            response = git_session.get(url)
            _check_quota(response)
            if (response.ok):
               commits = json.loads(response.text or response.content)
               for commit in commits:
                  committer = None
                  if 'author' in commit and commit['author'] is not None:
                     committer = commit['author']['login']
                  else:
                     committer = commit['commit']['author']['name'].encode('unicode_escape')

#                  i = commit_table.insert(dict(repository_id=repo['id'], committer=committer))
#                  i.execute()
                  InsertFields(commit_arr, dict(repository_id=repo_rand['id'], committer=committer), commit_table)

               links = response.links
               if 'next' in links:
                  url = response.links["next"]['url']
               else:
                  url = None
            else:
               url = None

         for tag in ['closed', 'open']:
            url = 'https://api.github.com/repos/' + repo_rand['full_name'] + '/issues?per_page=100&state=' + tag
            while url is not None:
               response = git_session.get(url)
               _check_quota(response)
               if (response.ok):
                  issues = json.loads(response.text or response.content)
                  for issue in issues:
                     created_at = datetime.strptime(issue['created_at'].replace('T',' ').replace('Z',''),"%Y-%m-%d %H:%M:%S")
                     closed_at = datetime.strptime(issue['closed_at'].replace('T',' ').replace('Z',''),"%Y-%m-%d %H:%M:%S")
                     i = issue_table.insert(
                           dict( number=issue['number'], repository_id=repo_rand['id'], creator=issue['user']['login'],
                                 open_date=created_at, close_date=closed_at));
                           #open_date=issue['created_at'], close_date=issue['closed_at']))
                     i.execute()
                     InsertFields()

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


crawl(5000)

