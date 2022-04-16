import pandas as pd
from tabulate import tabulate
import mysql.connector as sqlt
import matplotlib.pyplot as plt
con = sqlt.connect(host="localhost", user="root",
                   passwd="root", database="Inventory")
cursor = con.cursor()

########################################################################################################################

############## CUSTOMER MODULE ##############
def add_customer():
    cid = int(input("Enter Customer ID"))
    cname = input("Enter Customer Name")
    cadd = input("Enter Address")
    mobile = input("Enter Mobile")
    q = "insert into customer values({},'{}','{}','{}');".format(
        cid, cname, cadd, mobile)
    cursor.execute(q)
    con.commit()
    print("Customer Added")


def edit_customer():
    cid = int(input("Enter Customer ID"))
    q = "select * from Customer where cid = {};".format(cid)
    cursor.execute(q)
    if cursor.fetchone():
        cadd = input("Enter Customer Address")
        cursor.execute(
            "update customer set cadd = '{}' where cid={};".format(cadd, cid))
        con.commit()
        print("Customer Edited")
    else:
        print("Customer Not Found")


def search_customer():
    cname = input("Enter Customer Name")
    q = "select * from customer where cname like '%{}%';".format(cname)
    cursor.execute(q)
    if cursor.fetchall():
        df = pd.read_sql(q, con)
        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
    else:
        print("Customer Not found")


def delete_customer():
    cid = int(input("Enter Customer ID"))
    q = "select * from customer where cid = {};".format(cid)
    cursor.execute(q)
    if cursor.fetchone():
        cursor.execute("delete from customer where cid={};".format(cid))
        con.commit()
        print("customer deleted")
    else:
        print("customer Not Found")


        