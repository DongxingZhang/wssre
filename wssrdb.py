import sqlite3

import const
import funcset


def opendb():
    return sqlite3.connect(const.WSSRDB)


def cleanup_stock():
    conn = opendb()
    cur = conn.cursor()
    sql = ""
    try:
        sql = "DELETE FROM stock"
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
        funcset.output("Execution is failed: " + sql)
    finally:
        cur.close()
        conn.close()


def insert_stock(stock):
    conn = opendb()
    cur = conn.cursor()
    sql = ""
    try:
        sql = "INSERT INTO stock VALUES (?,?)"
        cur.execute(sql, (stock[0], stock[1]))
        conn.commit()
    except:
        conn.rollback()
        funcset.output("Execution is failed: " + sql + " with (" + stock[0] + " " + stock[1] + ")")
    finally:
        cur.close()
        conn.close()


def get_stock():
    stock_list = {}
    conn = opendb()
    cur = conn.cursor()
    sql = ""
    try:
        sql = "SELECT STOCKID, STOCKNAME FROM STOCK WHERE SUBSTR(STOCKID, 1, 2) IN ('00', '60', '30')"
        results = cur.execute(sql)
        all = results.fetchall()
        for r in all:
            stock_list[r[0]] = r[1]
        conn.commit()
    except:
        conn.rollback()
        funcset.output("Execution is failed: " + sql)
    finally:
        cur.close()
        conn.close()
    return stock_list
