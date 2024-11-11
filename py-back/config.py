# 数据库操作类

import pymysql

DB_CONFIG = {
	"host": "127.0.0.1",
	"port": 3306,
	"user": "root",
	"passwd": "123456",
	"db": "test",
	"charset": "utf8"
}

class SQLManager(object):

	# 初始化实例方法
	def __init__(self):
		self.conn = None
		self.cursor = None
		self.connect()

	# 连接数据库
	def connect(self):
		self.conn = pymysql.connect(
			host=DB_CONFIG["host"],
			port=DB_CONFIG["port"],
			user=DB_CONFIG["user"],
			passwd=DB_CONFIG["passwd"],
			db=DB_CONFIG["db"],
			charset=DB_CONFIG["charset"]
		)
		self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

	# 查询多条数据
	def get_list(self, sql, args=None):
		self.cursor.execute(sql, args)
		return self.cursor.fetchall()

	# 查询单条数据
	def get_one(self, sql, args=None):
		self.cursor.execute(sql, args)
		return self.cursor.fetchone()

	# 执行单条SQL语句
	def modify(self, sql, args=None):
		row = self.cursor.execute(sql, args)
		self.conn.commit()
		return row > 0

	# 执行多条SQL语句
	def multi_modify(self, sql, args=None):
		rows = self.cursor.executemany(sql, args)
		self.conn.commit()
		return rows > 0

	# 关闭数据库cursor和连接
	def close(self):
		self.cursor.close()
		self.conn.close()
