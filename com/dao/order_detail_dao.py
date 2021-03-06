"""订单明细管理"""
import pymysql
from com.dao.base_dao import BaseDao


class OrderDetailDao(BaseDao):
    def __init__(self):
        super().__init__()

    def create(self, orderdetail):
        """创建订单详细,插入到数据库"""

        try:
            with self.conn.cursor() as cursor:
                sql = 'insert into orderdetails (orderid, productid, quantity, unitcost) ' \
                      'values (%s,%s,%s,%s)'
                affectcount = cursor.execute(sql, orderdetail)
                print('成功插入 {0} 条数据'.format(affectcount))
                self.conn.commit()
        except pymysql.DatabaseError as e:
            self.conn.rollback()
            print(e)
        finally:
            self.conn.close()
