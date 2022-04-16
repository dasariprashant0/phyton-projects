import pandas as pd
from tabulate import tabulate
import mysql.connector as sqlt
import matplotlib.pyplot as plt
con = sqlt.connect(host="localhost", user="root",
                   passwd="root", database="Inventory")
cursor = con.cursor()
############################################################################################

############# SUPPILER MODULE ###################
def add_supplier():
    sid = int(input("Enter Supplier ID"))
    sname = input("Enter Supplier Name")
    sadd = input("Enter Address")
    mobile = input("Enter Mobile")
    q = "insert into supplier values({},'{}','{}','{}');".format(sid, sname, sadd, mobile)
    cursor.execute(q)
    con.commit()
    print("Supplier Added")


def edit_supplier():
    sid = int(input("Enter Supplier ID"))
    q = "select * from supplier where sid = {};".format(sid)
    cursor.execute(q)
    if cursor.fetchone():
        sadd = input("Enter Supplier Address")
        cursor.execute(
            "update supplier set sadd = '{}' where sid={};".format(sadd, sid))
        con.commit()
        print("Supplier Edited")
    else:
        print("Supplier Not Found")


def search_supplier():
    sid = int(input("Enter Supplier ID"))
    q = "select * from supplier where sid = {};".format(sid)
    cursor.execute(q)
    if cursor.fetchone():
        df = pd.read_sql(q, con)
        print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    else:
        print("Supplier Not Found")

def delete_supplier():
    sid = int(input("Enter Supplier ID"))
    q = "select * from supplier where sid = {};".format(sid)
    cursor.execute(q)
    if cursor.fetchone():
        cursor.execute("delete from Supplier where sid={};".format(sid))
        con.commit()
        print("Supplier deleted")
    else:
        print("Supplier Not Found")