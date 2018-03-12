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
    except Exception as e:
        conn.rollback()
        funcset.output("Execution is failed: " + sql)
        funcset.log(e)
    finally:
        cur.close()
        conn.close()


def insert_stock(stock_dict):
    conn = opendb()
    cur = conn.cursor()
    sql = ""
    try:
        sql = "INSERT INTO stock VALUES (?,?)"
        for k, v in stock_dict.items():
            cur.execute(sql, (k, v))
        conn.commit()
    except Exception as e:
        conn.rollback()
        funcset.output("Execution is failed: " + sql + " with stock_dict")
        funcset.log(e)
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
    except Exception as e:
        conn.rollback()
        funcset.output("Execution is failed: " + sql)
        funcset.log(e)
    finally:
        cur.close()
        conn.close()
    return stock_list


def insert_org(orgname):
    conn = opendb()
    cur = conn.cursor()
    sql = ""
    print(orgname)
    try:
        sql = "INSERT INTO ORG(ORGNAME) VALUES (?)"
        cur.execute(sql, (orgname,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        funcset.output("Execution is failed: " + sql + " with (" + orgname + ")")
        funcset.log(e)
    finally:
        cur.close()
        conn.close()


def get_org():
    org_list = {}
    conn = opendb()
    cur = conn.cursor()
    sql = ""
    try:
        sql = "SELECT ORGID, ORGNAME FROM ORG"
        results = cur.execute(sql)
        all = results.fetchall()
        for r in all:
            org_list[r[0]] = r[1]
        conn.commit()
    except Exception as e:
        conn.rollback()
        funcset.output("Execution is failed: " + sql)
        funcset.log(e)
    finally:
        cur.close()
        conn.close()
    return org_list


def get_orgid(org_name):
    conn = opendb()
    cur = conn.cursor()
    sql = ""
    orgid = 0
    orgid_arr = ()
    try:
        sql = "SELECT ORGID FROM ORG WHERE ORGNAME=?"
        results = cur.execute(sql, (org_name,))
        orgid_arr = results.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        funcset.output("Execution is failed: " + sql)
        funcset.log(e)
    finally:
        cur.close()
        conn.close()
    if len(orgid_arr) > 0:
        orgid = orgid_arr[0]
    return orgid


def insert_stock_rec(stock_records_dict):
    conn = opendb()
    cur = conn.cursor()
    sql = ""
    try:
        sql = "INSERT INTO RECORDS VALUES (?,?,?,?,?,?)"
        for date, sr in stock_records_dict.items():
            cur.execute(sql, (
                date, sr.get_stocknum(), sr.get_organization(), sr.get_reason(), sr.get_reason_file(), sr.get_from()))
        conn.commit()
    except Exception as e:
        conn.rollback()
        funcset.output("Execution is failed: " + sql)
        funcset.log(e)
    finally:
        cur.close()
        conn.close()
