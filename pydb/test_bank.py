import pymysql
import sys
		
class TransferMoney(object):
	def __init__(self, arg):
		self.conn = conn

	def check_acc_available(self,accid):
		cursor = self.conn.cursor()
		try:
			sql = 'select * from account where accid=%s' % accid
			cursor.execute(sql)
			print ('check_acc_available:' + sql)
			rs = cursor.fetchall()
			if len(rs) != 1:
				raise Exception('账号不存在' % accid)
		finally:
			cursor.close()

	def has_enough_money(self,accid,money):
		cursor = self.conn.cursor()
		try:
			sql = 'select * from account where accid=%s and money>%s' % (accid,money)
			cursor.execute(sql)
			print ('has_enough_money:' + sql)
			rs = cursor.fetchall()
			if len(rs) != 1:
				raise Exception('账号%s金额不足' % accid)
		finally:
			cursor.close()

	def reduce_money(self,accid,money):
		cursor = self.conn.cursor()
		try:
			sql = 'update account set money=money-%s where accid=%s' % (money,accid)
			cursor.execute(sql)
			print ('reduce_money:' + sql)
			if cursor.rowcount != 1:
				raise Exception('账号%s减款失败' % accid)
		finally:
			cursor.close()

	def add_money(self,accid,money):
		cursor = self.conn.cursor()
		try:
			sql = 'update account set money=money+%s where accid=%s' % (money,accid)
			cursor.execute(sql)
			print ('add_money:' + sql)
			if cursor.rowcount != 1:
				raise Exception('账号%s减款失败' % accid)
		finally:
			cursor.close()		

	def transfer(self,source_accid,target_accid,money):
		try:
			self.check_acc_available(source_accid)
			self.check_acc_available(target_accid)
			self.has_enough_money(source_accid,money)
			self.reduce_money(source_accid,money)
			self.add_money(target_accid,money)
			self.conn.commit()
		except Exception as e:
			self.conn.rowcount()
			raise e


if __name__ == '__main__':
	source_accid = sys.argv[1]
	target_accid = sys.argv[2]
	money = sys.argv[3]
	# 建立一个connection
	conn = pymysql.Connect(
		host = '127.0.0.1',
		port = 3306,
		user = 'root',
		passwd = '12125772',
		db = 'imooc',
		charset = 'utf8'
		)
	tr_money = TransferMoney(conn)

	try:
		tr_money.transfer(source_accid,target_accid,money)
	except Exception as e:
		print ('出现问题：' + str(e))
	finally:
		conn.close() 


