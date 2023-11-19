import sqlite3

conn = sqlite3.connect('Cal.db')
cur = conn.cursor()
cur.execute('''create table if not exists users (
            uid text primary key, 
            password text, 
            name text,
            age text,
            height text,
            gender text)''')

cur.execute('''create table if not exists exercise (
            e_id text primary key,
            e_name text,
            uid text,
            duration text,
            date text,
            bpm text,
            temperature text,
            calories text)''')

conn.commit()
conn.close()