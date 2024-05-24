import mysql.connector
from datetime import datetime
mydb = mysql.connector.connect(
	host = "localhost",
	user= "gaitrpi",
	password = "gait123",
	database="gaitdata")
	
print(mydb)

mycursor = mydb.cursor()
bad_char = ['(',')',',',"'"]
mycursor.execute("SELECT * from patient_details where client_id = %s",('2400001',))
entry_num =mycursor.fetchone()
print(entry_num) 
print("Name is "+entry_num[1])

#mycursor.execute("SELECT name from assessment where client_id = '2400002'")
##name =str(mycursor.fetchone()) 
#for i in bad_char:
#	name = name.replace(i,'')
#print(name)
#sql = 'INSERT INTO Test_Table (Id,Name,Age,Email) VALUES (%s,%s,%s,%s)'
#val = ("1","Isa","22","example@gmail.com")
#mycursor.execute(sql,val)
#mydb.commit()
#print(mycursor.rowcount,"record inserted.")
#mycursor.execute("Select * from Test_Table")
#for x in mycursor:
#	print(x)
