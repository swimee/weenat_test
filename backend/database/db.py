from datetime import datetime
from os import environ

import databases
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

now = datetime.now().isoformat()

DATABASE_URL = environ["DATABASE_URL"]

database = databases.Database(DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
    echo=True,
)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

metadata = MetaData()
measurements = Table(
    "measurements",
    metadata,
    Column("pk", Integer, primary_key=True),
    Column("id", String),
    Column("date", DateTime, default=now),
    Column("precip", Float),
    Column("temp", Float),
    Column("hum", Float),
    schema="public",
)

metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
