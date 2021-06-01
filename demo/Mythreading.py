# Mythreading.py 文件名
from PyQt5.QtCore import QThread, pyqtSignal

class RunThread(QThread):

    counter_value = pyqtSignal(int)

    def __init__(self, target, args, name=""):
        QThread.__init__(self)
        self.target = target
        self.args = args
        self.is_running = True

    def run(self):
        #print("starting",self.name, "at:",ctime())
        self.res = self.target(*self.args)

    def stop(self):
    	# 负责停止线程
        self.terminate()
