from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys
import os
import ffmpeg
import io
from time import sleep

app = QApplication(sys.argv)

# 定义软件的界面
window = QWidget()
window.setWindowTitle("竖屏转横屏(输出在out/目录下)")
window.setFixedSize(400, 400)

label1 = QLabel(window)
label1.setText("选择文件：")
label1.move(40, 40)

button1 = QPushButton(window)
button1.setText("打开")
button1.move(120, 33)

button2 = QPushButton(window)
button2.setText("开始转换")
button2.move(200, 33)

textbox1 = QTextEdit(window)
textbox1.setReadOnly(True)
textbox1.resize(320, 150)
textbox1.move(40, 90)

label2 = QLabel(window)
label2.setText("正在处理：")
label2.move(40, 270)

label3 = QLabel(window)
label3.move(120, 270)
label3.resize(150, 15)

'''
bar = QProgressBar(window)
bar.resize(320, 10)
bar.move(40, 320)

textbox2 = QTextEdit(window)
textbox2.setReadOnly(True)
textbox2.resize(320, 50)
textbox2.move(40, 320)
'''

label4 = QLabel(window)
label4.resize(320, 15)
label4.move(40, 320)

# 获取视频文件名
def getFiles():
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.ExistingFiles)
    
    textbox1.clear()
    if dlg.exec_():
        filenames = dlg.selectedFiles()
        for name in filenames:
            textbox1.append(name)

button1.clicked.connect(getFiles)

def bar_set(v_max, v):
    bar.reset()
    bar.setMinimum(0.0)
    bar.setMaximum(v_max)
    bar.setValue(v)

# 转换一个视频文件
def process_single(filename):
    SCALE_OPTIONS = {'width': '-1', 'height': '720'}
    PAD_OPTIONS = {'width': '1280', 'height': '720', 'x': '(1280-iw) / 2', 'y': '0', 'color': 'black'}
    infile = ffmpeg.input(filename)
    stream = ffmpeg.filter_(infile, "scale", **SCALE_OPTIONS)
    stream = ffmpeg.filter_(stream, "pad", **PAD_OPTIONS)
    if not os.path.exists('out'):
        os.mkdir('out')
    last = filename.split('/')[-1]
    name = "out/" + last.split('.')[0] + "_new.mp4"
    stream.output(name).global_args(*['-y']).run()

# 转换所有的视频文件
def process_all():
    filenames = textbox1.toPlainText()
    filenames = filenames.split('\n')
    for name in filenames:
        last = name.split('/')[-1]
        label3.setText(last)
        label3.repaint()
        label4.setText("可能会花上十几分钟，请耐心等待(请不要连续点击)")
        label4.repaint()
        app.processEvents()
        process_single(name)
        #sleep(3)
    textbox1.clear()
    label4.setText("已经全部转换完成，视频在out/文件夹下")

button2.clicked.connect(process_all)

#process_single('input.mp4')
window.show()

sys.exit(app.exec())
