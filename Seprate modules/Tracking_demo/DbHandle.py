import mysql.connector
from datetime import datetime
import time
class DB_Handle:
	def __init__(self):
		self.db = self.DB_Connect()

	def DB_Connect(self):
		mydb = mysql.connector.connect(	host="192.168.0.106",port=8080,
											user="SIH",
											password="SIH2020",
											database="SIH2020"
											)
		print("[ DATA BASE ]",mydb)
		return mydb

	def LogDB(self,records):
		Visitors = []
		NonVisitors = []
		for record in records:
			ret = self.Check_Vehicle_Exist(record[1])
			if not ret[0]:
				Visitors.append(record)
			else:
				NonVisitors.append(record)
		print('[   VISITOR   ] ',Visitors)
		print('[ NON VISITOR ] ',NonVisitors)

		self.Log_Non_Visitor(NonVisitors)
		self.Log_Visitor(Visitors)

	def Check_Vehicle_Exist(self,plate):
		query = ("SELECT NO_PLATE ,USER_ID, VEHICLE_TYPE FROM vehicles "
				"WHERE NO_PLATE = %s;")
		cursor = self.db.cursor()
		cursor.execute(query,(plate,))
		ret_lis = tuple()
		for (NO_PLATE, USER_ID, VEHICLE_TYPE) in cursor:
			ret_lis = (NO_PLATE, USER_ID, VEHICLE_TYPE)
		cursor.close()

		if len(ret_lis)> 0:
			return (True,ret_lis)
		else:
			return (False,)

	def Log_Non_Visitor(self,records_to_insert):
		query = ("INSERT INTO nonvisitors (TIMESTAMP , NO_PLATE , DIRECTION) VALUES (%s, %s, %s)" )
		cursor = self.db.cursor()
		cursor.executemany(query,records_to_insert)
		cursor.close()
		self.db.commit()
		print('[ NON VISITOR LOGGED ] ')


	def Log_Visitor(self,records_to_insert):
		query = ("INSERT INTO visitors (TIMESTAMP , NO_PLATE , DIRECTION) VALUES (%s, %s, %s)" )
		cursor = self.db.cursor()
		cursor.executemany(query,records_to_insert)
		cursor.close()
		# print('[DIR]',Dir)
		for visitor in records_to_insert:
			if visitor[2] == 'IN':
				self.Log_Current_Visitors_INSERT(visitor[1],visitor[0])
			elif visitor[2] == 'OUT':
				self.Log_Current_Visitors_DELETE(visitor[1])
			else:
				print("Something Is Wrong")
				raise Exception
		self.db.commit()
		print('[ VISITOR LOGGED ] ')



	def Log_Current_Visitors_INSERT(self,plate,Ts):
		query = ("INSERT INTO currentvisitors ( NO_PLATE , IN_TIME )VALUES ( %s , %s )" )
		args = (plate,Ts)
		cursor = self.db.cursor()
		ret = cursor.execute(query,args)
		# print('[ INS_C_VIS ]' , ret)
		cursor.close()

	def Log_Current_Visitors_DELETE(self,plate):
		query = ("DELETE FROM currentvisitors WHERE NO_PLATE = %s" )
		args = (plate,)
		cursor = self.db.cursor()
		ret = cursor.execute(query,args)
		# print('[ DEL_C_VIS ]' , ret)
		cursor.close()

	def All_Current_Visitors(self):
		query = ("SELECT * FROM currentvisitors ")
		cursor = self.db.cursor()
		cursor.execute(query)
		ret_lis = []
		for visitor in cursor:
			tmp = []
			for i in visitor:
				tmp.append(i)
			ret_lis.append(tmp)
		cursor.close()
		return ret_lis
		#[(no,ts)()]
	def List_Visitor(self, N):
		query = """SELECT * FROM (
    				SELECT * FROM currentvisitors ORDER BY id DESC LIMIT %s
					) sub ORDER BY id ASC"""

		cursor = self.db.cursor()
		cursor.execute(query,(N,))
		ret_lis = [ ]
		for visitor in cursor:
			tmp = [ ]
			for i in visitor:
				# print(i)
				tmp.append(i)
			ret_lis.append(tmp)
		cursor.close()
		return ret_lis

if __name__ == "__main__":
	# timestamp = int(time.time())
	# dt_object = datetime.fromtimestamp(timestamp)
	# Ts = str(dt_object)
	# print(Ts)
	records_to_insert =[('2020-07-29 12:24:26' , "UP16AF5100" , "OUT"),
						('2020-07-29 12:25:66' , "DL16BZ3160" , "OUT"),
						('2020-07-29 12:26:16' , "DL16BZ3180" , "OUT")]

	Db_H = DB_Handle()
	print(Db_H.List_Visitor(5))

	# UserStatus = Db_H.Check_Vehicle_Exist(plate)

	# if UserStatus[0]:
	# 	Db_H.Log_Non_Visitor(Ts,plate,Dir)
	# else:
	# 	Db_H.Log_Visitor(Ts,plate,Dir)
	# Db_H.All_Current_Visitors()








