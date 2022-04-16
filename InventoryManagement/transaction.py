import pandas as pd
from tabulate import tabulate
import mysql.connector as sqlt
import matplotlib.pyplot as plt
con = sqlt.connect(host="localhost", user="root",
                   passwd="root", database="Inventory")
cursor = con.cursor()

##########################################################################################
#####  TRANSACTION MODULE #####


def purchase():
    pid = 0
    total = 0
    grand = 0
    l = []
    ch = 'y'
    q = "select max(pid) as largest from pmaster"
    cursor.execute(q)
    r = cursor.fetchone()[0]
    if r:
        pid = r+1
    else:
        pid = 1
    pdate = input("Enter Purchase date")
    sid = int(input("Enter Supplier ID"))
    cursor.execute("select * from supplier where sid={};".format(sid))
    if cursor.fetchone():
        print("Item Details")
        df = pd.read_sql("select * from item", con)
        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
        while(ch == 'y'):
            ino = int(input("Enter Item No"))
            cursor.execute("select * from item where ino ={};".format(ino))
            r1 = cursor.fetchone()
            if r1:
                qty = int(input("Enter qty"))
                rate = r1[2]
                total = qty*rate
                grand = grand+total
                t = (pid, ino, qty, rate, total)
                l.append(t)
            else:
                print("Item Not Found")
            ch = input("Do you wish to add more Items in bucket y/n")
            q1 = "insert into pmaster values({},'{}',{},{});".format(
                pid, pdate, sid, grand)
            cursor.execute(q1)
            con.commit()
            q2 = "insert into pdetail values(%s,%s,%s,%s,%s);"
            cursor.executemany(q2, l)
            con.commit()
            cursor.executemany("insert into ptemp values(%s,%s,%s,%s,%s);", l)
            con.commit()
            q3 = "update item join ptemp using(ino) set item.qoh = item.qoh+ptemp.qty"
            cursor.execute(q3)
            con.commit()
            cursor.execute("delete from ptemp")
            con.commit()
            print("Item Purchased and Added")
        else:
            print("Supplier Not Found")


def sale():
    saleid = 0
    total = 0
    grand = 0
    l = []
    ch = 'y'
    q = "select max(saleid) as largest from smaster"
    cursor.execute(q)
    r = cursor.fetchone()[0]
    if r:
        saleid = r+1
    else:
        saleid = 1
    sdate = input("Enter Sale date")
    sid = int(input("Enter Supplier ID"))
    cursor.execute("select * from supplier where sid={};".format(sid))
    if cursor.fetchone():
        print("Item Details")
        df = pd.read_sql("select * from item", con)
        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
        while(ch == 'y'):
            ino = int(input("Enter Item No"))
            cursor.execute("select * from item where ino ={};".format(ino))
            r1 = cursor.fetchone()
            if r1:
                qty = int(input("Enter qty"))
                rate = r1[2]
                total = qty*rate
                grand = grand+total
                t = (saleid, ino, qty, rate, total)
                l.append(t)
            else:
                print("Item Not Found")
            ch = input("Do you wish to add more Items in bucket y/n")
        q1 = "insert into smaster values({},'{}',{},{});".format(
            saleid, sdate, sid, grand)
        cursor.execute(q1)
        con.commit()
        q2 = "insert into sdetail values(%s,%s,%s,%s,%s);"
        cursor.executemany(q2, l)
        con.commit()
        cursor.executemany("insert into stemp values(%s,%s,%s,%s,%s);", l)
        con.commit()
        q3 = "update item join stemp using(ino) set item.qoh = item.qoh-stemp.qty"
        cursor.execute(q3)
        con.commit()
        cursor.execute("delete from stemp")
        con.commit()
        print("Item Purchased and Added")
    else:
        print("Supplier Not Found")