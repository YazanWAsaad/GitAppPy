from config import *
from GitAppPy.Base.Config import ConfigCls

from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String, DateTime, VARCHAR
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker





class Database:
   def __init__(self):

   def DbConnect(self, config:Config):
      db_host = config.DbHost();
      db_user = config.DbUser();
      db_password = config.DbPassword();
      self.engine = create_engine('mysql://' + 'root:' + db_password + '@' + db_host + ':' + str(3306) + '/' + 'github', echo=False)
      Session = sessionmaker(bind=self.engine)
      self.db_session = Session()
      self.db_metadata = MetaData(bind=self.engine)
      return(self.engine, self.db_session)


   def DbAddRepoTable(self):
      arr=['id', 'name', 'forks', 'open_issues', 'watchers'];
      table = Table('repository', self.db_metadata
                      , Column('id', Integer, primary_key=True)
                      , Column('name', String(60)), Column('forks', Integer)
                      , Column('open_issues', Integer)
                      , Column('watchers', Integer)
                      , mysql_engine='InnoDB')
      return(table,arr);


   def DbAddIssuesTable(self):
      arr = ['id', 'repository_id', 'creator', 'number', 'open_date', 'close_date'];
      table = Table('issue', self.db_metadata
                          ,   Column('id', Integer, autoincrement=True, primary_key=True)
                          ,   Column('repository_id', Integer, ForeignKey('repository.id'))
                          ,   Column('creator', String(60))
                          ,   Column('number', Integer)
                          ,   Column('open_date', DateTime)
                          ,   Column('close_date', DateTime)
                          ,   Column('issue', VARCHAR(500))
                          ,   mysql_engine='InnoDB')
      return (table, arr);


   def DbAddCommitTable(self):
      arr = ['id', 'repository_id', 'committer'];
      table = Table('commit', self.db_metadata ,
                           Column('id', Integer, autoincrement=True, primary_key=True),
                           Column('repository_id', Integer, ForeignKey('repository.id')),
                           Column('committer', String(60)),
                           mysql_engine='InnoDB')
      return (table, arr);

   def DbAddMilestonesTable(self):
      arr = ['id', 'repository_id', 'name', 'creator', 'descripcion'];
      table = Table('millstone', self.db_metadata ,
                           Column('id', Integer, autoincrement=True, primary_key=True),
                           Column('repository_id', Integer, ForeignKey('repository.id')),
                           Column('name', String(60)),
                           Column('creator', String(60)),
                           Column('description', VARCHAR(500))
                           )
      return (table, arr);

   def DbAddCommentsTable(self):
      arr = ['id', 'issue_id', 'body'];
      table = Table('comments', self.db_metadata,
                          Column('id', Integer, autoincrement=True, primary_key=True),
                          Column('issue_id', Integer, ForeignKey('issue.id')),
                          Column('body', VARCHAR(500)))
      return (table, arr);

   def DbCreateAll(self):
      self.db_metadata.create_all()
      return;
