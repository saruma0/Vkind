import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import psycopg2 
from basa import *


from tokens import comunity_token, acces_token
from backend import vkTools
# puti = 'postgresql+psycopg2://postgres:saruma0@localhost:5432/Vkind'
# engine = sqlalchemy. create_engine(puti) 
# conn = psycopg2.connect(puti)
conn = psycopg2.connect(dbname="Vkind", user="postgres", password="saruma0", host="127.0.0.1")
cursor = conn.cursor()
def create_tables(engine):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)


vk = vk_api.VkApi(token=comunity_token)
tools = vkTools(acces_token)




class BotInterFace():
    def __init__(self,comunity_token, acces_token):
        self.vk = vk_api.VkApi(token=comunity_token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_tools = vkTools(acces_token)
        self.params = {}
        self.worksheets = []
        self.offset = 0
        
        

    def message_send(self, user_id,message,attachment=None):
        self.vk.method('messages.send',
                {'user_id': user_id,
                'message': message,
                'attachment':attachment,
                'random_id': get_random_id()})
    

    def event_handler(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower() =='привет':
                    self.params = self.vk_tools.get_profile_info(event.user_id)
                    self.message_send(event.user_id, f'Привет, {self.params["name"]}, напиши поиск если хочешь начать подбор партнёра')
                elif event.text.lower() =='поиск':
                    self.message_send(event.user_id, 'Начинаем поиск')
                    if self.worksheets:
                        worksheet = self.worksheets.pop() 
                        photos = self.vk_tools.get_photos(worksheet['id'])
                        photo_string = ''
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                    else:   
                        self.worksheets = self.vk_tools.search_worksheet(self.params, self.offset)
                        
                        worksheet = self.worksheets.pop()
                        cursor.execute("SELECT worksheet_id FROM Viewed ")
                        worksheet_id = cursor.fetchone()
                        for worksheet['id'] in worksheet_id:
                            if worksheet['id'] == worksheet_id:
                                return self.worksheets
                            continue
            
                        # Viewed.objects.filter(profile_id='event.user_id',worksheet_id='worksheet["id"]').exists()
                        
                        photos = self.vk_tools.get_photos(worksheet['id'])
                        photo_string = ''
                        
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                        self.offset += 10
                    self.message_send(event.user_id, f'имя:{worksheet ["name"]} ссылка: https://vk.com/id{worksheet["id"]}',
                                      attachment = photo_string)
                    bob = (event.user_id, worksheet["id"])
                    cursor.execute("INSERT INTO Viewed (profile_id, worksheet_id)VALUES (%s, %s) on conflict do nothing", bob)
                    conn.commit()  
                    print("Данные добавлены")
                   
                elif event.text.lower() =='пока':
                    self.message_send(event.user_id, 'До новых встреч')
                    cursor.close()
                    conn.close() 
           

if __name__ == '__main__':
    bot_interfasce = BotInterFace(comunity_token, acces_token)
    bot_interfasce.event_handler()    
    
    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    # create_tables(engine)
                    # Session = sessionmaker(bind = engine)
                    # session = Session()
                    # course1 = Viewed2(profile_id = 'event.user_id')
                    # course2 = Viewed2(worksheet_id = 'worksheet_id')
                    # session.add(course1, course2)
                    # session.commit()
                    # session.close()
    # def add_user(engine,profile_id,worksheet_id):
    #     with Session(engine) as session:
    #         to_bd = Viewed2(profile_id = profile_id, worksheet_id = worksheet_id)
    #         session.add(to_bd)
    #         session.commit()

                   
                    
                    # for worksheet in add_user(profile_id,worksheet_id):
                    #      profile_id = profile_id, 
                    #      worksheet_id = worksheet_id
                
                    


                
                    # try:
                    #     with conn.cursor() as cur:
                    #         cur.execute("""INSERT INTO Viewed (profile_id, worksheet_id)
                    #           VALUES ('event.user_id', 'worksheet["id"]');""")
                    #         cur.add()
                    #         print("Данные успешно добалены")
                    # except (Exception,Error) as error:
                    #     print("Ошибка при работе с PostgreSQL2", error)
                    
                    
                    
                    
                    
                    
#                 elif event.text.lower() =='пока':
#                     self.message_send(event.user_id, 'До новых встреч')



# if __name__ == '__main__':
#     bot_interfasce = BotInterFace(comunity_token, acces_token)
#     bot_interfasce.event_handler()
