###
# 
#  注册窗口
#
###

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QGraphicsOpacityEffect, QMessageBox

from ui import sign_up_window

class SignUpWindow(QMainWindow):
    def __init__(self, _main_window):
        QMainWindow.__init__(self)
        self.main_ui = sign_up_window.Ui_Sign_up_window()
        self.main_ui.setupUi(self)
        self._main_window = _main_window

        # 固定窗口大小
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        # 创建按钮点击事件
        self.main_ui.Sign_up_button.clicked.connect(lambda: self.sign_up_button_clicked())

        # 回车确认事件
        self.main_ui.Password_Inputer_2.returnPressed.connect(lambda: self.sign_up_button_clicked())

        # 展示图片
        self.main_ui.background_image.setPixmap(QtGui.QPixmap('images/sign.jpg'))
        op = QGraphicsOpacityEffect()
        op.setOpacity(0.3)  # 透明度设置为0.5
        self.main_ui.background_image.setGraphicsEffect(op)
        self.main_ui.background_image.setScaledContents(True)

        self.setWindowIcon(QtGui.QIcon('ico.ico'))
    
    # 注册按钮点击事件
    def sign_up_button_clicked(self):
        account = self.main_ui.account_Inputer.text()
        password = self.main_ui.Password_Inputer.text()
        password2 = self.main_ui.Password_Inputer_2.text()

        # 判断账号信息是否未空
        if account == "":
            QMessageBox.warning(self, "警告", "未输入账号！", QMessageBox.Cancel)
            return
        if number == "":
            QMessageBox.warning(self, "警告", "未输入职工号/学号！", QMessageBox.Cancel)
            return


        # 判断两次输入是否一致
        if password != password2:
            QMessageBox.warning(self, "警告", "密码不符合规范！", QMessageBox.Cancel)
            return
        
        # 尝试保存账户
        QMessageBox.about(self, "成功", "注册成功！")
        self.destroy()