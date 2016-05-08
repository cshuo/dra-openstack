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

    ids = Column(String(40), primary_key=True)
    name = Column(String(32))
    vm_type = Column(String(32))


