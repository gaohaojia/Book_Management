from PyQt5.QtWidgets import QApplication
import sys

from MainWin import MainWindow

# 主函数
def main():
    app = QApplication(sys.argv)
    _main_window = MainWindow()
    _main_window.sign_in()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()