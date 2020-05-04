import pymysql


class JianshuPipeline(object):
    def __init__(self):
        # 数据库的参数
        db_params = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'nitaoge',
            'database': 'testdatabase',
            'charset': 'utf8'
        }

        # 连接数据库
        self.conn = pymysql.connect(**db_params)

        # 数据库的游标对象
        self.cursor = self.conn.cursor()

        # 数据库语句
        self._sql = """
            insert into jianshu(title, author, content) values(%s, %s, %s)
            """

    def process_item(self, item, spider):
        # 执行sql语句
        self.cursor.execute(self._sql, (item['title'], item['author'], item['content']))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # 关闭游标
        self.cursor.close()

