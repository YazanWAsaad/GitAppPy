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
from GitAppPy.Base.Config import ConfigCls
from GitAppPy.Base.SqlDb import Database

#from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
#from sqlalchemy import Integer, String, DateTime, VARCHAR
#from sqlalchemy import func
#from sqlalchemy.orm import sessionmaker





configuration:ConfigCls = ConfigCls('./Config.ini')









db_sql:Database = Database();

db_engine, db_session = Database.DbConnect(configuration);


repo_table , repo_arr = Database.DbAddRepoTable();
issues_arr, issue_table =  Database.DbAddIssuesTable();
commit_table, commit_arr =  Database.DbAddCommitTable();
milestone_table, milestone_arr = Database.DbAddMilestonesTable();
comments_table, comments_arr =  Database.DbAddCommentsTable();


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
db_sql.create_all()




git_user=configuration.GitUser()
git_password=configuration.GitPassword()
git_session = requests.Session()
git_session.auth = (git_user, git_password)


# Get some random words
def RandomWords(config:Config)->list:
   combined_words = []
   words_aspects = config.WordsAspects();
   words_domain = config.WordsDomain();

   for domain in words_domain:
      for aspect in words_aspects:
         if(domain and aspect):
            combined_words.append(domain + '+' + aspect)
   return (combined_words);

random_words = RandomWords(configuration);









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
      response = git_session.get('https://api.github.com/legacy/repos/search/' +  "q=" +keyword)
      _check_quota(response)
      if (response.ok):
         repos = json.loads(response.text or response.content)
         print("Key words:" + keyword + " Repositories found:" + str(len(repos['repositories'])))
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
   while (sample_size > db_session.query(repo_table).count()):
      try:
         repo = {};
         repo_rand = _get_random_repo();
         repo = InsertFields(repo_arr, repo_rand, repo_table)

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

