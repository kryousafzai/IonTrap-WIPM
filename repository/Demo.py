# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\QC\Desktop\GUI\rabi.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from artiq.experiment import *
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import os
import sys

class GUI_Reveal(EnvExperiment,object):
    """GUI_Parallel_Test"""
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl0")
        self.setattr_device("ttl1")
        self.setattr_device("ttl2")
        self.setattr_device("ttl3")
        self.setattr_device("urukul1_ch0")
        self.setattr_device("ttl4")
        
        #设置初始值，这些值可以随意设置，其目的是防止报错
        self.DPL_time=30
        self.SIDE_BAND_time=30
        self.Rabi_time=30
        DETECTION_time=100
        self.delay_time=100
        
    def pepare(self):
        pass
    
    @kernel
    def run(self):     
        with parallel:
        
            #进程1：执行量子信息操作周期
            with sequential:
                delay(5*ms)
                self.QC_Unit(self)
            
            #进程2：打开GUI
            delay(5*ms)
            self.GUI_Begin()
    
    def GUI_Begin(self)
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.setupUi(MainWindow)    
        MainWindow.show()
        sys.exit(app.exec_())
    
    # 将你更改过的量子信息操作周期的代码来替换QC_Unit函数
    @kernel    
    def QC_Unit:
        try:
            while True:
                
                #Dopplor_cooling
                self.ttl0.on()
                self.ttl1.on()
                self.ttl2.on()
                delay(self.DPL_time*ms)
                self.ttl0.off()
                self.ttl1.off()
                
                #Side_band_cooling
                self.ttl3.on()
                delay(self.SIDE_BAND_time*ms)
                self.ttl2.off()
                self.ttl3.off()
                    
                #控制Rabi时长
                self.ttl3.on()
                delay(self.Rabi_time*us)
                self.ttl3.off()

                #光子计数
                with parallel:
                    self.ttl4.gate_rising(self.DETECTION_time*ms)
                    
                    with sequential:
                        self.ttl0.on()
                        self.ttl1.on()
                        delay(self.DETECTION_time*ms)
                        self.ttl0.off()
                        self.ttl1.off()
                    
                #输出光子计数结果
                self.count_t = self.ttl4.count()
                self.set_dataset("Count_Num_t", self.count_t, broadcast=True)
                
                delay(self.delay_time*ms)
                
                
       #将原先GUI文件中的其余的所有非kernel下的代码复制到这行下面
       #警告！：禁止粘贴kernel下的代码
       
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(120, 130, 151, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Hello QC Lab"))
