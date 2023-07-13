import sqlalchemy as sq
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData,create_engine
from sqlalchemy.orm import Session
from tokens import puti
Base = declarative_base()



metadata = MetaData()
def create_tables(engine):
        Base.metadata.create_all(engine)

engine = create_engine(puti)

class Viewed(Base):
    __tablename__ = 'viewed'
    profile_id = sq.Column(sq.Integer, primary_key=True)
    worksheet_id = sq.Column(sq.Integer, primary_key=True)
        
    def __str__ (self):
        return f'{self.profile_id}: {self.worksheet_id}'

    def create_tables(engine):
        Base.metadata.create_all(engine)


def add_user(engine,profile_id,worksheet_id):
     with Session(engine) as session:
          to_bd = Viewed(profile_id = profile_id, worksheet_id = worksheet_id)
          session.add(to_bd)
          session.commit()


def check_user(engine,profile_id,worksheet_id):
    with Session(engine) as session:
        from_bd = session.query(Viewed). filter(
             Viewed.profile_id == profile_id, 
             Viewed.worksheet_id == worksheet_id).first()
        return True if from_bd else False 



