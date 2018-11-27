import datetime as datetime
from statistics import median
from typing import Optional
from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    dates = []
    new_dates = []
    date = get_friends(user_id, 'bdate')
    for i in date['response']['items']:
        if i.get('bdate'):
            dates.append(i['bdate'])

    for k in dates:
        if len(k) in range(8, 11):
            new_dates.append(k)
    dates = new_dates

    grade = []
    for k in dates:
        s = list(map(int, k.split('.')))
        age = (datetime.date.today() - datetime.date(s[2], s[1], s[0])) / 365.25
        grade.append(age.days)
    average = 0

    m = 0
    for k in range(len(grade)):
        average += int(grade[k])
        m += 1
    average /= m
    return round(average)

