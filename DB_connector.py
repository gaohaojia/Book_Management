import pymysql
import yaml

class Connector():

    # 初始化
    def __init__(self):

        # 读取数据库密钥
        with open('./key.yml', 'r', encoding='utf-8') as f:
            key = yaml.load(f.read(), Loader=yaml.FullLoader)
        self.connect(key['host'], key['port'], key['user'], key['passwd'], key['db'])

    # 连接数据库
    def connect(self, host, port, user, passwd, db):
        try:
            self.connection = pymysql.connect(
                host = host,
                port = port,
                user = user,
                passwd = passwd,
                db = db,
                charset = 'utf8mb4'
            )
            self.cursor = self.connection.cursor()
            self.status = "success"
        except:
            self.status =  "error"

    # select语句
    def run_select(self, sql: str):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return "error"
    
    # insert语句
    def run_insert(self, sql: str) -> bool:
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    # 其他语句
    def run_other(self, sql: str) -> bool:
        try:
            self.cursor.execute(sql)
            return True
        except Exception as e:
            print(e)
            return False

# 初始化数据库连接
connector = Connector()