import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import psycopg2 
from basa import add_user , check_user, engine



from tokens import comunity_token, acces_token
from backend import vkTools

conn = psycopg2.connect(dbname="Vkind", user="postgres", password="saruma0", host="127.0.0.1")


vk = vk_api.VkApi(token=comunity_token)
tools = vkTools(acces_token)
# engine = create_engine(puti)
# def create_tables(conn):
#         Base.metadata.drop_all(conn)
#         Base.metadata.create_all(conn)




  
# sql = ''' DELETE FROM Viewed '''
# with conn.cursor() as cursor:
#     cursor.execute(sql)
#     conn.commit()




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
                        self.worksheets = self.vk_tools.search_worksheet(
                            self.params, self.offset)
                        worksheet = self.worksheets.pop()
                        while check_user(engine,event.user_id,worksheet['id']):
                             if True: 
                                    worksheet = self.worksheets.pop()
                                    print('такой id уже есть')
                                    continue
                            
                        photos = self.vk_tools.get_photos(worksheet['id'])
                        photo_string = ''

                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                        self.offset += 10
                    self.message_send(event.user_id, f'имя:{worksheet ["name"]} ссылка: https://vk.com/id{worksheet["id"]}',
                                      attachment = photo_string)
                    while add_user(engine,event.user_id,worksheet['id']):
                        
                        continue
                            
                                    
                   
                elif event.text.lower() =='пока':
                    self.message_send(event.user_id, 'До новых встреч')
                     
                     
           

if __name__ == '__main__':
    bot_interfasce = BotInterFace(comunity_token, acces_token)
    bot_interfasce.event_handler()  
    
    
 