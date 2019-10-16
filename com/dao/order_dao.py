"""订单管理DAO"""
import pymysql
from com.dao.base_dao import BaseDao


class OrderDao(BaseDao):
    def __init__(self):
        super().__init__()

    def findall(self):
        """查询所以订单"""

        orders = []
        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 执行SQL操作
                sql = 'select orderid, userid, orderdate from orders'
                cursor.execute(sql)
                # 提取结果集
                result_set = cursor.fetchall()

                for row in result_set:
                    order = {}
                    order['orderid'] = row[0]
                    order['userid'] = row[1]
                    order['orderdate'] = row[2]
                    orders.append(order)
                # with代码块结束,关闭游标
        finally:
            self.close()

        return orders

    def create(self, order):
        """创建订单,插入数据库"""

        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 执行插入操作
                sql = 'insert into order (orderid, userid, orderdate, status, amount) ' \
                      'values (%s,%s,%s,%s,%s)'
                affectedcount = cursor.execute(sql, order)
                print('成功插入 {0} 条数据'.format(affectedcount))
                # 提交数据库事务
                self.conn.commit()
        except pymysql.DatabaseError as e:
            self.conn.rollback()
            print(e)
        finally:
            self.close()
