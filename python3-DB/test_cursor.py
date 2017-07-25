import pymysql

# 建立一个connection
conn = pymysql.Connect(
	host = '127.0.0.1',
	port = 3306,
	user = 'root',
	passwd = '12125772',
	db = 'imooc',
	charset = 'utf8'
	)

# 创建cursor
cursor = conn.cursor()

# 执行sql语句
sql_select = 'select * from user'
sql_insert = 'insert into user (userid, username) values(11, "name11")'
sql_update = 'update user set username="name91" where userid=9'
sql_delete = 'delete from user where userid<3'

try:
	cursor.execute(sql_select)
	print (cursor.rowcount)
	cursor.execute(sql_insert)
	print (cursor.rowcount)
	cursor.execute(sql_update)
	print (cursor.rowcount)
	cursor.execute(sql_delete)
	print (cursor.rowcount)

	# 提交修改的数据到数据库中
	conn.commit()
except Exception as e:
	print (e)
	# 出现异常返回原数据
	conn.rollback()

# rs = cursor.fetchone()
# print (rs)
# rs = cursor.fetchmany(3)
# print (rs)
# rs = cursor.fetchall()
# print (rs)

# print (cursor.rowcount)

cursor.close()
conn.close()
