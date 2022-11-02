from connector import bot
from data.config import  cur, admin_id

print('Я готов считать посты!')

def pluralRusVariant(x):
    lastTwoDigits = x % 100
    tens = lastTwoDigits // 10
    if tens == 1:
        return 2
    ones = lastTwoDigits % 10
    if ones == 1:
        return 0
    if ones >= 2 and ones <= 4:
        return 1
    return 2

def showHours(main_result) :
    suffix = ["пост", "поста", "постов"][pluralRusVariant(main_result)]
    return "{0} {1}".format(main_result, suffix)

def check_post():
    cur.execute("SELECT * FROM Content where sent = 0 AND group_id == 'NotGroup'")
    result = cur.fetchall()
    if result == None:
        print('Одиночных сообщений нет. ищем дальше.')
    single_result = len(result)
    cur.execute("SELECT * FROM Content where sent = 0 AND group_id != 'NotGroup' group by group_id")
    result = cur.fetchall()
    if result == None:
        print('Групп нет. ищем дальше.')
    grp_result = len(result)
    main_result = single_result + grp_result
    suffix = showHours(main_result)    
    return f'В базе {suffix}'