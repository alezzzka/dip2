from app import (search_people_and_photos,
                 cur_user)

from functions import (event_listen,
                       write_msg,
                       prepare_photo)

from db import connection, WorkingDB
from messages import *


WorkingDB(connection).create_all_tables()

favorites = 1
black_list = 1

while True:
    message, user_id = event_listen()
    sex, city, dict_cur_user = cur_user(user_id=user_id)
    WorkingDB(connection).add_users(dictinary=dict_cur_user)
    age_at = 29
    age_to = 33
    status = 6
    dict_favorites = WorkingDB(connection).select_favorites(user_id=user_id)
    dict_blacklist = WorkingDB(connection).select_blacklist(user_id=user_id)

    if message == "начать":
        write_msg(user_id=user_id,
                  message=start_message.replace('{name}', dict_cur_user[user_id]['first_name']))

    elif message == "поиск":
        dict_all_persons = search_people_and_photos(sex=sex,
                                                    age_at=age_at,
                                                    age_to=age_to,
                                                    city=city,
                                                    status=status)
        WorkingDB(connection).add_users_and_search_params(dictionary=dict_all_persons,
                                                          sex=sex,
                                                          age_at=age_at,
                                                          age_to=age_to,
                                                          city=city,
                                                          status=status)
        write_msg(user_id=user_id,
                  message=message_view.replace('{name}', dict_cur_user[user_id]['first_name']))

    elif message == "смотреть":
        dict_for_view = WorkingDB(connection).select_search_params(sex=sex,
                                                                   age_at=age_at,
                                                                   age_to=age_to,
                                                                   city=city,
                                                                   status=status)

        if dict_for_view == {}:
            write_msg(user_id=user_id,
                      message=message_not_new)
        else:
            dict_one_persons = WorkingDB(connection).select_one_user_for_view(bd_id=dict_for_view[1])
            text, photo = prepare_photo(dict_one_persons)
            write_msg(user_id=user_id,
                      message=text,
                      attachment=photo)
            write_msg(user_id=user_id,
                      message=message_info)
            id_in_list = dict_one_persons['id']

    elif message == "добавить в избранное":
        WorkingDB(connection).add_favorites_users(user_id=user_id,
                                                  id_in_list=id_in_list)
        write_msg(user_id=user_id,
                  message=message_continue_view.replace('{name}',
                                                        dict_cur_user[user_id]['first_name']))

    elif message == "добавить в черный список":
        WorkingDB(connection).add_black_list(user_id=user_id,
                                             id_in_list=id_in_list)
        write_msg(user_id=user_id,
                  message=message_continue_view.replace('{name}',
                                                        dict_cur_user[user_id]['first_name']))

    elif message == "показать избранные анкеты":
        if dict_favorites == {}:
            write_msg(user_id=user_id,
                      message=message_no_favorite)
        else:
            if favorites not in dict_favorites.keys():
                write_msg(user_id=user_id,
                          message=message_end_favorite)
            else:
                text, photo = prepare_photo(dict_all_persons=dict_favorites[favorites])
                write_msg(user_id=user_id,
                          message=text,
                          attachment=photo)
                favorites += 1

    elif message == "с начала списка избранных":
        favorites = 1
        write_msg(user_id=user_id,
                  message=message_for_view_favorite)

    elif message == "показать черный список":
        if dict_blacklist == {}:
            write_msg(user_id=user_id,
                      message=message_no_black)
        else:
            if black_list not in dict_blacklist.keys():
                write_msg(user_id=user_id,
                          message=message_black_end)
            else:
                text, photo = prepare_photo(dict_all_persons=dict_blacklist[black_list])
                write_msg(user_id=user_id,
                          message=text,
                          attachment=photo)
                black_list += 1

    elif message == "с начала черного списка":
        black_list = 1
        write_msg(user_id=user_id,
                  message=message_view_black)

    elif message == "пока":
        write_msg(user_id=user_id,
                  message=message_goodbye)

    else:
        write_msg(user_id=user_id,
                  message=message_not_understand)
