# connect to mysql

# https://blog.csdn.net/FlowerMin/article/details/111600414  # install mysql+workbench in ubuntu
import time

import mysql.connector

def connect():
    a = 1
    time_init = time.time()
    state = True
    while state:
        try:
            print("number", a, "epoch")

            mydb = mysql.connector.connect(
                host="127.0.0.1",  # Database host address.
                user="root",  # Database username
                passwd="xxxx",  # Database password
            )
            print("Connect the database.")
            time.sleep(0.5)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            mycursor = mydb.cursor()

            mycursor.execute("CREATE DATABASE runoob_db")  # create database
            print("Create database")
            mycursor.execute("SHOW DATABASES")  # show database
            for x in mycursor:
                print(x)
            time.sleep(0.5)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            mycursor.execute("USE runoob_db")
            mycursor.execute("CREATE TABLE sites (name VARCHAR(255), url VARCHAR(255))")  # create table
            print("Create table.")
            mycursor.execute("SHOW TABLES")  # show table
            for x in mycursor:
                print(x)
            time.sleep(0.5)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            mycursor.execute("ALTER TABLE sites ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")  # 给表添加主键
            print("Add primary key to table.")
            time.sleep(0.5)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            sql = "INSERT INTO sites (name, url) VALUES (%s, %s)"
            val = [("Google", "https://www.google.com"), ("Github", "https://www.github.com"),
                   ("Taobao", "https://www.taobao.com"), ("stackoverflow", "https://www.stackoverflow.com/")]
            for i in range(len(val)):
                mycursor.execute(sql, val[i])  # Batch insert data
            print("Batch insert data.")
            mydb.commit()  # The data table content has been updated; this statement must be used.
            print(len(val), "records have been inserted successfully.")
            time.sleep(0.5)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            mycursor.execute("SELECT * FROM sites")  # Query data.
            print("Query data.")
            myresult = mycursor.fetchall()  # fetchall() Retrieve all records.
            for x in myresult:
                print(x)
            time.sleep(0.5)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            mycursor.execute("SELECT name, url FROM sites")  # Read the data of the specified fields.
            print("Read the data of the specified fields.")
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
            time.sleep(0.5)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            sql = "DELETE FROM sites WHERE name = %s"  # Delete records.
            na = ("stackoverflow",)
            mycursor.execute(sql, na)
            print("Delete records.")
            mycursor.execute("SELECT * FROM sites")  # Query data.
            print("Query the data after deleting records.")
            myresult = mycursor.fetchall()  # fetchall() retrieves all records.
            for x in myresult:
                print(x)
            time.sleep(0.5)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            mycursor.execute("DROP TABLE IF EXISTS sites")  # Delete the data table sites.
            print("Delete the table.")
            time.sleep(0.5)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            mycursor.execute("DROP DATABASE runoob_db")  # Drop database runoob_db.
            print("Drop database.")
            time.sleep(0.5)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            mydb.close()
            print("Disconnect from the database.")
            time.sleep(0.5)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            a = a + 1
            print()

            if time.time() - time_init > 598:
                state = False
                print("over")

        except Exception as e:
            print("error:", e)
            mycursor.execute("DROP DATABASE runoob_db")  # Drop database runoob_db.
            print("Drop database.")
            time.sleep(0.5)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            mydb.close()
            print("Disconnect from the database.")
            time.sleep(0.5)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            state = False



if __name__ == "__main__":
    connect()