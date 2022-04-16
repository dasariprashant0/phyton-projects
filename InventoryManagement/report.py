import pandas as pd
from tabulate import tabulate
import mysql.connector as sqlt
import matplotlib.pyplot as plt
con = sqlt.connect(host="localhost", user="root",
                   passwd="root", database="Inventory")
cursor = con.cursor()

##############################################################################################################

############## REPORT MODULE ###########################


def show_item():
    df = pd.read_sql("select * from item", con)
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))


def show_customer():
    df = pd.read_sql("select * from customer", con)
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))


def show_supplier():
    df = pd.read_sql("select * from supplier", con)
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))


def show_sale():
    bdate = input("enter beginning date")
    edate = input("enter end date")
    df = pd.read_sql(
        "select * from smaster where sdate between '{}' and '{}';".format(bdate, edate), con)
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))


def show_purchase():
    bdate = input("enter beginning date")
    edate = input("enter end date")
    df = pd.read_sql(
        "select * from pmaster where pdate between '{}' and '{}';".format(bdate, edate), con)
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))


def best_product():
    s = input("Enter Start date")
    e = input("Enter End Date")
    q = "select s2.ino,sum(s2.qty) as total from smaster s1,sdetail s2 \
        where s1.saleid = s2.saleid and s1.sdate between '{}' and '{}'\
        group by s2.ino;".format(s, e)
    df = pd.read_sql(q, con)
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
    plt.bar(df.ino, df.total)
    plt.xlabel("Item Code")
    plt.ylabel("Qty")
    plt.title("Best Selling Product")
    plt.xticks(df.ino)
    plt.show()


def sale_performance():
    y = input("Enter Year")
    q = "select month(sdate) as month,sum(total)\ as total from smaster where year(sdate) = '{}'\
         and group by month(sdate);".format(y)
    df = pd.read_sql(q, con)
    plt.plot(df.month, df.total)
    plt.xlabel("Month")
    plt.ylabel("Total Sale")
    plt.xticks(df.month)
    plt.show()
