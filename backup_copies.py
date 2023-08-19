import os, sqlite3
from datetime import datetime


def get_appdata_folder():
    """
    :return: имя рабочей папки
    """
    appdata_path = os.environ.get('APPDATA')
    if appdata_path:
        appdata_folder = os.path.join(appdata_path, 'LFK-records')
        if not os.path.exists(appdata_folder):
            os.makedirs(appdata_folder)
    else:
        raise Exception("Could not access AppData folder.")
    return appdata_folder


def get_full_path(backup_name):
    """
    :param backup_name:
    :return: полный путь до файла
    """
    return os.path.join(get_appdata_folder(), backup_name)


def check_correct_db(con):
    """
    Выполняет базовую проверку на наличие потерь.

    :param con:
    :return: код ошибки: 0 - нет ошибки 1 - несоответствие records 2 - несоответствие lessons 3 - records и lessons -1 - неизвестная проблема
    """

    x1 = True
    x2 = True

    cur = con.cursor()
    inquiry = f"""SELECT COUNT(*) FROM records"""
    count_1 = cur.execute(inquiry).fetchone()[0]
    inquiry = f"""SELECT id FROM records
    WHERE id >= {count_1 - 30}"""
    count_2 = cur.execute(inquiry).fetchall()
    if max(count_2, key=lambda x: x[0])[0] == count_1:
        x1 = False

    inquiry = f"""SELECT COUNT(*) FROM lessons"""
    count_1 = cur.execute(inquiry).fetchone()[0]
    inquiry = f"""SELECT id FROM lessons
        WHERE id >= {count_1 - 30}"""
    count_2 = cur.execute(inquiry).fetchall()
    if max(count_2, key=lambda x: x[0])[0] == count_1:
        x2 = False

    if not x1 and not x2:
        return 0
    if x1 and not x2:
        return 1
    if not x1 and x2:
        return 2
    if x1 and x2:
        return 3
    return -1


def wright_file(db_name, appdata_folder, backup_files, base_name=''):
    """
    Использовать create_new_backup

    :param db_name: Оригинальная база
    :param appdata_folder: Рабочая попка
    :param backup_files: Список прошлых бэкапов
    :param base_name: Ключевое имя
    :return: путь до новой копии
    """
    with open(db_name, 'rb') as f:
        b = f.read()
    new_name = 1
    for file in backup_files:
        x = int(file.split('_')[0])
        if new_name <= x:
            new_name = x + 1
    current_date = datetime.now()
    if base_name == '':
        new_name = f'{new_name}_{current_date.strftime("%d-%m-%Y")}'
    else:
        new_name = f'{new_name}_{base_name}'
    with open(os.path.join(appdata_folder, new_name), 'wb') as f:
        f.write(b)
    return new_name


def create_new_backup(db_name, base_name=''):
    """
    Автоматически назначает имя для новой копии, создаёт её и удаляет не нужные:
    :param db_name: путь к базе для копирования:
    :param base_name: Ключевое имя:
    :return: путь до новой копии
    """
    appdata_folder = get_appdata_folder()
    backup_files = []
    for file in os.listdir(appdata_folder):
        if os.path.isfile(os.path.join(appdata_folder, file)):
            backup_files.append(file)
    if len(backup_files) < 6:
        return wright_file(db_name, appdata_folder, backup_files, base_name)
    else:
        min_name = min(backup_files, key=lambda x: int(x.split('_')[0]))
        max_name = max(backup_files, key=lambda x: int(x.split('_')[0]))
        current_date = datetime.now()
        if max_name.split('_')[1] == current_date.strftime("%d-%m-%Y"):
            os.remove(os.path.join(appdata_folder, max_name))
        else:
            os.remove(os.path.join(appdata_folder, min_name))

        return wright_file(db_name, appdata_folder, backup_files, base_name)


def get_all_backups():
    """
    :return: Возвращает имена всех созданных копий
    """
    appdata_folder = get_appdata_folder()
    backup_files = []
    for file in os.listdir(appdata_folder):
        if os.path.isfile(os.path.join(appdata_folder, file)):
            backup_files.append(file)
    return backup_files


def get_data_of_backup(backup_name):
    with open(backup_name, 'rb') as f:
        return f.read()


def close_all_windows(main_menu):

    """
    закрывает все ока текущей сессии
    :param main_menu:
    :return:
    """
    try:
        main_menu.admin_window.close()
    except Exception: pass

    try:
        main_menu.adding_window.close()
    except Exception: pass

    try:
        main_menu.dischar_window.close()
    except Exception: pass

    try:
        main_menu.procedure_window.close()
    except Exception: pass

    try:
        main_menu.history_window.close()
    except Exception: pass

    try:
        main_menu.description_window.close()
    except Exception: pass

    try:
        main_menu.report_window.close()
    except Exception: pass


def choose_another_backup(backup_name, main_menu):
    backup_path = os.path.join(get_appdata_folder(), backup_name)

    main_menu.login_in_system.is_backup = True
    main_menu.login_in_system.db_name = backup_path
    close_all_windows(main_menu)
    main_menu.login_in_system.show()
    main_menu.close()


def come_back_from_backup(main_menu):
    with open('options.txt') as file:
        db_name = file.read().split('\n')[0]
    main_menu.login_in_system.is_backup = False
    main_menu.login_in_system.db_name = db_name

    close_all_windows(main_menu)
    main_menu.login_in_system.show()
    main_menu.close()


def recover(backup_name, main_menu):
    backup_path = os.path.join(get_appdata_folder(), backup_name)

    with open('options.txt') as file:
        db_name = file.read().split('\n')[0]
    with open(db_name, 'wb') as f:
        f.write(get_data_of_backup(backup_path))

    main_menu.login_in_system.is_backup = False
    main_menu.login_in_system.db_name = db_name

    close_all_windows(main_menu)
    main_menu.login_in_system.show()
    main_menu.close()


def smart_recovery(db_name, cod):
    # TODO v-1.11.3
    if cod == -1:
        return False
    if cod == 0:
        return True
    if cod == 1:
        con = sqlite3.connect(db_name)
        cur = con.cursor()

        inquiry = f"""SELECT COUNT(*) FROM records"""
        count_1 = cur.execute(inquiry).fetchone()[0]
        inquiry = f"""SELECT id FROM records
            WHERE id >= {count_1 - 30}"""
        count_2 = cur.execute(inquiry).fetchall()



if __name__ == "__main__":
    # con = sqlite3.connect("C:/Users/pavel/Desktop/журнал ЛФК/lfk_work.db")
    print(create_new_backup('C:/Users/pavel/Desktop/журнал ЛФК/lfk_work.db'))

