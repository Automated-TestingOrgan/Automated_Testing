import time
import random
import pymysql
from interfaceTest.log_and_logresult_package import Log
from interfaceTest.config_package import readConfig as rc

class DateBaseHandle(object):

    def __init__(self):

        self.conn = None
        self.logger = Log.logger
        self.sid = []
        self.name = []
        self.list_mysql_sid = []
        self.list_mysql_name = []
        self.num = None
        self.key = None
        self.list = []

    def conn_timeout(self):
        conn_status = True
        max_count = 10  # 设置最大重试次数
        conn_count = 0  # 初始重试次数
        conn_timeout = 3  # 连接超时时间为3秒
        while conn_status and conn_count <= max_count:
            try:
                self.conn = pymysql.connect(host=rc.ret.get_mysql("host"),
                                        port=int(rc.ret.get_mysql("port")),
                                        user=rc.ret.get_mysql("user"),
                                        password=rc.ret.get_mysql("password"),
                                        db=rc.ret.get_mysql("db"),
                                        charset=rc.ret.get_mysql("charset"),
                                        connect_timeout=conn_timeout)
                conn_status = False
                return self.conn

            except:

                conn_count += 1
                print(conn_count)
            time.sleep(3)
            continue

    def select_mysql(self, sql):

        self.conn_timeout()
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            for rows, table in data:
                self.sid.append(rows)
                self.name.append(table)
                self.list_mysql_sid.append(self.sid)
                self.list_mysql_name.append(self.name)
            for topic in self.list_mysql_sid:
                self.num = random.choice(topic)
            for topics in self.list_mysql_name:
                self.key = random.choice(topics)
            self.list.append(self.num)
            self.list.append(self.key)
            return self.list
        except:
            self.logger.error("select date error")
        finally:
            cursor.close()
    def delete_mysql(self, sql):

        self.conn_timeout()
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
        except:
            self.logger.info("···数据库删除数据错误，回滚中···")
            self.conn.rollback()
            self.logger.info("···数据回滚成功···")
        finally:
            cursor.close()

# "select name,mobile FROM axd_user WHERE id=1541682410768827427"
results = DateBaseHandle()