import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="LynBer01",
    
)

my_cursor = mydb.cursor()

#my_cursor.execute("CREATE DATABASE our_users")

my_cursor.execute("SHOW DATABASE")
for db in my_cursor:
    print(db)

