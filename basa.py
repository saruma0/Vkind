import sqlalchemy as sq
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData,create_engine
from sqlalchemy.orm import Session
Base = declarative_base()

# from tokens import puti
# # puti = 'postgresql+psycopg2://postgers:saruma0@localhost:5432/Vkind'
# # engine = sqlalchemy.create_engine(puti)

# metadata = MetaData()

# # Session = sessionmaker(bind = engine)



# # try:
# #     conn = psycopg2.connect(user="postgres",
# #                                   password="saruma0",
# #                                   host="localhost",
# #                                   port="5432",
# #                                   database="Vkind")

    
# # except:
# #     print('Не удаётся подключитьсяк БД')


class Viewed(Base):
    __tablename__ = 'viewed'
    profile_id = sq.Column(sq.Integer, primary_key=True)
    worksheet_id = sq.Column(sq.Integer, primary_key=True)
        
    def __str__ (self):
        return f'{self.profile_id}: {self.worksheet_id}'

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


# def add_user(engine,profile_id,worksheet_id):
#     with Session(engine) as session:
#             to_bd = Viewed(profile_id = profile_id, worksheet_id = worksheet_id)
#             session.add(to_bd)
#             session.commit()
 
     
            

# def check_user(engine,profile_id,worksheet_id):
#     with Session(engine) as session:
#         from_bd = session.query(Viewed). filter(
#              Viewed.profile_id == profile_id, 
#              Viewed.worksheet_id == worksheet_id).first()
#         return True if from_bd else False 



# if __name__ == '__main__':
#      engine = create_engine(puti)
#      Base.metadata.create_all(engine)
#     #  add_user(engine, 2113, 123242)
#     #  res = check_user(engine, 2113, 123242)
#     #  print(res)


# # try:
# #     with conn.cursor() as cur:
# #         cur.execute("""CREATE TABLE Viewed (profile_id SERIAL PRIMARY KEY, 
# #                         worksheet_id cidr); """)
# #         conn.commit()
# #     print("Таблица успешно создана в PostgreSQL")
# # except (Exception, Error) as error:
# #     print("Ошибка при работе с PostgreSQL", error)
# # finally:
# #     if conn:
# #         conn.close()
# #         print("Соединение с PostgreSQL закрыто")
# # 
# # 
# # 