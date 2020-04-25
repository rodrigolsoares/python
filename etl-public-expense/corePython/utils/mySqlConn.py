import mysql.connector

config = {
  'user': 'root',
  'password': 'MySql2019!',
  'host': '127.0.0.1',
  'port': 3307,
  'database': 'etl_despesa_publica',
  'raise_on_warnings': True
}

def getConnection():
    return mysql.connector.connect(**config)


def getClose(cn):
    cn.close()