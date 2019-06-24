import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

insert_query = "INSERT INTO users VALUES(?, ?, ?)"

user = (1, 'vsinghal', 'infernal')
cursor.execute(insert_query, user)

users = \
    [
        (2, 'namit', 'aneja'),
        (3, 'mayank', 'baggu'),
        (4, 'kkkk', 'yyyy')
    ]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()
