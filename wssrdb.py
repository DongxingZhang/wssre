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
        funcset.log("Execution is failed: " + sql)
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
        funcset.log("Execution is failed: " + sql + " with stock_dict")
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
        funcset.log("Execution is failed: " + sql)
        funcset.log(e)
    finally:
        cur.close()
        conn.close()
    return stock_list


def insert_org(orgname):
    conn = opendb()
    cur = conn.cursor()
    sql = ""
    try:
        sql = "INSERT INTO ORG(ORGNAME) VALUES (?)"
        cur.execute(sql, (orgname,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        funcset.log("Execution is failed: " + sql + " with (" + orgname + ")")
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
        funcset.log("Execution is failed: " + sql)
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
        funcset.log("Execution is failed: " + sql)
        funcset.log(e)
    finally:
        cur.close()
        conn.close()
    if len(orgid_arr) > 0:
        orgid = orgid_arr[0]
    return orgid


def insert_stock_records(stock_records_list):
    for sr in stock_records_list:
        conn = opendb()
        cur = conn.cursor()
        sql = ""
        try:
            sql = "INSERT INTO RECORDS VALUES (?,?,?,?,?,?)"
            cur.execute(sql, (
                sr.get_date(), sr.get_stockid(), sr.get_orgid(), sr.get_reason(), sr.get_url(), sr.get_source()))
            conn.commit()
        except Exception as e:
            conn.rollback()
            funcset.log("Execution is failed: " + sql)
            funcset.log(e)
        finally:
            cur.close()
            conn.close()


def delete_stock_records(start_date, end_date):
    conn = opendb()
    cur = conn.cursor()
    sql = ""
    try:
        sql = "DELETE FROM RECORDS WHERE RECDATE >= ? AND RECDATE <= ?"
        cur.execute(sql, (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
        conn.commit()
    except Exception as e:
        conn.rollback()
        funcset.log("Execution is failed: " + sql)
        funcset.log(e)
    finally:
        cur.close()
        conn.close()


def top_recommend(start_date, end_date, top_count):
    top_list = []
    conn = opendb()
    cur = conn.cursor()
    sql = ""
    try:
        sql = "SELECT STOCKID, SUM(RECCOUNT) RC FROM (SELECT * FROM STOCK_REC WHERE RECDATE >= ? AND RECDATE <= ?) GROUP BY STOCKID ORDER BY RC DESC  LIMIT ?"
        results = cur.execute(sql, (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), top_count))
        all = results.fetchall()
        for r in all:
            top_list.append(r)
        conn.commit()
    except Exception as e:
        conn.rollback()
        funcset.log("Execution is failed: " + sql)
        funcset.log(e)
    finally:
        cur.close()
        conn.close()
    return top_list
