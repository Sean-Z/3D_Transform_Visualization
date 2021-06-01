import sys
import ctypes
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDesktopWidget, QAction, qApp, QMenu
from PyQt5.QtWidgets import QLCDNumber, QSlider, QVBoxLayout, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QGraphicsView, QComboBox, QGridLayout, QGroupBox, QRadioButton, QLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QSpinBox, QSpacerItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from interface import Ui_Form
import numpy as np
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import transform
# 相关预设




class MainWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        # 初始化继承的父类（Qmainwindow），调用了父类的构造函数
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # 设置固定窗口大小
        self.setFixedSize(1180, 750)
        # 创建窗口标题
        self.setWindowTitle('Transform')
        # 设置图标
        self.setWindowIcon(QIcon('./resources/icon.png'))
        # 窗口居中
        self.center()

        # 全局布局
        wlayout = QHBoxLayout()
        left_wlayout = QHBoxLayout()
        right_wlayout = QHBoxLayout()

        self._set_left_wlayout(left_wlayout)
        self._set_right_wlayout(right_wlayout)

        wlayout.addLayout(left_wlayout)
        wlayout.addLayout(right_wlayout)

        self.setLayout(wlayout)

        self.show()


    def center(self):
        """窗口居中"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _set_left_wlayout(self, left_wlayout):
        """设置左侧布局"""

        # 定义窗口w为GLViewWidget部件
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 20  # 初始视角高度
        self.w.setFixedSize(700, 700)

        xgrid = gl.GLGridItem()
        ygrid = gl.GLGridItem()
        zgrid = gl.GLGridItem()
        self.w.addItem(xgrid)
        self.w.addItem(ygrid)
        self.w.addItem(zgrid)

        xgrid.rotate(90, 0, 1, 0)
        ygrid.rotate(90, 1, 0, 0)

        xgrid.scale(0.2, 0.1, 0.1)
        ygrid.scale(0.2, 0.1, 0.1)
        zgrid.scale(0.1, 0.2, 0.1)

        # g用来显示白色网格
        self.g = gl.GLGridItem()
        self.w.addItem(self.g)
        self.w.show()  # 显示窗口
        left_wlayout.addWidget(self.w)

    def _set_right_wlayout(self, right_wlayout):
        """设置右侧布局"""
        # 四元数部分
        self.quat_lab1 = QLabel('x: ')
        self.quat_lab2 = QLabel('y: ')
        self.quat_lab3 = QLabel('z: ')
        self.quat_lab4 = QLabel('w: ')

        self.quat_ldt1 = QLineEdit()
        self.quat_ldt2 = QLineEdit()
        self.quat_ldt3 = QLineEdit()
        self.quat_ldt4 = QLineEdit()

        quat_layout = QGridLayout()
        quat_layout.addWidget(self.quat_lab1, 0, 0)
        quat_layout.addWidget(self.quat_lab2, 0, 2)
        quat_layout.addWidget(self.quat_lab3, 1, 0)
        quat_layout.addWidget(self.quat_lab4, 1, 2)
        quat_layout.addWidget(self.quat_ldt1, 0, 1)
        quat_layout.addWidget(self.quat_ldt2, 0, 3)
        quat_layout.addWidget(self.quat_ldt3, 1, 1)
        quat_layout.addWidget(self.quat_ldt4, 1, 3)

        quat_gbx = QGroupBox('四元数')
        quat_gbx.setAlignment(4)
        quat_gbx.setLayout(quat_layout)

        # 欧拉角部分
        # Yaw部分
        self.Yaw_lab = QLabel('Yaw: ')
        self.Yaw_ldt = QSpinBox()
        self.Yaw_sld = QSlider()

        self.Yaw_sld.setOrientation(Qt.Horizontal)
        self.Yaw_sld.setMaximum(180)
        self.Yaw_sld.setMinimum(-180)
        self.Yaw_sld.setFixedWidth(100)
        self.Yaw_ldt.setFixedWidth(100)
        self.Yaw_ldt.setMinimum(-180)
        self.Yaw_ldt.setMaximum(180)
        Yaw_h_layout = QHBoxLayout()
        Yaw_h_layout.addWidget(self.Yaw_lab)
        Yaw_h_layout.addWidget(self.Yaw_ldt)
        Yaw_h_layout.addWidget(self.Yaw_sld)

        Yaw_widget = QWidget()  # 布局不能直接嵌套布局，需要依附在widget
        Yaw_widget.setLayout(Yaw_h_layout)

        # Pitch部分
        self.Pitch_lab = QLabel('Pitch: ')
        self.Pitch_ldt = QSpinBox()
        self.Pitch_sld = QSlider()

        self.Pitch_sld.setOrientation(Qt.Horizontal)
        self.Pitch_sld.setMaximum(180)
        self.Pitch_sld.setMinimum(-180)
        self.Pitch_sld.setFixedWidth(100)
        self.Pitch_ldt.setFixedWidth(100)
        self.Pitch_ldt.setMinimum(-180)
        self.Pitch_ldt.setMaximum(180)
        Pitch_h_layout = QHBoxLayout()
        Pitch_h_layout.addWidget(self.Pitch_lab)
        Pitch_h_layout.addWidget(self.Pitch_ldt)
        Pitch_h_layout.addWidget(self.Pitch_sld)

        Pitch_widget = QWidget()  # 布局不能直接嵌套布局，需要依附在widget
        Pitch_widget.setLayout(Pitch_h_layout)

        # Roll部分
        self.Roll_lab = QLabel('Roll: ')
        self.Roll_ldt = QSpinBox()
        self.Roll_sld = QSlider()

        self.Roll_sld.setOrientation(Qt.Horizontal)
        self.Roll_sld.setMaximum(180)
        self.Roll_sld.setMinimum(-180)
        self.Roll_sld.setFixedWidth(100)
        self.Roll_ldt.setFixedWidth(100)
        self.Roll_ldt.setMinimum(-180)
        self.Roll_ldt.setMaximum(180)
        Roll_h_layout = QHBoxLayout()
        Roll_h_layout.addWidget(self.Roll_lab)
        Roll_h_layout.addWidget(self.Roll_ldt)
        Roll_h_layout.addWidget(self.Roll_sld)

        Roll_widget = QWidget()  # 布局不能直接嵌套布局，需要依附在widget
        Roll_widget.setLayout(Roll_h_layout)

        # 槽
        self.Yaw_sld.valueChanged.connect(self.slot_yaw_changed)
        self.Pitch_sld.valueChanged.connect(self.slot_pitch_changed)
        self.Roll_sld.valueChanged.connect(self.slot_roll_changed)


        # Euler角部分垂直布局
        Euler_v_layout = QVBoxLayout()
        Euler_v_layout.addWidget(Yaw_widget)
        Euler_v_layout.addWidget(Pitch_widget)
        Euler_v_layout.addWidget(Roll_widget)

        Euler_widget = QWidget()  # 布局不能直接嵌套布局，需要依附在widget
        Euler_widget.setLayout(Euler_v_layout)

        euler_gbx = QGroupBox('欧拉角')
        euler_gbx.setAlignment(4)
        euler_gbx.setLayout(Euler_v_layout)

        # 平移向量部分
        self.vector_lab1 = QLabel('x: ')
        self.vector_lab2 = QLabel('y: ')
        self.vector_lab3 = QLabel('z: ')

        self.vector_ldt1 = QLineEdit()
        self.vector_ldt2 = QLineEdit()
        self.vector_ldt3 = QLineEdit()

        vector_layout = QGridLayout()
        vector_layout.addWidget(self.vector_lab1, 0, 0)
        vector_layout.addWidget(self.vector_ldt1, 0, 1)
        vector_layout.addWidget(self.vector_lab2, 0, 2)
        vector_layout.addWidget(self.vector_ldt2, 0, 3)
        vector_layout.addWidget(self.vector_lab3, 0, 4)
        vector_layout.addWidget(self.vector_ldt3, 0, 5)

        vector_gbx = QGroupBox('平移向量')
        vector_gbx.setAlignment(4)
        vector_gbx.setLayout(vector_layout)

        # 旋转矩阵
        self.Mat00 = QLineEdit()
        self.Mat01 = QLineEdit()
        self.Mat02 = QLineEdit()
        self.Mat10 = QLineEdit()
        self.Mat11 = QLineEdit()
        self.Mat12 = QLineEdit()
        self.Mat20 = QLineEdit()
        self.Mat21 = QLineEdit()
        self.Mat22 = QLineEdit()

        matrix_layout = QGridLayout()
        matrix_layout.addWidget(self.Mat00, 0, 0)
        matrix_layout.addWidget(self.Mat01, 0, 1)
        matrix_layout.addWidget(self.Mat02, 0, 2)
        matrix_layout.addWidget(self.Mat10, 1, 0)
        matrix_layout.addWidget(self.Mat11, 1, 1)
        matrix_layout.addWidget(self.Mat12, 1, 2)
        matrix_layout.addWidget(self.Mat20, 2, 0)
        matrix_layout.addWidget(self.Mat21, 2, 1)
        matrix_layout.addWidget(self.Mat22, 2, 2)

        matrix_widget = QWidget()
        matrix_widget.setLayout(matrix_layout)

        matrix_gbx = QGroupBox('旋转矩阵')
        matrix_gbx.setAlignment(4)
        matrix_gbx.setLayout(matrix_layout)

        # 角轴
        axies_lab1 = QLabel('x: ')
        axies_lab2 = QLabel('y: ')
        axies_lab3 = QLabel('z: ')
        axies_lab4 = QLabel('angle: ')

        self.axies_ldt1 = QLineEdit()
        self.axies_ldt2 = QLineEdit()
        self.axies_ldt3 = QLineEdit()
        self.axies_ldt4 = QLineEdit()

        axies_layout = QGridLayout()
        axies_layout.addWidget(axies_lab1, 0, 0)
        axies_layout.addWidget(self.axies_ldt1, 0, 1)
        axies_layout.addWidget(axies_lab2, 1, 0)
        axies_layout.addWidget(self.axies_ldt2, 1, 1)
        axies_layout.addWidget(axies_lab3, 2, 0)
        axies_layout.addWidget(self.axies_ldt3, 2, 1)
        axies_layout.addWidget(axies_lab4, 3, 0)
        axies_layout.addWidget(self.axies_ldt4, 3, 1)

        axies_gbx = QGroupBox('角轴')
        axies_gbx.setAlignment(4)
        axies_gbx.setLayout(axies_layout)


        MA_h_layout = QHBoxLayout()
        MA_h_layout.addWidget(matrix_gbx)
        MA_h_layout.addWidget(axies_gbx)
        MA_gbx = QGroupBox()
        MA_gbx.setLayout(MA_h_layout)
        # 右边垂直布局

        G_v_layout = QVBoxLayout()
        G_v_layout.addWidget(quat_gbx)
        G_v_layout.addWidget(euler_gbx)
        G_v_layout.addWidget(MA_gbx)
        G_v_layout.addWidget(vector_gbx)

        G_v_layout.addStretch(1)

        # 设置Group Box
        show_gbx = QGroupBox('控制窗口')
        show_gbx.setLayout(G_v_layout)

        right_wlayout.addWidget(show_gbx)

    def show_coord(self):
        """显示坐标系"""
        pass

    def slot_yaw_changed(self, value):
        self.Yaw_ldt.setValue(value)

    def slot_pitch_changed(self, value):
        self.Pitch_ldt.setValue(value)

    def slot_roll_changed(self, value):
        self.Roll_ldt.setValue(value)


if __name__ == "__main__":
    # windows任务栏图标显示
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行 创建一个应用
    app = QApplication(sys.argv)
    # 初始化 创建一个窗口
    mainWindow = MainWindow()
    # 将窗口控件显示在屏幕上
    mainWindow.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
