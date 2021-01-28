import sqlalchemy
from sqlalchemy.orm import sessionmaker

en = sqlalchemy.create_engine('sqlite:///db.sqlite3', echo=True)
Session = sessionmaker(bind=en)