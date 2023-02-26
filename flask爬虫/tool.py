import pymysql
def get_conn():
    conn = pymysql.connect(host='127.0.0.1', port=3306,
                           user='root', password='root',
                           database='cov', charset='utf8')
    cursor=conn.cursor()
    return conn,cursor
def close(conn,cursor):
    conn.close()
    cursor.close()
