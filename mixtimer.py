import sys
import time
import re
import global_value as gv
import ctypes
import images
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QTimer
from pynput.keyboard import Key, Controller
from mainwindow import Ui_ReaderTimer


class MainWindow(QMainWindow):   
    def __init__(self):
        super(MainWindow, self).__init__()        
        self.ui = Ui_ReaderTimer()
        self.ui.setupUi(self)
        # 创建定时器和键盘控制
        self.keyboard = Controller()
        self.timer = QTimer()
        self.timer.timeout.connect(self.one_second_event)
        # 全局变量
        self.cycle_index = 0    # 计时器循环次数，为0时表示无穷
        self.timer_delay_seconds = 15   # 翻页间隔(无暂停情况下)
        self.countdown = 0  # 倒计时
        self.next_page_mode = 0    # 翻页方式
        # 初始化并连接信号和槽函数
        self.setWindowTitle('MixTimer -'+gv.VERSION)    # 修改标头
        self.setWindowIcon(QtGui.QIcon(":/images/timer.ico"))   # 虚拟图片
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")    # 状态栏图标
        self.ui.LabelAddress.setText('<a href={}>新版下载地址'.format(gv.DOWNLOAD_ADDRESS))      
        self.ui.LabelAddress.setOpenExternalLinks(True) # 下载地址超链接      
        self.ui.LabelQR.setPixmap(QtGui.QPixmap(':/images/SponsorshipQRCode.jpg'))   # 赞助码  
        # Tab0
        self.ui.ButtStart.clicked.connect(self.timer_start)
        self.ui.ButtStop.clicked.connect(self.timer_stop)
        self.ui.ButtPause.clicked.connect(self.timer_pause)
        self.ui.ButtAdd.clicked.connect(self.add_time)
        self.ui.ButtDel.clicked.connect(self.del_time)
        self.ui.EditTimer.textChanged.connect(self.reset_timer)
        self.ui.CboxMode.currentIndexChanged.connect(self.reset_mode)
        self.ui.ButtPause.setEnabled(False) # 初始化时，暂停按键被禁用
        # Tab_setting
        self.ui.CboxCycleMode.currentIndexChanged.connect(self.reset_cycle_mode)
        self.ui.EditCycleTimes.textChanged.connect(self.reset_cycle_index)
        self.ui.ButtAddCt.clicked.connect(self.add_cycle_times)
        self.ui.ButtDelCt.clicked.connect(self.del_cycle_times)
        self.ui.EditCycleTimes.setEnabled(False)
        self.ui.ButtAddCt.setEnabled(False)
        self.ui.ButtDelCt.setEnabled(False)

    def timer_start(self):
        """开始计时：给倒计时赋值并启用暂停键"""
        if self.timer.isActive():
            self.timer.stop()
        self.timer.start(1000)  # 每秒进一次timer，更新倒计时并判断是否重新进入下一轮
        self.countdown = self.timer_delay_seconds   # 重置倒计时
        self.ui.EditCountdown.setText(str(self.countdown))
        self.ui.ButtPause.setEnabled(True) # 启用暂停键
        self.ui.ButtPause.setText('暂停')

    def timer_stop(self):
        """结束计时：倒计时归零并清空计时窗口，锁定暂停键"""
        if self.timer.isActive():
            self.timer.stop()
        self.ui.ButtPause.setEnabled(False) # 禁用暂停键
        self.ui.ButtPause.setText('暂停(lock)')
        self.countdown = 0   # 倒计时归零
        self.ui.EditCountdown.setText("")

    def timer_pause(self):
        """暂停控制函数,仅当timer进行中可以解锁"""
        if self.timer.isActive():
            self.timer.stop()
            self.ui.ButtPause.setText('继续')
        else:
            self.ui.EditCountdown.setText(str(self.countdown))
            self.ui.ButtPause.setText('暂停')
            self.timer.start(1000)
    
    def add_time(self):
        self.timer_delay_seconds += 1
        self.ui.EditTimer.setText(str(self.timer_delay_seconds))

    def del_time(self):    
        self.timer_delay_seconds -= 1
        self.ui.EditTimer.setText(str(self.timer_delay_seconds))

    def reset_timer(self):
        """设置倒计时时长,支持[纯数字]&[分钟.秒]两种格式"""
        try:            
            time_input = self.ui.EditTimer.text() 
            time_list = time_input.split('.')
            for part in time_list:  # 输入必须是纯数字/小数
                if not part.isdigit():
                    number = re.findall("\d+\.?\d*", time_input)  # 正则表达式
                    self.timer_delay_seconds = number[0]  
                    self.ui.EditTimer.setText(number[0]) 
                    return False
            if len(time_list) == 1:
                self.timer_delay_seconds = int(time_list[0])
                assert self.timer_delay_seconds >= 1    # 定时时间必须大于等于1
            elif len(time_list) == 2:
                self.timer_delay_seconds = int(time_list[0])*60 + int(time_list[1])      
        except:
            # 删掉全部数据的时候会报错,恢复默认设置
            self.ui.EditTimer.setText('15')
            self.timer_delay_seconds = 15

    def reset_cycle_mode(self):
        """设置倒计时次数"""
        cycle_mode = int(self.ui.CboxCycleMode.currentIndex())
        if cycle_mode == 0:
            self.ui.EditCycleTimes.setText('0')
            self.cycle_index = 0    # 无限循环
        elif cycle_mode == 1:
            self.ui.EditCycleTimes.setText('1')
            self.cycle_index = 1    # 循环1次            
        elif cycle_mode == 2:
            self.ui.EditCycleTimes.setText('1')
            self.cycle_index = 1    # 先设成1
            self.ui.EditCycleTimes.setEnabled(True)
            self.ui.ButtAddCt.setEnabled(True)
            self.ui.ButtDelCt.setEnabled(True)

    def reset_cycle_index(self):
        """设置倒计时长"""
        self.cycle_index = int(self.ui.EditCycleTimes.text())

    def add_cycle_times(self):
        self.cycle_index += 1
        self.ui.EditCycleTimes.setText(str(self.cycle_index))

    def del_cycle_times(self):
        self.cycle_index -= 1
        self.ui.EditCycleTimes.setText(str(self.cycle_index))

    def reset_mode(self):
        """设置倒计时结束后执行的操作"""
        self.next_page_mode = self.ui.CboxMode.currentIndex()

    def one_second_event(self):
        """倒计时处理函数"""
        self.countdown -= 1
        self.ui.EditCountdown.setText(str(self.countdown))       
        if self.countdown == 0:                        
            self.time_out_event()
            self.countdown = self.timer_delay_seconds
            self.ui.EditCountdown.setText(str(self.countdown))
            # 根据剩余循环次数判断是否继续执行
            if self.cycle_index == 1:
                self.timer_stop()
                self.cycle_index = int(self.ui.EditCycleTimes.text())
            elif self.cycle_index > 1:
                self.cycle_index -= 1

    def time_out_event(self):
        """定时时刻执行的操作(按键控制)"""
        mode_index = self.next_page_mode
        # 单键操作
        keyboard_single_opr_list = [Key.right, Key.down, Key.left, Key.up, 
                                    Key.enter, Key.space, Key.tab, Key.cmd,
                                    Key.shift, Key.ctrl]
        # 多键操作 - win+XX
        win_opr_list = ['d']
        # 多键操作 - ctrl+XX
        ctrl_opr_list = ['s']

        # 三种操作列表的长度 
        single_length = len(keyboard_single_opr_list)    # single operation list   
        win_length = len(win_opr_list)        # win operation list  
        ctrl_length = len(ctrl_opr_list)    # ctrl operation list  

        # 单键操作     
        if self.next_page_mode < single_length:      
            self.keyboard.press(keyboard_single_opr_list[mode_index])
            time.sleep(0.02)
            self.keyboard.release(keyboard_single_opr_list[mode_index])
        # 多键操作 - win+XX
        elif self.next_page_mode < single_length + win_length: 
            self.keyboard.press(Key.cmd)
            self.keyboard.press(win_opr_list[mode_index - single_length])            
            time.sleep(0.02)
            self.keyboard.release(Key.cmd)  
            self.keyboard.release(win_opr_list[mode_index - single_length])                  
        # 多键操作 - ctrl+XX
        elif self.next_page_mode < single_length + win_length + ctrl_length:               
            self.keyboard.press(Key.ctrl)
            self.keyboard.press(ctrl_opr_list[mode_index - single_length - win_length])
            time.sleep(0.02)            
            self.keyboard.release(Key.ctrl)
            self.keyboard.release(ctrl_opr_list[mode_index - single_length - win_length])
        else:
            # print("ilegal opreation!")
            pass


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())