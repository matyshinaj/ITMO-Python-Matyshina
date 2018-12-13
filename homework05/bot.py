import requests
import config
import telebot
from bs4 import BeautifulSoup
import datetime

bot = telebot.TeleBot(config.access_token)


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    print(url)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_day(web_page, day_number):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на день
    schedule_table = soup.find("table", attrs={"id": day_number + "day"})

    if schedule_table is None:
        return None
    else:
        # Время проведения занятий
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]

        # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text + ", №:" + room.dd.text for room in locations_list]

        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.replace('\n', '') for lesson in lessons_list]
        lessons_list = ['\n'.join([info for info in lesson_info if info]).replace("\t", "").replace("\n", "") for
                        lesson_info in lessons_list]

        return [times_list, locations_list, lessons_list]


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    param = message.text.split()
    if len(param) == 3:
        day, group, week = param
    else:
        day, group = param
        week = ''
    web_page = get_page(group, week)
    if day == "/monday":
        day_number = "1"
    elif day == "/tuesday":
        day_number = "2"
    elif day == "/wednesday":
        day_number = "3"
    elif day == "/thursday":
        day_number = "4"
    elif day == "/friday":
        day_number = "5"
    elif day == "/saturday":
        day_number = "6"
    elif day == "/sunday":
        day_number = "7"

    if parse_schedule_for_a_day(web_page, day_number) is None:
        bot.send_message(message.chat.id, "You have no lessons on this day")
    else:
        times_lst, locations_lst, lessons_lst = parse_schedule_for_a_day(web_page, day_number)
        resp = ''
        for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}'.format(time, location, lesson) + '\n'

        bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    try:
        day, group = message.text.split()
        week_number = datetime.date.today().isocalendar()[1]
        if week_number % 2 == 1:
            week_number = "2"
        else:
            week_number = "1"
        time = datetime.datetime.now().time()
        time_list = str(time).split(":")
        time = float(time_list[0] + "." + time_list[1])
        day_number = datetime.datetime.isoweekday(datetime.datetime.today())
        web_page = get_page(group, week_number)
        day_pass = False
        resp = ''
        find = False
        while True:
            lists = parse_schedule_for_a_day(web_page, str(day_number))
            if lists is None:
                day_pass = True
                day_number += 1
                if day_number > 7:
                    day_number = 1
                    if week_number == 2:
                        week_number = 1
                    else:
                        week_number = 2
                    web_page = get_page(group, str(week_number))
                continue
            times = lists[0]
            if day_pass:
                resp += '<b>{}</b>, {}, {}\n'.format(lists[0][0], lists[1][0], lists[2][0])
                break
            i = -1
            for lessons in times:
                i += 1
                lessons = float(str(lessons).split("-")[0].replace(":", "."))
                if time < lessons:
                    resp += '<b>{}</b>, {}, {}\n'.format(lists[0][i], lists[1][i], lists[2][i])
                    find = True
                elif i == len(times) - 1:
                    day_pass = True
                    day_number += 1
                    if day_number > 7:
                        day_number = 1
                        if week_number == 2:
                            week_number = 1
                        else:
                            week_number = 2
                        web_page = get_page(group, str(week_number))
                    continue

            if find:
                break

        bot.send_message(message.chat.id, resp, parse_mode='HTML')

    except ValueError:
        bot.send_message(message.chat.id, "Incorrect request", parse_mode='HTML')


@bot.message_handler(commands=['tomorrow'])
def get_tomorrow(message):
    """ Получить расписание на следующий день """
    group = message.text.split()[1]
    day = datetime.datetime.weekday(datetime.datetime.today()) + 2
    week = datetime.date.today().isocalendar()[1]
    if day >= 6:
        day = 1
        week += 1
    if week % 2 == 0:
        week = 1
    else:
        week = 2
    day_number = str(day)
    web_page = get_page(group, week)
    if parse_schedule_for_a_day(web_page, day_number) is None:
        bot.send_message(message.chat.id, "NO lessons tomorrow")
    else:
        times_lst, locations_lst, lessons_lst = parse_schedule_for_a_day(web_page, day_number)
        resp = ''
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    all_les = ''
    param = message.text.split()
    if len(param) == 3:
        _, group, week = param
    else:
        _, group = param
        week = ''
    days = {
        '1': 'Понедельник: ',
        '2': 'Вторник: ',
        '3': 'Среда: ',
        '4': 'Четверг: ',
        '5': 'Пятница: ',
        '6': 'Суббота: ',
        '7': 'Воскресенье'}
    for day_number in range(1, 8):
        if parse_schedule_for_a_day(get_page(group, week), str(day_number)) is None:
            all_les += days[str(day_number)] + '\n' + 'нет пар' + '\n' + '\n'
        else:
            times_lst, locations_lst, lessons_lst = parse_schedule_for_a_day(get_page(group, week), str(day_number))
            resp = ''
            for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}'.format(time, location, lesson)
            all_les += days[str(day_number)] + '\n' + resp + '\n\n'

    bot.send_message(message.chat.id, all_les, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
