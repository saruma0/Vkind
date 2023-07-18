from pprint import pprint
from datetime import datetime
import vk_api
from vk_api.exceptions import ApiError
import vk_api


from tokens import acces_token


class vkTools:
    def __init__(self,acces_token):
        self.vkapi = vk_api.VkApi(token=acces_token)

    def _bdate_toyear(self, bdate):
        user_year = bdate.split('.')[2]
        now = datetime.now().year
        return now - int(user_year)


    def get_profile_info(self, user_id):
        
        try:
            info, = self.vkapi.method('users.get',
                                    {'user_id': user_id,
                                    'fields': 'bdate,city,sex,relation'
                                    }
                                    )
        
        except ApiError as e:
            info = {}
            print(f'eror = {e}')


        result = {'name': (info['first_name'] + ' ' + info['last_name']) if 
                  'first_name' in info and 'last_name' in info else None,
                  'sex': info.get('sex') if 'sex' in info else None,
                  'city': info.get('city')['title'] or ['id'] if info.get('city') is not None else None if 'city' in info else None,
                  'bdate':self._bdate_toyear(info.get('bdate') if 'bdate' in info else None)
                  }
        return result
    
    def search_worksheet(self,params,offset):
        try:
            users = self.vkapi.method('users.search',
                                    {'count': 50,
                                     'offset' : offset,
                                     'hometown': params['city'],
                                     'sex' : 1 if params['sex'] == 2 else 2,
                                     'has_photo': True,
                                     'age_from' : params['bdate'] - 3,
                                     'age_to' : params['bdate'] + 3,
                                    }
                                    )
        
        except ApiError as e:
            users = []
            print(f'eror = {e}')  

        result = [{'name': item['first_name'] + ' ' + item['last_name'],
                   'id': item['id']}
                   for item in users['items'] if item['is_closed'] is False ]
                   
        return result

    def get_photos(self, id):
        try:
            photos = self.vkapi.method('photos.get',
                                        {'owner_id':id,
                                        'album_id': 'profile',
                                        'extended': 1 }  )
        except ApiError as e:
            photos = {}
            print(f'eror = {e}')

        result = [{'owner_id': item['owner_id'],
                   'id': item['id'],
                   'likes': item['likes']['count'],
                   'comments': item['comments']['count'],
                   
                   }
                   for item in photos ['items']
                   
                   ]
        result.sort(key=lambda x: x['likes'], reverse=True)
        result.sort(key=lambda x: x['comments'], reverse=True)
       
        return result[:3]


        

if __name__ == '__main__':
    user_id = 26264405
    tools = vkTools(acces_token)
    params = tools.get_profile_info(user_id)
    worksheets = tools.search_worksheet(params,10)
    worksheet = worksheets.pop()
    photos = tools.get_photos(worksheet['id']) 
    
    pprint(photos)
