import sqlite3
from flask import jsonify


def create_database_schema():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = """
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
           id integer unique primary key autoincrement,
           name text,
           emp_id integer
    );
    """
    c.executescript(sql)
    conn.commit()
    conn.close()

    return jsonify({'status': "SUCCESS"})
