import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',      # 数据库主机地址
            user='root',           # 数据库用户名
            password='123456',     # 数据库密码
            database='cookie_pool' # 数据库名称
        )
        if connection.is_connected():
            print("成功连接到数据库")
            return connection
    except Error as e:
        print(f"连接数据库时出错: {e}")
        return None

def insert_cookie(connection, account_id, cookie_name, cookie_value, expire_time=None):
    try:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO cookies (account_id, cookie_name, cookie_value, expire_time)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (account_id, cookie_name, cookie_value, expire_time))
        connection.commit()
        print("Cookie插入成功")
    except Error as e:
        print(f"插入cookie时出错: {e}")

def fetch_cookies(connection, account_id):
    try:
        cursor = connection.cursor()
        select_query = "SELECT cookie_name, cookie_value FROM cookies WHERE account_id = %s AND is_available = TRUE"
        cursor.execute(select_query, (account_id,))
        cookies = cursor.fetchall()
        return {row[0]: row[1] for row in cookies}
    except Error as e:
        print(f"查询cookie时出错: {e}")
        return None

# 使用示例
connection = connect_to_database()
# if connection:
# #     # 插入一个cookie
# #     insert_cookie(connection, 'account_group_1', 'RT', 'z=1&dm=baidu.com...', '2025-12-31 23:59:59')
    
#     # 查询某个account_id的cookie
#     cookies = fetch_cookies(connection, 'cookie_fkc')
#     if cookies:
#         print("获取到的cookie:", cookies)
    
#     # 关闭连接
#     connection.close()