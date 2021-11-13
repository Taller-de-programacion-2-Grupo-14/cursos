import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(os.environ.get("DATABASE_URL"), echo=True, future=True)

Base = declarative_base()
