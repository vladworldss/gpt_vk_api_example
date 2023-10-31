import vk_api


def get_user_info(user_id):
    # Авторизация в Вконтакте
    vk_session = vk_api.VkApi('+79123456789', 'mypassword')
    vk_session.auth()

    # Создание экземпляра API
    vk = vk_session.get_api()

    # Получение информации о пользователе
    user_info = vk.users.get(user_ids=user_id, fields='sex,bdate,country,education,online')[0]

    return user_info


def get_friends_info(user_id):
    # Авторизация в Вконтакте
    vk_session = vk_api.VkApi('+79123456789', 'mypassword')
    vk_session.auth()

    # Создание экземпляра API
    vk = vk_session.get_api()

    # Получение списка друзей пользователя
    friends = vk.friends.get(user_id=user_id, fields='sex,bdate,country,education,online')['items']

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

# Пример использования
user_id = '123456789'  # ID пользователя Вконтакте
user_info = get_user_info(user_id)
friends_info = get_friends_info(user_id)

print('Информация о пользователе:')
print('ID: ', user_id)
print('Пол: ', user_info['sex'])
print('Дата рождения: ', user_info['bdate'])
print('Страна: ', user_info['country']['title'])
print('Образование: ', user_info['education']['name'])
print('Активность: ', 'online' if user_info['online'] else 'offline')

print('\nСтатистика друзей:')
print('Возраст:')
for age, count in friends_info['age'].items(): print(age, ': ', count)

print('\nПол:')
for sex, count in friends_info['sex'].items(): print(sex, ': ', count)

print('\nСтрана:')
for country, count in friends_info['country'].items(): print(country, ': ', count)

print('\nОбразование:')
for education, count in friends_info['education'].items(): print(education, ': ', count)

print('\nАктивность:')
for activity, count in friends_info['online'].items():
    print(activity, ': ', count)