from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, String, Integer, Boolean, MetaData, ForeignKey

Base = declarative_base()