import mysql.connector
import csv 


#TODO: Talk with dale about the data structure for local storage and how we will handle the data

mydb = mysql.connector.connect(
    host="153.92.15.9",
    user="u274618925_gaitinsight",
    password="GaitInsight!05",
    database="u274618925_GaitData",
    port=3306,
    autocommit=True)

#confirm connection
print(mydb)

#read csv file
data = []
with open('vid4_angles.csv', 'r') as file:
    reader = csv.reader(file)
    #skip one row
    next(reader)
    for row in reader:
        data.append(row)

mycursor = mydb.cursor()
sql = "INSERT INTO test_table (Video_Name, Frame_Number, RKAngle, RHAngle, RAAngle, LKAngle, LHAngle, LAAngle) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

#insert data
mycursor.executemany(sql, data)
mydb.commit()

#confirm data has been inserted
print(mycursor.rowcount, "record inserted.")

mydb.close()

