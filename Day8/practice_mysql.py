from random import choice

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="employee_db"
)


def create_database(name):
    c = db.cursor()
    c.execute(f"CREATE DATABASE {name}")


def show_database():
    c = db.cursor()
    c.execute("SHOW DATABASES")
    for i in c:
        print(i)


def read_table(name):
    c = db.cursor()
    sql = f"SELECT * FROM {name}"
    c.execute(sql)
    results = c.fetchall()
    for row in results:
        print(row)


def show_tables():
    c = db.cursor()
    c.execute("SHOW TABLES")
    for i in c:
        print(i)


def drop_table(name):
    c = db.cursor()
    c.execute(f"DROP TABLE {name}")


def drop_database(name):
    c = db.cursor()
    c.execute(f"DROP DATABASE {name}")


def update():
    name = input("Enter the Column in which you want to update")
    value = input("Enter the value to update")
    id = input("Enter the id where to Update value")
    if name.casefold() == 'Salary':
        sql = f"UPDATE employee SET {name} = {value} WHERE id ={id}"
    else:
        sql = f"UPDATE employee SET {name} = '{value}' WHERE id ={id}"

    c = db.cursor()
    c.execute(sql)


# drop_table('employee')
create_table = '''CREATE TABLE `employee_db`.`employee` (
    `Id` INT PRIMARY KEY AUTO_INCREMENT,
    `Name` VARCHAR(40) NOT NULL,
    `Department` VARCHAR(45) NOT NULL,
    `Salary` INT NOT NULL
);
'''


def insert_table():
    insert_table = '''INSERT INTO employee(
    `Name`,
    `Department`,
    `Salary`)
    values ('krish','IT',0)
    '''

    c = db.cursor()

    c.execute(insert_table)
    db.commit()
    show_tables()


read_table('employee')


def update():
    name = input("Enter the name of column you want to update")
    value = input('Enter the value you want to update')
    id = input('Enter id of where you want to update')
    c = db.cursor()
    update = "UPDATE employee SET {name} = 115000 WHERE Id = 2"

    c.execute(update)

    db.commit()


read_table('employee')


def run():
    while True:
        print(
            "1).Show table data\n"
            "2).Show Tables in database\n"
            "3).Update Table\n"
            "4)Delete table\n"
            "5)Insert in table \n"
            "6)Create Database\n"
            "7)Exit")
        choice = int(input("Select the operation to perform"))
        if choice == 1:
            read_table('employee')
        if choice == 2:
            show_tables()
        if choice == 3:
            update()
        if choice == 4:
            name = input("Enter the Name of table you want to delete")
            drop_table('employee')
        if choice == 5:
            insert_table()
        if choice == 6:
            name = input("Enter the name of database you want to create")
            create_database(name)
        if choice == 7:
            break
