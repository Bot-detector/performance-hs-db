from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Database configuration
DATABASE_URI = "mysql+pymysql://root:root_bot_buster@localhost:3333/playerdata"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URI, echo=False)

# Create a configured "Session" class
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get a database session
@contextmanager
def get_session() -> Iterator[Session]:
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
