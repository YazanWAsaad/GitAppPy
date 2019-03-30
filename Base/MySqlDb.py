

from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker





class CDatabase:
   def __init__(self,host:str, user:str, Password:str, Pipe:str)->bool:
      return
