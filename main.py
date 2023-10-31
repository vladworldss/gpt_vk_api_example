from client import get_vk_session

from gpt_vk_api_example.secrets import MY_ID


def get_user_info(user_id):
    vk = get_vk_session()
    
    # Получение информации о пользователе
    user_info = vk.users.get(user_ids=user_id, fields='sex,bdate,country,education,online')[0]
    
    return user_info


def get_friends_info(user_id):
    vk = get_vk_session()
    
    # Получение списка друзей пользователя
    friends = vk.friends.get(user_id=user_id, fields='name,sex,bdate,country,education,online')['items']
    
    # Статистика
    stats = {'age': {}, 'sex': {}, 'country': {}, 'education': {}, 'online': {}}
    
    for friend in friends:
        # Подсчет возраста
        if 'bdate' in friend:
            bdate = friend['bdate'].split('.')
            if len(bdate) == 3:
                age = 2022 - int(bdate[2])
                if age in stats['age']:
                    stats['age'][age] += 1
                else:
                    stats['age'][age] = 1
    
        # Подсчет пола
        if 'sex' in friend:
            sex = friend['sex']
            if sex in stats['sex']:
                stats['sex'][sex] += 1
            else:
                stats['sex'][sex] = 1
    
        # Подсчет страны
        if 'country' in friend:
            country = friend['country']['title']
            if country in stats['country']:
                stats['country'][country] += 1
            else:
                stats['country'][country] = 1
    
        # Подсчет образования
        if 'education' in friend:
            education = friend['education']['name']
            if education in stats['education']:
                stats['education'][education] += 1
            else:
                stats['education'][education] = 1
    
        # Подсчет активности
        if 'online' in friend:
            online = friend['online']
            activity = 'online' if online else 'offline'
            if activity in stats['online']:
                stats['online'][activity] += 1
            else:
                stats['online'][activity] = 1
    
    return stats


if __name__ == '__main__':
    res = get_friends_info(MY_ID)
    for k, v in res.items():
        print(k, v)
