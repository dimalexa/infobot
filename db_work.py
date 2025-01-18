import sqlite3


async def save_user(first_name, second_name, number, letter, teg_id):
    connection = sqlite3.connect('users_data.db')
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO registration (first_name, second_name,class_number,class_letter, telegram_id) VALUES (?, ?, ?, ?, ?)
    ''', (first_name, second_name, number, letter, teg_id))
    connection.commit()

    connection.close()


def get_users_by_class(number, letter):
    connection = sqlite3.connect('users_data.db')
    cursor = connection.cursor()
    cursor.execute('''
    SELECT telegram_id FROM registration WHERE class_number == ? AND class_letter == ?
    ''', (number, letter))
    teg_id = cursor.fetchall()

    connection.close()

    return teg_id


def get_class_by_id(teg_id):
    print(teg_id)
    connection = sqlite3.connect('users_data.db')
    cursor = connection.cursor()
    cursor.execute('''
    SELECT class_number, class_letter FROM registration WHERE telegram_id == ?
    ''', (teg_id,))
    result = cursor.fetchall()

    connection.close()

    return result[0][0], result[0][1]


def get_schedule_by_class(number, letter):
    connection = sqlite3.connect('users_data.db')
    cursor = connection.cursor()
    cursor.execute('''
    SELECT schedule FROM schedule WHERE class_number == ? AND class_letter == ?
    ''', (number, letter))
    result = cursor.fetchall()

    connection.close()

    return result[0][0]


async def set_schedule_by_class(number, letter, schedule):
    connection = sqlite3.connect('users_data.db')
    cursor = connection.cursor()
    cursor.execute('''
    UPDATE schedule SET schedule = ?  WHERE class_number == ? AND class_letter == ?
    ''', (schedule, number, letter))
    connection.commit()

    connection.close()


def is_admin(teg_id):
    connection = sqlite3.connect('users_data.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id FROM admin  WHERE telegram_id == ?
        ''', (teg_id,))
    result = cursor.fetchall()

    connection.close()
    return bool(result)
