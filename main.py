import time
from members import get_users
from walls import get_walls
import dataframes as df


def parser(group_list):
    for group in group_list:
        users_df_header = df.users_header()
        posts_df_header = df.posts_header()
        print(f'Группа: {group}')

        try:
            get_users(group, users_df_header)
            time.sleep(2)
        except Exception as ex:
            print(f'{group} - не предвиденная ошибка при работе с подписчиками: {ex}\n')
            continue

        try:
            get_walls(group, posts_df_header)
            time.sleep(2)
        except Exception as ex:
            print(f'{group} - не предвиденная ошибка при сборе постов: {ex}\n')
            continue
        

if __name__ == '__main__':
    # вносим в список интересующие вас группы
    # group_list = ['happython', 'python_forum', 'vk_python', 'pirsipy']
    group_list = ['ldpr']
    parser(group_list)
