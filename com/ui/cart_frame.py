"""商品购物车窗口"""
import datetime
import sys
import wx
import wx.grid

from com.dao.order_dao import OrderDao
from com.dao.product_dao import ProductDao
from com.dao.order_detail_dao import OrderDetailDao
from com.ui.cart_gridtable import CartGridTable
from com.ui.my_frame import MyFrame


class CartFrame(MyFrame):
    def __init__(self, cart, product_list_frame):
        super().__init__(title='商品购物车', size=(1000, 700))

        # 购物车, 奸尸选择的商品Id,值是商品的数量
        self.cart = cart
        self.product_list_frame = product_list_frame

        # 加载数据到data
        self.data = self.loaddata()

        # 设置整个窗口布局是垂直box布局
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.contentpanel.SetSizer(vbox)

        # 添加顶部对象(topbox)到vbox
        vbox.Add(self.createtopbox(), 1, flag=wx.EXPAND | wx.ALL, border=10)

        # 添加底部对象(topbox)到vbox
        vbox.Add(self.creategrid(), 1, flag=wx.CENTER | wx.FIXED_MINSIZE | wx.ALL, border=10)

        # 为当前Frame对象添加默认状态栏
        self.CreateStatusBar()
        self.SetStatusText('装备就绪')

    def loaddata(self):
        """根据购物车中保存的商品ID查询出商品的其他属性"""

        data = []
        keys = self.cart.keys()
        for productid in keys:
            # 创建DAO对象
            dao = ProductDao()
            product = dao.findbyid(productid)

            row = {}
            row['productid'] = product['productid']  # 商品编号
            row['cname'] = product['cname']          # 商品中文名
            row['unitcost'] = product['unitcost']    # 单价
            row['quantity'] = self.cart[productid]    # 数量
            # 计算商品应付金额
            amount = row['unitcost']*row['quantity']
            row['amount'] = amount

            data.append(row)

        return data

    def createtopbox(self):
        """创建顶部布局管理器topbox"""

        # 创建按钮对象
        return_btn = wx.Button(parent=self.contentpanel, label='返回商品列表')
        submit_btn = wx.Button(parent=self.contentpanel, label='提交订单')
        # 绑定事件处理
        self.Bind(wx.EVT_BUTTON, self.return_btn_onclick, return_btn)
        self.Bind(wx.EVT_BUTTON, self.submit_btn_onclick, submit_btn)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.AddSpacer(350)
        box.Add(return_btn, 1, flag=wx.EXPAND | wx.ALL, border=10)
        box.Add(submit_btn, 1, flag=wx.EXPAND | wx.ALL, border=10)
        box.AddSpacer(350)

        return box

    def creategrid(self):
        """创建购物车表格"""

        # 创建网格对象
        grid = wx.grid.Grid(self.contentpanel, name='grid')

        # 初始化表格
        # 创建网格中所需的表格
        table = CartGridTable(self.data)
        # 设置网格的表格属性
        grid.SetTable(table, True)
        grid.SetSize(1000, 600)

        # 设置网格所有行高
        rowsizeinfo = wx.grid.GridSizesInfo(40, [])
        grid.SetRowSizes(rowsizeinfo)

        # 设置网格所有列宽
        colsizeinfo = wx.grid.GridSizesInfo(176, [])
        grid.SetColSizes(colsizeinfo)
        # 设置单元格默认字体
        grid.SetDefaultCellFont(wx.Font(11, wx.FONTFAMILY_DEFAULT,
                                        wx.FONTSTYLE_NORMAL,
                                        wx.FONTWEIGHT_NORMAL,
                                        faceName='微软雅黑'))

        # 设置行和列标题的默认字体
        grid.SetLabelFont(wx.Font(9, wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL,
                                  wx.FONTWEIGHT_NORMAL,
                                  faceName='微软雅黑'))
        # 设置表格选择模式为行选择
        grid.SetSelectionMode(grid.wxGridSelectRows)
        # 设置不能通过拖动改变行高度
        grid.DisableDragRowSize()
        # 设置不能通过拖动改变列宽度
        grid.DisableDragColSize()

        return grid

    def return_btn_onclick(self, event):
        """返回商品列表按钮事件处理"""

        # 更新购物车
        for gridrowdata in self.data:
            productid = gridrowdata['productid']    # 商品编号
            quantity = gridrowdata['quantity']      # 数量
            self.cart[productid] = quantity

        self.product_list_frame.Show()
        self.Hide()

    def submit_btn_onclick(self, event):
        """提交订单按钮事件处理"""
        # 生成订单
        self.generateorders()

        dlg =wx.MessageDialog(self, '订单已经生成,等待付款...', '信息', wx.YES_NO | wx.ICON_INFORMATION)

        if dlg.ShowModal() == wx.ID_YES:
            # TODO 等待付款
            print('等待付款...')
            pass

        #退出系统
        dlg.Destroy()
        self.Destroy()
        sys.exit(0)


    def generateorders(self):
        """生成订单"""

        orderdate = datetime.datetime.today()
        # 从用户session中取出用户id
        userid = MyFrame.Session['userid']
        orderid = int(orderdate.timestamp()*1000)
        status = 0
        amount = self.getorderamount()

        order = orderid, userid, orderdate, status, amount
        # 创建订单
        orderdao = OrderDao()
        orderdao.create(order)

        for row in self.data:
            orderdetail = orderid, row['productid'], row['quantity'], row['unitcost']
            # 创建订单明细
            orderdetaildao = OrderDetailDao()
            orderdetaildao.create(orderdetail)


    def getorderamount(self):
        """计算订单应付总金额"""

        totalamount = 0.0
        for row in self.data:
            totalamount += float(row['amount'])

        return totalamount

