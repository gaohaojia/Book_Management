###
#
#  主窗口
#
###
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import datetime
import time

from ui import main_window

from DB_connector import connector
from SignInWin import SignInWindow
from InsertWin import InsertWindow

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = main_window.Ui_MainWindow()
        self.main_ui.setupUi(self)

        # 参数
        self.isLogin = False

        # 初始化登录窗口
        self._sign_in_window = SignInWindow(self)

        self.main_ui.modeBox.addItems(["全部图书查询", "书目库存查询", "销售记录查询", "进货记录查询", "仓库状态查询"])
        self.main_ui.modeBox.currentIndexChanged.connect(self.fresh_page)
        self.main_ui.startDateEdit.setDate(datetime.date(1900, 1, 1))
        self.main_ui.endDateEdit.setDate(datetime.datetime.now())
        self.main_ui.startDateEdit.setCalendarPopup(True)
        self.main_ui.endDateEdit.setCalendarPopup(True)
        self.main_ui.startDateEdit.dateChanged.connect(self.fresh_page)
        self.main_ui.endDateEdit.dateChanged.connect(self.fresh_page)
        self.main_ui.deleteButton.clicked.connect(self.click_deleteButton)
        self.main_ui.addButton.clicked.connect(self.click_addButton)

        self.main_ui.mainTable.horizontalHeader().setStretchLastSection(True)
        self.main_ui.mainTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.main_ui.mainTable.clicked.connect(self.click_table)
        self.main_ui.mainTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.setObjectName("MainWindow")
        # self.setStyleSheet("#MainWindow{border-image:url(images/background.jpg)}")

        self.setWindowIcon(QIcon('ico.ico'))
    
    # 弹出登录窗口
    def sign_in(self):
        # 初始化界面
        self._sign_in_window.main_ui.account_Inputer.setText("")
        self._sign_in_window.main_ui.Password_Inputer.setText("")
        self._sign_in_window.show()
        self.hide()
    
    # 完成登录
    def finish_sign_in(self):
        self.isLogin = True
        self.fresh_page()
        self.show()

    # 选中表格
    def click_table(self):
        self.main_ui.deleteButton.setEnabled(True if self.main_ui.modeBox.currentIndex() in [0, 2, 3] else False)

    # 插入表格
    def click_addButton(self):
        self._insert_window = InsertWindow(self, self.main_ui.modeBox.currentIndex())
        self._insert_window.show()

    # 点击删除按钮
    def click_deleteButton(self):
        reply = QMessageBox.warning(self, "警告", "是否要删除该行数据？", QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.No:
            return
        select_row = self.main_ui.mainTable.currentIndex().row()
        data = self.main_ui.mainTable.model().index(select_row, 0).data()
        if self.main_ui.modeBox.currentIndex() == 0:
            if not connector.run_insert(f"DELETE FROM Book WHERE ISBN = {data}"):
                QMessageBox.warning(self, "警告", "请先删除该书相关的进货记录和销售记录！", QMessageBox.Cancel)
        if self.main_ui.modeBox.currentIndex() == 2:
            if not connector.run_insert(f"DELETE FROM SalesOrderDetail WHERE OrderID = {data}"):
                QMessageBox.warning(self, "警告", "删除失败！", QMessageBox.Cancel)
            if not connector.run_insert(f"DELETE FROM SalesOrder WHERE OrderID = {data}"):
                QMessageBox.warning(self, "警告", "删除失败！", QMessageBox.Cancel)
        if self.main_ui.modeBox.currentIndex() == 3:
            if not connector.run_insert(f"DELETE FROM StockIn WHERE StockInID = {data}"):
                QMessageBox.warning(self, "警告", "删除失败！", QMessageBox.Cancel)
        self.fresh_page()

    # 刷新界面
    def fresh_page(self):
        self.main_ui.deleteButton.setEnabled(False)
        model = QStandardItemModel()
        if self.main_ui.modeBox.currentIndex() == 0:
            result = connector.run_select(f"SELECT ISBN, Title, Author, CategoryName, PublisherName, Price, PublishDate FROM (Book INNER JOIN BookCategory ON BookCategory.CategoryID = Book.CategoryID) INNER JOIN Publisher ON Publisher.PublisherID = Book.PublisherID WHERE PublishDate BETWEEN '{self.main_ui.startDateEdit.date().toString('yyyy-MM-dd')}' AND '{self.main_ui.endDateEdit.date().toString('yyyy-MM-dd')}'")
            model.setHorizontalHeaderLabels(['ISBN','Title','Author','Category','Publisher','Price','PublishDate'])
            self.main_ui.startDateEdit.setEnabled(True)
            self.main_ui.endDateEdit.setEnabled(True)
            self.main_ui.addButton.setEnabled(True)
        
        if self.main_ui.modeBox.currentIndex() == 1:
            result = connector.run_select("SELECT Book.ISBN, Title, WarehouseName, Quantity FROM (Book INNER JOIN Inventory ON Inventory.ISBN = Book.ISBN) INNER JOIN Warehouse ON Warehouse.WarehouseID = Inventory.WarehouseID")
            model.setHorizontalHeaderLabels(['ISBN','Title','WareHouse','Quantity'])
            self.main_ui.startDateEdit.setEnabled(False)
            self.main_ui.endDateEdit.setEnabled(False)
            self.main_ui.addButton.setEnabled(False)

        if self.main_ui.modeBox.currentIndex() == 2:
            result = connector.run_select(f"SELECT SalesOrder.OrderID, OrderDate, Book.ISBN, Title, Quantity, SalesOrderDetail.Price, CustomerName, ContactInfo FROM ((SalesOrder INNER JOIN SalesOrderDetail ON SalesOrder.OrderID = SalesOrderDetail.OrderID) INNER JOIN Customer ON Customer.CustomerID = SalesOrder.CustomerID) INNER JOIN Book ON Book.ISBN = SalesOrderDetail.ISBN WHERE OrderDate BETWEEN '{self.main_ui.startDateEdit.date().toString('yyyy-MM-dd')}' AND '{self.main_ui.endDateEdit.date().toString('yyyy-MM-dd')}'")
            model.setHorizontalHeaderLabels(['OrderID','OrderDate','ISBN','Title','Quantity','Price','CustomerName','CustomerContactInfo'])
            self.main_ui.startDateEdit.setEnabled(True)
            self.main_ui.endDateEdit.setEnabled(True)
            self.main_ui.addButton.setEnabled(True)

        if self.main_ui.modeBox.currentIndex() == 3:
            result = connector.run_select(f"SELECT StockInID, StockInDate, Book.ISBN, Title, Quantity, StockIn.Price FROM StockIn INNER JOIN Book ON Book.ISBN = StockIn.ISBN WHERE StockInDate BETWEEN '{self.main_ui.startDateEdit.date().toString('yyyy-MM-dd')}' AND '{self.main_ui.endDateEdit.date().toString('yyyy-MM-dd')}'")
            model.setHorizontalHeaderLabels(['StockInID','StockInDate','ISBN','Title','Quantity','Price'])
            self.main_ui.startDateEdit.setEnabled(True)
            self.main_ui.endDateEdit.setEnabled(True)
            self.main_ui.addButton.setEnabled(True)

        if self.main_ui.modeBox.currentIndex() == 4:
            result = connector.run_select("SELECT WarehouseName, Location, InventoryCount, Capacity, CONCAT(InventoryCount*100/Capacity,'%') FROM Warehouse INNER JOIN (SELECT WarehouseID, SUM(Quantity) AS InventoryCount FROM Inventory GROUP BY WarehouseID) AS CacheTable ON CacheTable.WarehouseID = Warehouse.WarehouseID")
            model.setHorizontalHeaderLabels(['Warehouse','Location','Count','Capacity','Proportion'])
            self.main_ui.startDateEdit.setEnabled(False)
            self.main_ui.endDateEdit.setEnabled(False)
            self.main_ui.addButton.setEnabled(False)
        
        for row in result:
            model.appendRow([QStandardItem(str(item)) for item in row])
        self.main_ui.mainTable.setModel(model)