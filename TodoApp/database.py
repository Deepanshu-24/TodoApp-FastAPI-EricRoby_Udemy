from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL =  'postgresql://postgres:[Deepanshu@246saini]@db.ajhymebglktrkupzugqz.supabase.co:5432/postgres'

engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
