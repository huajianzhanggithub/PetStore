"""商品管理DAO"""
from com.dao.base_dao import BaseDao


class ProductDao(BaseDao):
    def __init__(self):
        super().__init__()

    def findall(self):
        """查询所有商品信息"""
        products = []
        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 执行SQL操作
                sql = 'select productid,category,cname,ename,image,descn,listprice,unitcost ' \
                      'from products'
                cursor.execute(sql)
                # 提取结果集
                result_set = cursor.fetchall()

                for row in result_set:
                    product = {}
                    product['productid'] = row[0]
                    product['category'] = row[1]
                    product['cname'] = row[2]
                    product['ename'] = row[3]
                    product['image'] = row[4]
                    product['descn'] = row[5]
                    product['listprice'] = row[6]
                    product['unitcost'] = row[7]
                    products.append(product)
                # with代码块结束,游标被关闭

        finally:
            # 关闭数据库
            self.close()

        return products

    def findbycat(self, category):
        """按照商品类别查询商品"""
        products = []
        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 执行SQL操作
                sql = 'select productid,category,cname,ename,image,descn,listprice,unitcost ' \
                      'from products where category = %s'
                cursor.execute(sql, category)
                # 提取结果集
                result_set = cursor.fetchall()

                for row in result_set:
                    product = {}
                    product['productid'] = row[0]
                    product['category'] = row[1]
                    product['cname'] = row[2]
                    product['ename'] = row[3]
                    product['image'] = row[4]
                    product['descn'] = row[5]
                    product['listprice'] = row[6]
                    product['unitcost'] = row[7]
                    products.append(product)
                # with代码块结束,游标被关闭

        finally:
            # 关闭数据库
            self.close()

        return products

    def findbyid(self, productid):
        """按照商品ID查询商品"""
        product = None
        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 执行SQL操作
                sql = 'select productid,category,cname,ename,image,descn,listprice,unitcost ' \
                      'from products where productid = %s'
                cursor.execute(sql, productid)
                # 提取结果集
                row = cursor.fetchone()

                if row is not None:
                    product = {}
                    product['productid'] = row[0]
                    product['category'] = row[1]
                    product['cname'] = row[2]
                    product['ename'] = row[3]
                    product['image'] = row[4]
                    product['descn'] = row[5]
                    product['listprice'] = row[6]
                    product['unitcost'] = row[7]
                # with代码块结束,游标被关闭

        finally:
            # 关闭数据库
            self.close()

        return product
