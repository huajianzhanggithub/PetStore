"""自定义GridTaleBase类,用语购物车网格"""
import wx.grid

# 购物车网格列名
COLUMN_NAMES = ['商品编号', '商品名', '商品单价', '数量', '商品应付金额']


class CartGridTable(wx.grid.GridTableBase):
    def __init__(self, data):
        super().__init__()
        self.colLabels = COLUMN_NAMES
        self.data = data

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(COLUMN_NAMES)

    def GetValue(self, row, col):
        product = self.data[row]
        if col == 0:
            return product['productid']
        elif col == 1:
            return product['cname']
        elif col == 2:
            return product['unitcost']
        elif col == 3:
            return product['quantity']
        else:
            return product['amount']

    def GetColLabelValue(self, col):
        return self.colLabels[col]

    def SetValue(self, row, col, value):
        # 只允许修改数量列
        if col != 3:
            return

        # 获得商品数量
        try:
            quantity = int(value)
        except:
            # 输入非数字数据则不能修改
            return

        # 商品数量不能小于0
        if quantity < 0:
            return
        # 更新数据列
        self.data[row]['quantity'] = quantity
        # 计算商品应付金额
        amount = self.data[row]['unitcost'] * quantity
        # 更新商品应付金额列
        self.data[row]['amount'] = amount
