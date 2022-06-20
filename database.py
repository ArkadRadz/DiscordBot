import sqlite3

addition = '++'
subtraction = '--'

def create_connection():
    con =  sqlite3.connect('discord.db')
    cur = con.cursor()
    cur.execute('create table if not exists karma ( id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, score INTEGER )')
    con.commit()

    return con

def update_user_karma(user, operation):
    con =  create_connection()
    cur = con.cursor()
    cur.execute('select score from karma where user=:user', {'user': user})
    
    result = cur.fetchone()

    if result is None:
        score = handle_karma_operation(operation)
        cur.execute('insert into karma(user, score) values (:user, :score)',  {'user': user, 'score': score})
    else:
        score = handle_karma_operation(operation, result[0])
        cur.execute('update karma set score = :score where user = :user', {'user': user, 'score': score})

    con.commit()
    con.close()

    return score
    
def handle_karma_operation(operation, score = None):

    if score is None:
        score = 0

    if operation == addition:
        return score + 1
    if operation == subtraction:
        return score - 1

    return 0