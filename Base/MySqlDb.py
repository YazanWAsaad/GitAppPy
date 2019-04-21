

from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker





class CDatabase:
   def __init__():
      return

   def Connect(self,host:str, Pipe:int, user:str, Password:str)->bool:
      self.engine = create_engine('mysql://' + 'root:MySqlPassword' + '@' + '127.0.0.1' + ':' + str(3306) + '/' + 'MySQL', echo=False)
      self.metadata = MetaData(bind=self.engine)
      self.Session = sessionmaker(bind=self.engine)
      self.db_session = self.Session()
      return(True);

   def CreateTables(self)->bool:
      self.repository_table = Table('repository', self.metadata
                               , Column('id', Integer, primary_key=True), Column('name', String(60)),
                               Column('forks', Integer)
                               , Column('open_issues', Integer), Column('watchers', Integer)
                               , mysql_engine='InnoDB', )

      self.issue_table = Table('issue', self.metadata,
                          Column('id', Integer, autoincrement=True, primary_key=True),
                          Column('repository_id', Integer, ForeignKey('repository.id')),
                          Column('creator', String(60)),
                          Column('number', Integer),
                          Column('open_date', DateTime),
                          Column('close_date', DateTime),
                          mysql_engine='InnoDB',
                          )

      self.commit_table = Table('commit', self.metadata,
                           Column('id', Integer, autoincrement=True, primary_key=True),
                           Column('repository_id', Integer, ForeignKey('repository.id')),
                           Column('committer', String(60)),
                           mysql_engine='InnoDB'
                           )
      # create tables in database
      self.metadata.create_all()
      return(True);



