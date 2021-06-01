# pyqt5_graph.py 文件名
import pyqtgraph as pg
from TmpData import _read_data, wind_mach_chooice

colour = ["r", "g", "b"]
yp_list = ["叶片1", "叶片2", "叶片3"]


def _data_to_dict():
    mydict = {}
    for my_vars, i in zip(_read_data(), range(len(_read_data()))):
        tmp_dict = {}
        for var, j in zip(my_vars, range(len(my_vars))):
            tmp_dict[var[0]] = var[1]
        mydict[i] = tmp_dict
    return mydict


def plt_init():
    # 绘图初始化
    pg.setConfigOption("background", "w")
    plt = pg.PlotWidget()
    plt.addLegend(size=(150, 80))
    plt.showGrid(x=True, y=True, alpha=0.5)
    return plt


def plt_show(num):
    # 传绘制的新图
    mydict = _data_to_dict()
    pg.setConfigOption("background", "w")
    plt = pg.PlotWidget()
    plt.addLegend(size=(150, 80))
    plt.showGrid(x=True, y=True, alpha=0.5)
    for i in num.split(","):
        i = int(i) - 1
        plt.plot(x=list(mydict[i].keys()), y=list(mydict[i].values()), pen=colour[i],
                 name=yp_list[i])

    return plt


if __name__ == '__main__':
    _data_to_dict()
    pass
