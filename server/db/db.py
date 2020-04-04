#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Project: $Project$
Filename: $Filename$
Author: $Date$
Date: $Date$
Revision: $Revision$
Description: $Description$
"""

try:
    from Queue import Queue
except:
    from queue import Queue
import threading
import time
import re
import datetime
import os
import uuid
import traceback
import logging
import pymysql

log = logging.getLogger(__name__)


class PoolError(Exception):
    """
    连接异常类
    """
    pass


class PooledConnection(object):
    """
    连接池
    """
    def __init__(self, connection_strings, max_count=10, min_free_count=1):
        self._max_count = max_count
        self._min_free_count = min_free_count
        self._connection_strings = connection_strings
        self._count = 0
        self._queue = Queue(max_count)
        self._lock = threading.Lock()
        self._run_monitor()

    def __del__(self):
        while not self._queue.empty():
            conn = self._queue.get()
            if conn:
                self._close_connection(conn)
            else:
                break

    def _run_monitor(self):
        pass

    def _create_connection(self, autoCommit=True):
        if self._count >= self._max_count:
            raise PoolError('The maximum number of connections beyond!')

        conn = Connection(self, host=self._connection_strings.get('host'),
                          port=self._connection_strings.get('port'),
                          user=self._connection_strings.get('user'),
                          password=self._connection_strings.get('password'),
                          db=self._connection_strings.get('database'),
                          charset='utf8',
                          autocommit=autoCommit,
                          cursorclass=pymysql.cursors.DictCursor)
        self._count += 1
        return conn

    def release_connection(self, connection):
        """
        释放连接
        """
        self._lock.acquire()
        if self._queue.qsize() >= self._min_free_count:
            self._close_connection(connection)
        else:
            self._queue.put(connection)
        self._lock.release()

    def get_connection(self, timeout=15):
        """
        获取一个连接
        """
        bt = datetime.datetime.now()
        def get_conn():
            self._lock.acquire()
            try:
                if not self._queue.empty():
                    conn = self._queue.get()
                elif self._count < self._max_count:
                    conn = self._create_connection()
                else:
                    conn = None
                return conn
            except Exception as err:
                raise
            finally:
                self._lock.release()

        conn = get_conn()
        if conn:
            return conn
        else:
            if timeout:
                while (datetime.datetime.now() - bt).seconds < timeout:
                    conn = get_conn()
                    if conn:
                        break
                    time.sleep(0.2)
            if not conn:
                raise PoolError(
                    'Timeout!There has no enough connection to be used!')
            return conn

    def _close_connection(self, connection):
        """
        关闭连接
        """
        try:

            if connection._close():
                self._count -= 1
        except Exception as err:
            pass


class Connection(object):
    """
    连接类
    """
    PARAMERTS_REG = re.compile(r'\:([_0-9]*[_A-z]+[_0-9]*[_A-z]*)')

    def __init__(self, pool, *args, **kwargs):
        self._pool = pool
        self.id = uuid.uuid4()

        # 连不上数据库时，自动重试
        try:
            self._conn = pymysql.connections.Connection(*args, **kwargs)
            self.__is_closed = False
        except pymysql.err.OperationalError:
            self._conn = pymysql.connections.Connection(*args, **kwargs)
            self.__is_closed = False

    def __del__(self):
        """
        销毁连接
        """
        self.drop()

    def execute(self, sql, args=None):
        """
        执行 sql
        """
        cursor = self._conn.cursor()
        sqlText = self.PARAMERTS_REG.sub(r'%(\1)s', sql)
        modelAttrs = []
        result = self.PARAMERTS_REG.finditer(sql)

        for m in result:
            modelAttrs.append(m.group(1))

        def filter_args(modelAttrs, m):
            if m is None:
                return None

            return {a: m[a] for a in modelAttrs}

        query = cursor.mogrify(sqlText, filter_args(modelAttrs, args))

        if args and isinstance(args, list):

            cursor.executemany(
                sqlText, [filter_args(modelAttrs, a) for a in args])
        else:

            cursor.execute(sqlText, filter_args(modelAttrs, args))

        return cursor

    def insert(self, sql, args=None):
        """
        插入记录
        """

        cursor = None
        try:
            cursor = self.execute(sql, args)
            row_id = cursor.lastrowid
            return row_id
        except:
            raise
        finally:
            cursor and cursor.close()

    def update(self, sql, args=None):
        """
        更新记录
        """

        cursor = None
        try:
            cursor = self.execute(sql, args)
            row_count = cursor.rowcount

            if not row_count:
                log.debug(cursor._last_executed)

            return row_count
        except:
            raise
        finally:
            cursor and cursor.close()

    def delete(self, sql, args=None):
        """
        删除记录
        """

        cursor = None
        try:
            cursor = self.execute(sql, args)
            row_count = cursor.rowcount
            return row_count
        except:
            raise
        finally:
            cursor and cursor.close()

    def query(self, sql, args=None):
        """
        查询
        """

        cursor = None
        try:
            cursor = self.execute(sql, args)
            return cursor.fetchall()
        except:
            raise
        finally:
            cursor and cursor.close()

    def query_one(self, sql, args=None):
        """
        查询返回一条数据
        """

        cursor = None
        try:
            cursor = self.execute(sql, args)
            return cursor.fetchone()
        except:
            raise
        finally:
            cursor and cursor.close()

    def release(self):
        """
        释放连接，将连接放回连接池
        """

        self._pool.release_connection(self)

    def close(self):
        """
        释放连接，将连接放回连接池
        """

        self.release()

    def drop(self):
        """
        丢弃连接
        """

        self._pool._close_connection(self)

    def _close(self):
        """
        真正关闭
        """

        if self.__is_closed:
            return False
        try:

            self._conn.close()
            self.__is_closed = True

        except:
            log.error(traceback.format_exc())

        return True


class MySQLdb(object):
    """
    mysql 的数据库操作类，支持连接池
    """

    def __init__(self, cfg):
        self.config = cfg
        self._pool = PooledConnection(self.config,
                                      self.config.get('maxConnections'),
                                      self.config.get('minFreeConnections', 1))

    def execute(self, sql, args=None):
        """
        执行 sql
        """

        cursor = None
        conn = None
        try:
            try:
                conn = self._pool.get_connection()
                cursor = conn.execute(sql, args)
            except pymysql.err.OperationalError:
                log.error('execute error ready to retry:',
                          traceback.format_exc())
                conn and conn.drop()
                conn = self._pool.get_connection()
                cursor = conn.execute(sql, args)
            except RuntimeError:
                log.error('execute error ready to retry:',
                          traceback.format_exc())
                conn and conn.drop()
                conn = self._pool.get_connection()
                cursor = conn.execute(sql, args)
        except pymysql.err.InterfaceError:
            raise
        except pymysql.err.IntegrityError:
            raise
        except:
            log.error('execute error ready to retry:', traceback.format_exc())
            conn and conn.drop()
            conn = None
        finally:
            conn and conn.release()

        return cursor

    def insert(self, sql, args=None):
        """
        插入记录
        """
        cursor = None
        try:
            cursor = self.execute(sql, args)
            row_id = cursor.lastrowid
            return row_id
        except:
            raise
        finally:
            cursor and cursor.close()

    def update(self, sql, args=None):
        """
        更新记录
        """
        cursor = None
        try:
            cursor = self.execute(sql, args)
            row_count = cursor.rowcount
            return row_count
        except:
            raise
        finally:
            cursor and cursor.close()

    def delete(self, sql, args=None):
        """
        删除记录
        """
        cursor = None
        try:
            cursor = self.execute(sql, args)
            row_count = cursor.rowcount
            return row_count
        except:
            raise
        finally:
            cursor and cursor.close()

    def query(self, sql, args=None):
        """
        查询
        """
        cursor = None
        try:
            cursor = self.execute(sql, args)
            return cursor.fetchall()
        except:
            raise
        finally:
            cursor and cursor.close()

    def query_one(self, sql, args=None):
        """
        查询返回一条数据
        """
        cursor = None
        try:
            cursor = self.execute(sql, args)
            return cursor.fetchone()
        except:
            raise
        finally:
            cursor and cursor.close()

    def begin(self):
        """
        开启并返回一个事务
        """

        tran = Transaction(self._pool.get_connection())
        tran.begin()

        return tran

    def commit(self, tran):
        """
        提交事务
        """
        return tran.commit()

    def rollback(self, tran):
        """
        回滚事务
        """
        return tran.rollback()


class Transaction(object):
    """
    事务类
    """

    def __init__(self, conn):
        self.__isBegan = False
        self.conn = conn
        self.__old_autocommit = self.conn._conn.get_autocommit()
        self.conn._conn.autocommit(False)

    def begin(self):
        """
        开启事务
        """

        if not self.__isBegan:
            self.conn._conn.begin()
            self.__isBegan = True

    def commit(self):
        """
        提交事务
        """

        self.conn._conn.commit()
        self.__isBegan = False
        self._finished()

    def rollback(self):
        """
        回滚事务
        """

        self.conn._conn.rollback()
        self.__isBegan = False
        self._finished()

    def _finished(self):
        self.__reset_autocommit()
        self.conn.release()

    def __reset_autocommit(self):
        """
        将连接的自动提交设置重置回原来的设置
        """
        self.conn._conn.autocommit(self.__old_autocommit)

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
