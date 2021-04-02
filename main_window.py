import sys
import ctypes
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QAction, qApp, QMenu
from PyQt5.QtGui import QIcon
from interface import Ui_Form


class MainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        # 初始化继承的父类（Qmainwindow），调用了父类的构造函数
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # 设置窗口的大小
        self.resize(900, 600)
        # 实例化创建状态栏
        self.status = self.statusBar()
        # 将提示信息显示在状态栏中showMessage（‘提示信息'，显示时间（单位毫秒））
        self.status.showMessage('这是状态栏提示', 40000)
        # 创建窗口标题
        self.setWindowTitle('Transform')
        # 放在屏幕固定位置
        # self.move(500, 150)
        # 设置图标
        self.setWindowIcon(QIcon('./resources/icon.png'))
        # 窗口居中
        self.center()

        # QMenuBar： 就是所有窗口的菜单栏，在此基础上添加不同的QMenu和QAction
        # QMenu： 菜单栏里面菜单，可以显示文本和图标，但是并不负责执行操作，有点类似label的作用
        # QAction： Qt将用户与界面进行交互的元素抽象为一种“动作”，使用QAction类表示。QAction才是真正负责执行操作的部件
        # 菜单栏
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        editMenu = menubar.addMenu('&Edit')
        viewMenu = menubar.addMenu('&View')
        # 子菜单
        impMenu = QMenu('Import', self)
        impAct = QAction('Import mail', self)
        impMenu.addAction(impAct)

        newAct = QAction('New', self)

        fileMenu.addAction(newAct)
        fileMenu.addMenu(impMenu)

    def center(self):
        """窗口居中"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == "__main__":
    # windows任务栏图标显示
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    mainWindow = MainWindow()
    # 将窗口控件显示在屏幕上
    mainWindow.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())