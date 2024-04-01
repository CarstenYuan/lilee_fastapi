import pymysql
from fastapi import APIRouter, HTTPException


statistic_router = APIRouter()
users_tag = ['Users APIs']

# MySQL Config
config = {
    'user': 'lilee',
    'password': '1qaz@WSX',
    'host': 'localhost',
    'database': 'lilee',
    'port': 3306
}


@statistic_router.post("/addUser", tags=users_tag)
def add_user(name: str, group: str=''):
    try:
        conn = pymysql.connect(**config)
    except pymysql.err.MySQLError as err:
        print(f"Failed to connect: {err}")
        raise HTTPException(status_code=500, detail="Database connection failed.")

    cursor = conn.cursor()

    if group:
        cmd = """
                INSERT INTO `users` (`name`, `group`)
                VALUES (%s, %s)"""
        values = (name, group)
    else:
        cmd = """
                INSERT INTO `users` (`name`)
                VALUES (%s)"""
        values = (name,)

    cursor.execute(cmd, values)
    conn.commit()

    cursor.close()
    conn.close()
    return {"message": "Added user successfully", "username": name, "group_name": group}
