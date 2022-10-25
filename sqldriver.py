#-*- coding: UTF-8 -*-
import pymysql
from dbutils.pooled_db import PooledDB
from config import sqlconfig
'''
@功能：PT数据库连接池
'''
class PTConnectionPool(object):
    __pool = None;
    # def __init__(self):
    #     self.conn = self.__getConn();
    #     self.cursor = self.conn.cursor();
    
    def __enter__(self):
        self.conn = self.__getConn()
        self.cursor = self.conn.cursor()
        print ("PT数据库创建con和cursor")
        return self

    def __getConn(self):
        if self.__pool is None:
            self.__pool = PooledDB(creator=MySQLdb, mincached=sqlconfig.DB_MIN_CACHED , maxcached=sqlconfig.DB_MAX_CACHED,
                               maxshared=sqlconfig.DB_MAX_SHARED, maxconnections=sqlconfig.DB_MAX_CONNECYIONS,
                               blocking=sqlconfig.DB_BLOCKING, maxusage=sqlconfig.DB_MAX_USAGE,
                               setsession=sqlconfig.DB_SET_SESSION,
                               host=sqlconfig.DB_HOST , port=sqlconfig.DB_PORT ,
                               user=sqlconfig.DB_USER , passwd=sqlconfig.DB_PASSWORD ,
                               db=sqlconfig.DB_DBNAME , use_unicode=False, charset=sqlconfig.DB_CHARSET);
        return self.__pool.connection()
    """
    @summary: 释放连接池资源
    """
    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()
        print ("PT连接池释放con和cursor")

    #重连接池中取出一个连接
    def getconn(self):
        conn = self.__getConn()
        cursor = conn.cursor()
        return cursor,conn

    #关闭连接归还给连接池
    # def close(self):
    #     self.cursor.close()
    #     self.conn.close()
    #     print u"PT连接池释放con和cursor";


    def getPTConnection():
        return PTConnectionPool()