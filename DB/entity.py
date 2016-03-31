# coding: utf-8
__author__ = 'cshuo'

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine, 
    Table, 
    Column, 
    Integer, 
    String, 
    MetaData, 
    ForeignKey
)

Base = declarative_base()


class Vm(Base):
    __tablename__ = 'vm'

    name = Column(String(32), primary_key=True)
    vm_type = Column(String(32))
    host = Column(String(32))


