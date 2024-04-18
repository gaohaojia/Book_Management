###
# 
#  插入窗口
#
###

from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from ui import insertWindow

class InsertWindow(QMainWindow):
    def __init__(self, parent, index):
        QMainWindow.__init__(self)
        self.main_ui = insertWindow.Ui_MainWindow()
        self.main_ui.setupUi(self)
        self._parent = parent

        self.main_ui.insertButton.clicked.connect(self.insert_button_clicked)
        model = QStandardItemModel()
        self.main_ui.insertTable.horizontalHeader().setStretchLastSection(True)
        self.main_ui.insertTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if index == 0:
            model.setHorizontalHeaderLabels(['ISBN','Title','Author','Category','Publisher','Price','PublishDate'])
            for i in range(5):
                model.appendRow([QStandardItem('') for i in range(7)])
        elif index == 2:
            model.setHorizontalHeaderLabels(['OrderID','OrderDate','ISBN','Title','Quantity','Price','CustomerName','CustomerContactInfo'])
            for i in range(5):
                model.appendRow([QStandardItem('') for i in range(8)])
        elif index == 3:
            model.setHorizontalHeaderLabels(['StockInID','StockInDate','ISBN','Title','Quantity','Price'])
            for i in range(5):
                model.appendRow([QStandardItem('') for i in range(6)])
        self.main_ui.insertTable.setModel(model)

        self.setWindowIcon(QIcon('ico.ico'))

    # 点击插入按钮事件
    def insert_button_clicked(self):
        QMessageBox.warning(self, "警告", "外键约束不符合条件！", QMessageBox.Cancel)
        self.destroy()