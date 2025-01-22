import sqlite3



async def save_user(teg_id):
    connection = sqlite3.connect('users_data.db')
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO registration (telegram_id) VALUES (?)
    ''', (teg_id,))
    connection.commit()

    connection.close()


def get_users():
    connection = sqlite3.connect('users_data.db')
    cursor = connection.cursor()
    cursor.execute('''
    SELECT telegram_id FROM registration
    ''')
    teg_id = cursor.fetchall()

    connection.close()

    return teg_id


def is_admin(teg_id):
    connection = sqlite3.connect('users_data.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id FROM admin  WHERE telegram_id == ?
        ''', (teg_id,))
    result = cursor.fetchall()

    connection.close()
    return bool(result)


async def save_homework(subject, text, files):
    connection = sqlite3.connect('users_data.db')
    cursor = connection.cursor()
    cursor.execute('''
            UPDATE homework SET text = ? WHERE subject = ?
            ''', (text, subject))
    cursor.execute('''
                UPDATE homework SET file1 = ? WHERE subject = ?
                ''', ('o', subject))
    cursor.execute('''
                    UPDATE homework SET file2 = ? WHERE subject = ?
                    ''', ('o', subject))
    cursor.execute('''
                    UPDATE homework SET file3 = ? WHERE subject = ?
                    ''', ('o', subject))
    connection.commit()

    for i in range(len(files)):
        cursor.execute(f'''
                    UPDATE homework SET file{i + 1} = ? WHERE subject = ?
                    ''', (files[i], subject))
        connection.commit()



    connection.close()


async def get_homework(subject):
    connection = sqlite3.connect('users_data.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT text, file1, file2, file3 FROM homework WHERE subject = ?
        ''', (subject,))
    result = cursor.fetchall()

    connection.close()
    return result[0][0], result[0][1], result[0][2], result[0][3]